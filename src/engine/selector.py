import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bulletchess
import numpy as np
import torch
import torch.nn as nn


def mirror_square(square: int) -> int:
    return square ^ 0x38


def num_to_piece_type(num: int) -> bulletchess.PieceType:
    match num:
        case 1:
            return bulletchess.PAWN
        case 2:
            return bulletchess.KNIGHT
        case 3:
            return bulletchess.BISHOP
        case 4:
            return bulletchess.ROOK
        case 5:
            return bulletchess.QUEEN
        case 6:
            return bulletchess.KING
        case _:
            raise ValueError(f"Invalid piece type number: {num}")


def fen_to_layers(fen: str):
    board = bulletchess.Board.from_fen(fen)
    matrix = np.zeros((15, 8, 8), dtype=np.float32)

    is_black = board.turn == bulletchess.BLACK
    opp_col = bulletchess.WHITE if is_black else bulletchess.BLACK

    for color in [bulletchess.WHITE, bulletchess.BLACK]:
        us = color == board.turn
        offset = 0 if us else 6

        for piece_type in range(1, 7):  # 1=Pawn, 6=King
            pt = num_to_piece_type(piece_type)
            bb = board.__getitem__((color, pt))
            for square in bb:
                index = square.index()
                sq = mirror_square(index) if is_black else index
                row, col = 7 - (sq // 8), sq % 8
                matrix[offset + piece_type - 1, row, col] = 1.0

    for move in board.legal_moves():
        fsq = mirror_square(move.origin.index()) if is_black else move.origin.index()
        tsq = (
            mirror_square(move.destination.index())
            if is_black
            else move.destination.index()
        )

        f_row, f_col = 7 - (fsq // 8), fsq % 8
        t_row, t_col = 7 - (tsq // 8), tsq % 8
        matrix[12, f_row, f_col] = 1.0
        matrix[13, t_row, t_col] = 1.0

    if board.castling_rights.kingside(board.turn):
        matrix[14, 0:4, 4:8] = 1.0  # White kingside (bottom-right quadrant)
    if board.castling_rights.queenside(board.turn):
        matrix[14, 0:4, 0:4] = 1.0  # White queenside (bottom-left quadrant)
    if board.castling_rights.kingside(opp_col):
        matrix[14, 4:8, 4:8] = 1.0  # Black kingside (top-right quadrant)
    if board.castling_rights.queenside(opp_col):
        matrix[14, 4:8, 0:4] = 1.0  # Black queenside (top-left quadrant)

    return matrix, is_black


def index_to_move(index: int, is_black: bool) -> bulletchess.Move:
    from_sq_int = index // 64
    to_sq_int = index % 64

    if is_black:
        from_sq_int = mirror_square(from_sq_int)
        to_sq_int = mirror_square(to_sq_int)

    move = bulletchess.Move(
        bulletchess.SQUARES[from_sq_int], bulletchess.SQUARES[to_sq_int]
    )

    return move


class ResBlock(nn.Module):
    def __init__(self, channels: int):
        super(ResBlock, self).__init__()
        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(channels),
            nn.ReLU(),
        )
        self.conv = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.norm = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU()

    def forward(self, x: torch.Tensor):
        residual = x
        out = self.block(x)
        out = self.conv(out)
        out = self.norm(out)
        return self.relu(out + residual)


class ChessModel(nn.Module):
    def __init__(self):
        super(ChessModel, self).__init__()
        self.relu = nn.ReLU()
        self.conv = nn.Conv2d(15, 128, kernel_size=3, padding=1)
        self.conv1 = nn.Conv2d(128, 64, kernel_size=1)
        self.normalize = nn.BatchNorm2d(128)
        self.normalize1 = nn.BatchNorm2d(64)
        self.lin = nn.Linear(64 * 8 * 8, 4096)
        self.blocks = nn.Sequential(*[ResBlock(128) for _ in range(12)])

    def forward(self, x: torch.Tensor):
        x = self.relu(self.normalize(self.conv(x)))

        x = self.blocks(x)

        x = self.relu(self.normalize1(self.conv1(x)))
        x = torch.flatten(x, 1)
        x = self.lin(x)

        return x


if __name__ == "__main__":
    k = 5
    engine = ChessModel()
    weights = torch.load("selectortemp.pth")
    engine.load_state_dict(weights)
    while True:
        fen = input("Enter FEN: ")
        matrix, is_black = fen_to_layers(fen)
        input_tensor = torch.tensor(matrix).unsqueeze(0)
        with torch.no_grad():
            chance, bk = torch.topk(engine(input_tensor), k=k)
        output = []
        for i in range(k):
            output.append(
                (index_to_move(bk[0][i].item(), is_black).uci(), chance[0][i].item())
            )

        print(output)
