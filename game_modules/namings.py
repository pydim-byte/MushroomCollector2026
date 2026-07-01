from enum import Enum, auto


class StateName(Enum):
    MAIN_MENU = auto()
    GAMEPLAY = auto()
    LEVEL_MENU = auto()
    SKINS_MENU = auto()
    LEVEL_COMPLETE = auto()
    GAME_OVER = auto()