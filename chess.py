from enum import Enum
from pathlib import Path
import json

class PieceColor(Enum):
    WHITE = 1
    BLACK = 2

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
    
class Piece:
    def __init__(self, color : PieceColor, type : PieceType):
        self.__color = color
        self.__type = type

    def get_color(self):
        return self.__color
    
    def get_type(self):
        return self.__type
    
    def __str__(self):
        if self.__color == PieceColor.BLACK:
            if self.__type == PieceType.PAWN:
                return '\u265F'
            elif self.__type == PieceType.KNIGHT:
                return '\u265E'
            elif self.__type == PieceType.BISHOP:
                return '\u265D'
            elif self.__type == PieceType.ROOK:
                return '\u265C'
            elif self.__type == PieceType.QUEEN:
                return '\u265B'
            elif self.__type == PieceType.KING:
                return '\u265A'
        else:
            if self.__type == PieceType.PAWN:
                return '\u2659'
            elif self.__type == PieceType.KNIGHT:
                return '\u2658'
            elif self.__type == PieceType.BISHOP:
                return '\u2657'
            elif self.__type == PieceType.ROOK:
                return '\u2656'
            elif self.__type == PieceType.QUEEN:
                return '\u2655'
            elif self.__type == PieceType.KING:
                return '\u2654'

class InvalidMove(Exception):
    pass

class Board:

    __cell_height = 3
    __cell_width = 6

    __white_cell_bg = '47'
    __black_cell_bg = '40'

    __white_piece_fg = '33'
    __black_piece_fg = '32'

    def __init__(self):
        self.__board = [[ None for i in range(8) ] for l in range(8)]

    def init0(self):

        self.__board = [[ None for i in range(8) ] for l in range(8)]

        self.__board[0][0] = Piece(PieceColor.BLACK, PieceType.ROOK)
        self.__board[0][1] = Piece(PieceColor.BLACK, PieceType.KNIGHT)
        self.__board[0][2] = Piece(PieceColor.BLACK, PieceType.BISHOP)
        self.__board[0][3] = Piece(PieceColor.BLACK, PieceType.QUEEN)
        self.__board[0][4] = Piece(PieceColor.BLACK, PieceType.KING)
        self.__board[0][5] = Piece(PieceColor.BLACK, PieceType.BISHOP)
        self.__board[0][6] = Piece(PieceColor.BLACK, PieceType.KNIGHT)
        self.__board[0][7] = Piece(PieceColor.BLACK, PieceType.ROOK)

        for i in range(8):
            self.__board[1][i] = Piece(PieceColor.BLACK, PieceType.PAWN)

        for i in range(8):
            self.__board[6][i] = Piece(PieceColor.WHITE, PieceType.PAWN)

        self.__board[7][0] = Piece(PieceColor.WHITE, PieceType.ROOK)
        self.__board[7][1] = Piece(PieceColor.WHITE, PieceType.KNIGHT)
        self.__board[7][2] = Piece(PieceColor.WHITE, PieceType.BISHOP)
        self.__board[7][3] = Piece(PieceColor.WHITE, PieceType.QUEEN)
        self.__board[7][4] = Piece(PieceColor.WHITE, PieceType.KING)
        self.__board[7][5] = Piece(PieceColor.WHITE, PieceType.BISHOP)
        self.__board[7][6] = Piece(PieceColor.WHITE, PieceType.KNIGHT)
        self.__board[7][7] = Piece(PieceColor.WHITE, PieceType.ROOK)

    def move(self, source, dest):
        
        if self.__board[source[0]][source[1]] is None:
            raise InvalidMove("Source cell is empty")
        if self.__board[dest[0]][dest[1]] is not None and self.__board[dest[0]][dest[1]].get_color() == self.__board[source[0]][source[1]].get_color():
            raise InvalidMove("Destination cell contains a piece of the same color")
        
        self.__board[dest[0]][dest[1]] = self.__board[source[0]][source[1]]
        self.__board[source[0]][source[1]] = None

    def print(self):

        for row in range(8):
            for i in range(self.__cell_height):
                for col in range(8):
                    str_color = '\x1b[0;'
                    str_color += self.__white_piece_fg if self.__board[row][col] is not None and self.__board[row][col].get_color() == PieceColor.WHITE else self.__black_piece_fg
                    str_color += ';'
                    str_color += self.__black_cell_bg if (col + row) % 2 else self.__white_cell_bg
                    str_color += 'm'
                    
                    
                    if i == (self.__cell_height // 2):
                        cell_center = str(self.__board[row][col]) if self.__board[row][col] is not None else " "
                        cell_center += " " if self.__cell_width % 2 == 0 else ""
                        content = (" " * ((self.__cell_width - 1) // 2)) + f"{cell_center}" + (" " * ((self.__cell_width - 1) // 2))
                    else:
                        content = " " * self.__cell_width

                    print(str_color + content + '\x1b[0m', end="")
                    
                    if col == 7:
                        print() 
    
    def export_data(self):
        
        ret = []
        for row in range(8):
            for col in range(8):
                if self.__board[row][col] is not None:
                    ret.append({
                        "row": row,
                        "col": col,
                        "color": self.__board[row][col].get_color().name,
                        "type": self.__board[row][col].get_type().name
                    })
        return ret
    
    def import_data(self, json_data):
        
        self.__board = [[ None for i in range(8) ] for l in range(8)]

        for piece_data in json_data:
            row = piece_data["row"]
            col = piece_data["col"]
            color = PieceColor[piece_data["color"]]
            piece_type = PieceType[piece_data["type"]]
            self.__board[row][col] = Piece(color, piece_type)



if __name__ == "__main__":

    board = Board()

    if Path('board.json').is_file():
        with open("board.json", "r") as f:
            board.import_data(json.loads(f.read()))
    else:
        board.init0()

    board.print()

    #print(board.to_json())

    while True:
        move = input(">>> Move: ")
        move = move.upper()

        if move == "QUIT":
            print("Goodbye!")
            break

        if move == "RESET":
            board.init0()
            board.print()
            continue
        
        move = move.replace(" ","")
        if move[0] not in "ABCDEFGH" or move[1] not in "12345678" or move[2] not in "ABCDEFGH" or move[3] not in "12345678":
            print("Invalid move")
            continue

        source = [8 - int(move[1]), ord(move[0]) - 65]
        dest = [8 - int(move[3]), ord(move[2]) - 65]
        print("move:", source, dest)

        try:
            board.move(source, dest)
        except InvalidMove as e:
            print(e)

        board.print()


    with open("board.json", "w") as f:
        f.write(json.dumps(board.export_data()))
