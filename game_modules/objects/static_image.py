from __future__ import annotations
import pygame


class StaticImage(pygame.sprite.Sprite):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2):
        super().__init__()
        self.image = image
        self.pos = pos
        self.rect : pygame.Rect = self.image.get_rect(topleft=pos) 

    def draw(self, screen : pygame.surface.Surface, aplha : float) -> None:
        screen.blit(self.image, self.rect)

