import torch
import torch.nn as nn
import chess
import numpy as np


class ResBlock(nn.Module):
    def __init__(self, channels):
        super(ResBlock, self).__init__()
        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(channels),
            nn.ReLU(),
        )
        self.conv = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.norm = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU()

    def forward(self, x):
        residual = x
        out = self.block(x)
        out = self.conv(out)
        out = self.norm(out)
        return self.relu(out + residual)


class ChessModel(nn.Module):
    def __init__(self):
        super(ChessModel, self).__init__()
        self.relu = nn.ReLU()
        self.conv = nn.Conv2d(16, 128, kernel_size=3, padding=1)
        self.conv1 = nn.Conv2d(128, 2, kernel_size=1)
        self.normalize = nn.BatchNorm2d(128)
        self.normalize1 = nn.BatchNorm2d(2)
        self.lin = nn.Linear(2 * 8 * 8, 4096)
        self.blocks3 = nn.Sequential(*[ResBlock(128) for _ in range(3)])
        self.blocks31 = nn.Sequential(*[ResBlock(128) for _ in range(3)])

    def forward(self, x):
        x = self.relu(self.normalize(self.conv(x)))
        x = self.blocks3(x)
        x = self.blocks31(x)
        x = self.relu(self.normalize1(self.conv1(x)))
        x = torch.flatten(x, 1)
        x = self.lin(x)

        return x


class Engine:
    def __init__(self):
        self.device = torch.device("cpu")
        self.model = ChessModel().to(self.device)
        weights = torch.load("chess_model.pth", map_location=torch.device('cpu'))
        self.model.load_state_dict(weights)

    def move(self, fen):
        matrix = self.fen_to_16_layers(fen)
        self.model.eval()
        with torch.inference_mode():
            output = self.model(matrix)
        return torch.argmax(output)

    def index_to_uci(self, index):
        # Get the 'from' and 'to' square integers (0-63)
        from_sq_int = index // 64
        to_sq_int = index % 64

        # Create the chess.Move object
        move = chess.Move(from_sq_int, to_sq_int)

        # Return the UCI string (e.g., "e2e4")
        return move.uci()

    def twoindexreturn(self, index):
        fromsqint = int(index // 64)
        tosqint = int(index % 64)

        fromsqintx, fromsqinty = fromsqint % 8, fromsqint // 8
        tosqintx, tosqinty = tosqint % 8, tosqint // 8

        print((fromsqintx, 7-fromsqinty), (tosqintx, 7-tosqinty))

        return ((fromsqintx, 7-fromsqinty), (tosqintx, 7-tosqinty))

    def fen_to_16_layers(self, fen):
        board = chess.Board(fen)
        matrix = np.zeros((16, 8, 8), dtype=np.float32)

        for color in [chess.WHITE, chess.BLACK]:
            offset = 0 if color == chess.WHITE else 6
            for piece_type in range(1, 7): # 1=Pawn, 6=King
                mask = board.pieces(piece_type, color)
                for square in mask:
                    row, col = 7 - (square // 8), square % 8
                    matrix[offset + piece_type - 1, row, col] = 1.0

        # Layer 12: Turn
        if board.turn == chess.WHITE:
            matrix[12, :, :] = 1.0

        # Layers 13 & 14: Legal Move Origins and Destinations
        for move in board.legal_moves:
            f_row, f_col = 7 - (move.from_square // 8), move.from_square % 8
            t_row, t_col = 7 - (move.to_square // 8), move.to_square % 8
            matrix[13, f_row, f_col] = 1.0
            matrix[14, t_row, t_col] = 1.0
        
        # Layer 15: Castling Rights
        if board.has_kingside_castling_rights(chess.WHITE):
            matrix[15, 0:4, 4:8] = 1.0  # White kingside (bottom-right quadrant)
        if board.has_queenside_castling_rights(chess.WHITE):
            matrix[15, 0:4, 0:4] = 1.0  # White queenside (bottom-left quadrant)
        if board.has_kingside_castling_rights(chess.BLACK):
            matrix[15, 4:8, 4:8] = 1.0  # Black kingside (top-right quadrant)
        if board.has_queenside_castling_rights(chess.BLACK):
            matrix[15, 4:8, 0:4] = 1.0  # Black queenside (top-left quadrant)

        return torch.from_numpy(matrix).cpu()[None, :]  # Return the single matrix


if __name__ == "__main__":
    engine = Engine()
    while True:
        fen = input("Enter FEN string (or 'exit' to quit): ")
        if fen == "exit":
            break
        move_index = np.asarray(engine.move(fen))
        print("Predicted move index:", move_index)
        print("Predicted move in UCI format:", engine.index_to_uci(move_index))
