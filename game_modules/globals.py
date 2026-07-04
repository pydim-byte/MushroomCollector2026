from __future__ import annotations
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from enum import Enum
import pygame, os


class GameUpdate():
    FPS : int = 60
    FIXED_TPS : int = 60

class GameScreen():
    SCREEN_WIDTH : int = 800
    SCREEN_HEIGHT : int = 600
    DISPLAY_WIDTH : int = 800
    DISPLAY_HEIGHT : int = 600

class PlayerStats():
    PLAYER_ACCELERATION : int = 1
    PLAYER_MOVEMENT_SPEED : int = 1
    PLAYER_MAX_MOVEMENT_SPEED : int = 8

class SkinsUnlocks:
    LEVELS_WITH_SKINS = (3, 6, 7, 10)
    LEVELS_WITH_SHOP = (7,)
    SKINS = {
        3 : {"skin" : "glasses.png", "offset": (0, 0), "unlocked" : False},
        6 : {"skin" : "cool.png", "offset": (0, 0), "unlocked" : False},
        7 : {"skin" : "angel.png", "offset": (0, -7), "unlocked" : False},
        10 : {"skin" : "bro.png", "offset": (0, -2), "unlocked" : False},
    }



