from chess import Board


class User:
    __in_a_game = False
    __game = None
    __websocket = None

    def __init__(self, id = None, username = None):
        self.__id = id
        self.__username = username

    def is_in_a_game(self):
        return self.__in_a_game
    
    def set_in_a_game(self, in_a_game):
        self.__in_a_game = in_a_game
    
    def get_id(self):
        return self.__id
    
    def get_username(self):
        return self.__username
    
    def set_game(self, game):
        self.__game = game

    def get_game(self):
        return self.__game
    
    def set_websocket(self, websocket):
        self.__websocket = websocket

    def get_websocket(self):
            return self.__websocket

    def __str__(self):
        return f"[{self.__id}] {self.__username}"
    
    def export_data(self):
        """
        Export the data of the user to a dictionary.
        """
        return {
            "id": self.__id,
            "username": self.__username
        }
    
    def import_data(self, data):
        """
        Import the data of the user from a dictionary.
        """
        self.__id = data["id"]
        self.__username = data["username"]

class Game:

    def __init__(self, white: User = None, black: User = None):
        self.__white = white
        self.__black = black
        self.__turn = 'white'

        self.__board = Board()
        self.__board.init0()
    
    def get_white(self):
        return self.__white

    def get_black(self):
        return self.__black

    def get_turn(self):
        return self.__turn

    def get_board(self):
        return self.__board
    
    def move(self, source, dest):
        self.__board.move(source, dest)
        self.__turn = 'black' if self.__turn == 'white' else 'white'
    
    def export_data(self):
        """
        Export the data of the game to a dictionary.
        """
        return {
            "white": self.__white.export_data(),
            "black": self.__black.export_data(),
            "turn": self.__turn,
            "board": self.__board.export_data()
        }
    
    def import_data(self, data):
        """
        Import the data of the game from a dictionary.
        """
        self.__white = User()
        self.__white.import_data(data["white"])
        self.__black = User()
        self.__black.import_data(data["black"])
        self.__turn = data["turn"]
        self.__board = Board()
        self.__board.import_data(data["board"])

