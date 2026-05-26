import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch
import torch.nn as nn
import bulletchess
import numpy as np
from selector import mirror_square, num_to_piece_type

print(torch.__version__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def fen_to_layers(fen: str):
    board = bulletchess.Board.from_fen(fen)
    matrix = np.zeros((16, 8, 8), dtype=np.float32)

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

    if board.castling_rights.kingside(board.turn):
        matrix[12, :, :] = 1.0
    if board.castling_rights.queenside(board.turn):
        matrix[13, :, :] = 1.0
    if board.castling_rights.kingside(opp_col):
        matrix[14, :, :] = 1.0
    if board.castling_rights.queenside(opp_col):
        matrix[15, :, :] = 1.0

    return matrix


class ChessModel(nn.Module):
    def __init__(self):
        super(ChessModel, self).__init__()
        self.lin1 = nn.Linear(8 * 8 * 16, 512)
        self.lin2 = nn.Linear(512, 256)
        self.lin3 = nn.Linear(256, 1)

    def forward(self, x: torch.Tensor):
        x = torch.flatten(x, 1)
        x = torch.clamp(self.lin1(x), 0, 1) ** 2
        x = torch.clamp(self.lin2(x), 0, 1) ** 2
        x = self.lin3(x)

        return x


if __name__ == "__main__":
    model = ChessModel().to(device)

    weights = torch.load("evaluator.pth")

    model.load_state_dict(weights)
    while True:
        fen = input("Enter FEN: ")
        # rev = input("Reverse board? (y/n): ")
        # if rev.lower() == "y":
        #     fen = reverse_board(fen)
        matrix = fen_to_layers(fen)
        with torch.inference_mode():
            eva = model(torch.tensor(matrix, device=device).unsqueeze(0))
        print("Evaluation:", eva)
