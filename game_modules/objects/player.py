import pygame
from ..globals import GameScreen, PlayerStats
from .dynamic_object import DynamicObject


class Player(DynamicObject):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2):
        super().__init__(image, pos)
        self.type : str = 'player'
        self.acceleration : int = 1
        self.speed : int = 0
        self.max_speed : int = PlayerStats.PLAYER_MAX_MOVEMENT_SPEED

    def calculate_velocity(self) -> None:
        self.direction.xy = self.movement_direction.xy
        if self.movement_direction.length() != 0:
            self.speed += self.acceleration
            self.speed = min(self.speed, self.max_speed)
        else:
            self.speed = 0
        self.movement_direction = pygame.Vector2(0, 0)

        if self.knockback_vel.length() != 0:
            self.vel.xy = self.knockback_vel.xy
            self.knockback_vel /= self.knockback_firction
            if self.knockback_vel.length() <= self.knockback_cutoff:
                self.knockback_vel = pygame.Vector2(0, 0)
        else:
            self.vel.xy = self.direction.xy * self.speed

    def fixed_update(self) -> None:
        super().fixed_update()

    def draw(self, surf : pygame.surface.Surface, alpha : float) -> None:
        alpha_pos = self.pos * alpha + self.prev_pos * (1 - alpha)
        draw_rect = self.rect.copy()
        draw_rect.topleft = alpha_pos
        surf.blit(self.image, draw_rect)