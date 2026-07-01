import pygame
from ..globals import GameScreen, PlayerStats
from .dynamic_object import DynamicObject


class SkyMushroom(DynamicObject):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2):
        super().__init__(image, pos)
        self.solid = False
        self.phasing = True
        self.type : str = 'sky'
        self.acceleration : int = 1
        self.speed : int = 2
        self.max_speed : int = 1

    def set_direction(self, direction="falling") -> pygame.Vector2:
        self.direction.xy = (0, 1)

    def calculate_velocity(self) -> None:
        self.set_direction()
        self.vel.xy = self.direction.xy * self.speed

    def fixed_update(self) -> None:
        super().fixed_update()

    def update(self, dt):
        if self.rect.top >= 40:
            self.phasing = False

    def draw(self, surf : pygame.surface.Surface, alpha : float) -> None:
        alpha_pos = self.pos * alpha + self.prev_pos * (1 - alpha)
        draw_rect = self.rect.copy()
        draw_rect.topleft = alpha_pos
        surf.blit(self.image, draw_rect)


    