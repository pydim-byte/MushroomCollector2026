from __future__ import annotations
from game_modules.objects.static_object import StaticObject
import pygame


class InvisibleWall(StaticObject):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2):
        super().__init__(image, pos)
        self.solid = True

    def alive(self):
        return True

    def draw(self, surf : pygame.surface.Surface, alpha : float) -> None:
        pass