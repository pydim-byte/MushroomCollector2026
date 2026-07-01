import pygame
from ..globals import GameScreen, PlayerStats
from .dynamic_object import DynamicObject


class Spore(DynamicObject):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2, movement_direction : pygame.Vector2):
        super().__init__(image, pos)
        self.rect = self.image.get_rect(center=pos)
        self.movement_direction : pygame.Vector2 = movement_direction
        self.solid = False
        self.phasing = True
        self.type : str = 'spore'
        self.acceleration : int = 1
        self.speed : int = 6
        self.max_speed : int = 1
        
        self.timer = 0

    def set_direction(self, direction="away_from_boss") -> pygame.Vector2:
        self.direction.xy = self.movement_direction.xy

    def calculate_velocity(self) -> None:
        self.set_direction()
        self.vel.xy = self.direction.xy * self.speed

    def fixed_update(self) -> None:
        super().fixed_update()

    def update(self, dt):
        self.timer += dt
        if self.timer >= 10:
            self.kill()

    def draw(self, surf : pygame.surface.Surface, alpha : float) -> None:
        alpha_pos = self.pos * alpha + self.prev_pos * (1 - alpha)
        draw_rect = self.rect.copy()
        draw_rect.topleft = alpha_pos
        surf.blit(self.image, draw_rect)


    