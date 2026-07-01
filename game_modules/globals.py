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


