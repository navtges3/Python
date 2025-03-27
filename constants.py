from enum import Enum

class GameState(Enum):
    WELCOME = 1
    NEW_GAME = 2
    MAIN_GAME = 3
    GAME_OVER = 4