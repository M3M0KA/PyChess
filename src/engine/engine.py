import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch
import bulletchess
from selector import ChessModel as SelectorModel, index_to_move, fen_to_layers
from evaluator import (
    ChessModel as EvaluatorModel,
    fen_to_layers as eval_fen_to_layers,
)

width_tree = 12
depth_tree = 6

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if (
    torch.cuda.is_available()
    and hasattr(torch, "set_float32_matmul_precision")
    and torch.cuda.get_device_capability()[0] >= 8
):
    torch.set_float32_matmul_precision("high")

path = os.path.dirname(os.path.abspath(__file__))
sel_path = os.path.join(path, "selector.pth")
eval_path = os.path.join(path, "evaluator.pth")


def mirror_square(square: int) -> int:
    return square ^ 0x38


class MoveIndexer:
    def __init__(self):
        self.lookup = {}

        for start_sq in range(64):
            for end_sq in range(64):
                uci = (
                    bulletchess.SQUARES[start_sq].index(),
                    bulletchess.SQUARES[end_sq].index(),
                )
                self.lookup[uci] = (start_sq * 64) + end_sq

    def get_index(self, uci: tuple) -> int:
        return self.lookup[uci]


class Engine:
    def __init__(self):
        self.move_indexer = MoveIndexer()
        self.selector = SelectorModel().to(device)
        self.evaluator = EvaluatorModel().to(device)

        selector_weights = torch.load(sel_path)
        evaluator_weights = torch.load(eval_path)

        self.selector.load_state_dict(selector_weights)
        self.evaluator.load_state_dict(evaluator_weights)

        self.selector = torch.compile(self.selector, mode="reduce-overhead")
        self.evaluator = torch.compile(self.evaluator, mode="reduce-overhead")

    def select_move(
        self, fen: str, width_tree: int = width_tree, return_moves: bool = False
    ):
        with torch.no_grad():
            matrix, is_black = fen_to_layers(fen)
            input_tensor = (
                torch.from_numpy(matrix)
                .unsqueeze(0)
                .to(device=device, non_blocking=True)
            )
            output = self.selector(input_tensor)
            board = bulletchess.Board.from_fen(fen)
            mask = torch.full_like(output, float("-inf"))
            legal_moves = board.legal_moves()
            length = len(legal_moves)
            for move in legal_moves:
                uci = (
                    (move.origin.index(), move.destination.index())
                    if not is_black
                    else (
                        mirror_square(move.origin.index()),
                        mirror_square(move.destination.index()),
                    )
                )
                index = self.move_indexer.get_index(uci)

                if mask[0][index] == float("-inf"):
                    mask[0][index] = output[0][index]
                else:
                    length -= 1
                    continue

            score, bk = torch.topk(mask, k=min(length, width_tree))

        output = []
        if not return_moves:
            for i in bk[0]:
                output.append(index_to_move(i.item(), is_black).uci())
        else:
            for i in bk[0]:
                output.append(index_to_move(i.item(), is_black))
        return output

    def evaluate_position(self, fen: str):
        matrix = eval_fen_to_layers(fen)
        input_tensor = torch.from_numpy(matrix).unsqueeze(0).to(device)
        with torch.no_grad():
            evaluation = self.evaluator(input_tensor).item()
            return evaluation

    def handle_fen(self, fen: str, depth: int = depth_tree):
        best = [float("-inf"), None]  # [evaluation, move]
        board = bulletchess.Board.from_fen(fen)
        self.cutted = 0

        alpha = float("-inf")

        for move in self.select_move(fen, return_moves=True):
            print(f"Evaluating move: {move.uci()}")
            try:
                board.apply(move)
            except ValueError:
                continue

            evaluation = self.minimax(board.fen(), True, depth - 1, alpha)

            board.undo()

            if evaluation > best[0]:
                best = [evaluation, move]

            alpha = max(alpha, evaluation)

        return best[1], best[0]

    def minimax(
        self,
        fen: str,
        minimizing: bool,
        depth: int = depth_tree,
        alpha: float = float("-inf"),
        beta: float = float("inf"),
    ):

        if depth == 0:
            return self.quiescence(minimizing, fen, alpha, beta)

        board = bulletchess.Board.from_fen(fen)

        if minimizing:
            best = float("inf")
            for move in self.select_move(fen, return_moves=True):
                try:
                    board.apply(move)
                except ValueError:
                    continue
                if board in bulletchess.CHECKMATE:
                    evaluation = float("-inf")
                else:
                    evaluation = self.minimax(
                        board.fen(),
                        False,
                        depth - 1,
                        alpha,
                        beta,
                    )

                board.undo()

                best = min(best, evaluation)
                beta = min(beta, evaluation)

                if beta <= alpha:
                    self.cutted += 1
                    break

            return best

        else:
            best = float("-inf")
            for move in self.select_move(fen, return_moves=True):
                try:
                    board.apply(move)
                except ValueError:
                    continue
                if board in bulletchess.CHECKMATE:
                    evaluation = float("inf")
                else:
                    evaluation = self.minimax(
                        board.fen(),
                        True,
                        depth - 1,
                        alpha,
                        beta,
                    )
                board.undo()

                alpha = max(alpha, evaluation)
                best = max(best, evaluation)
                if beta <= alpha:
                    self.cutted += 1
                    break
            return best

    def quiescence(
        self,
        minimizing: bool,
        fen: str,
        alpha: float = float("-inf"),
        beta: float = float("inf"),
        cdepth: int = 0,
    ):
        eva = self.evaluate_position(fen)
        if cdepth >= 3:
            return eva

        if minimizing:
            if eva < alpha:
                return eva
            beta = min(beta, eva)
        else:
            if eva > beta:
                return eva
            alpha = max(alpha, eva)

        moves = self.select_move(fen, width_tree=width_tree * 2, return_moves=True)
        board = bulletchess.Board.from_fen(fen)
        best = eva
        if minimizing:
            for move in moves:
                if move.is_capture(board):
                    try:
                        board.apply(move)
                    except ValueError:
                        continue
                    if board in bulletchess.CHECKMATE:
                        evaluation = float("-inf")
                    else:
                        evaluation = self.quiescence(
                            minimizing=False,
                            fen=board.fen(),
                            alpha=alpha,
                            beta=beta,
                            cdepth=cdepth + 1,
                        )
                    board.undo()
                    beta = min(beta, evaluation)
                    best = min(best, evaluation)
                    if beta <= alpha:
                        self.cutted += 1
                        break
            return best
        else:
            for move in moves:
                if move.is_capture(board):
                    try:
                        board.apply(move)
                    except ValueError:
                        continue
                    if board in bulletchess.CHECKMATE:
                        evaluation = float("inf")
                    else:
                        evaluation = self.quiescence(
                            minimizing=True,
                            fen=board.fen(),
                            alpha=alpha,
                            beta=beta,
                            cdepth=cdepth + 1,
                        )
                    board.undo()
                    alpha = max(alpha, evaluation)
                    best = max(best, evaluation)
                    if beta <= alpha:
                        self.cutted += 1
                        break
            return best

    def twoindexreturn(self, index):
        fromsqint = int(index // 64)
        tosqint = int(index % 64)

        fromsqintx, fromsqinty = fromsqint % 8, fromsqint // 8
        tosqintx, tosqinty = tosqint % 8, tosqint // 8

        return ((fromsqintx, 7 - fromsqinty), (tosqintx, 7 - tosqinty))

    def uci_to_index(self, uci):
        move = bulletchess.Move.from_uci(uci)
        return (move.origin.index() * 64) + move.destination.index()


if __name__ == "__main__":
    engine = Engine()
    while True:
        fen = input("Enter FEN: ")
        move, evaluation = engine.handle_fen(fen)
        print(f"Selected Move: {move}, Evaluation: {evaluation}")
        print(engine.twoindexreturn(engine.uci_to_index(move.uci())))
