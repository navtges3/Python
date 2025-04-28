from enum import Enum

class Game_State(Enum):
    WELCOME = 1
    NEW_GAME = 2
    MAIN_GAME = 3
    BATTLE = 4
    SHOP = 5
    GAME_OVER = 6
    EXIT = 7

class Battle_Action(Enum):
    HOME = 0
    ATTACK = 1
    DEFEND = 2
    USE_ITEM = 3
    RUN_AWAY = 4
    MONSTER_DEFEATED = 5