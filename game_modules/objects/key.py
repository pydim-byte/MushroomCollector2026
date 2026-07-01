import pygame
from ..globals import GameScreen, PlayerStats
from .dynamic_object import DynamicObject


class Key(DynamicObject):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2):
        super().__init__(image, pos)
        self.solid = True
        self.pushable = True
        self.push_vel = pygame.Vector2(0, 0)
        self.type : str = 'key'
        self.acceleration : int = 1
        self.speed : int = 0
        self.max_speed : int = PlayerStats.PLAYER_MAX_MOVEMENT_SPEED

    def calculate_velocity(self) -> None:
        self.vel.xy = self.push_vel.xy
        self.push_vel = pygame.Vector2(0, 0)

    def fixed_update(self) -> None:
        self.push_direction = pygame.Vector2(0, 0)
        super().fixed_update()

    def draw(self, surf : pygame.surface.Surface, alpha : float) -> None:
        alpha_pos = self.pos * alpha + self.prev_pos * (1 - alpha)
        draw_rect = self.rect.copy()
        draw_rect.topleft = alpha_pos
        surf.blit(self.image, draw_rect)