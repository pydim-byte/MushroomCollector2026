from __future__ import annotations
import pygame


class StaticObject(pygame.sprite.Sprite):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2):
        super().__init__()
        self.image : pygame.surface.Surface = image
        self.rect = self.image.get_rect(midbottom=pos)
        self.pos : pygame.Vector2 = pygame.Vector2(self.rect.x, self.rect.y)
        self.solid = True
        self.pushable = False

    def update(self, dt : float) -> None:
        pass