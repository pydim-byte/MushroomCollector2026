from __future__ import annotations
from game_modules.objects.static_object import StaticObject
import pygame


class Flood(StaticObject):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2):
        super().__init__(image, pos)
        self.solid = True
        self.render_rect = self.rect.copy()
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width - 4, self.rect.height - 4)
        self.rect.center = self.render_rect.center

    def draw(self, surf : pygame.surface.Surface, alpha : float) -> None:
        surf.blit(self.image, self.render_rect)