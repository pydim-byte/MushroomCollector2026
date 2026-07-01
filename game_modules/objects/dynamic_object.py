import pygame
from ..globals import GameScreen, PlayerStats


class DynamicObject(pygame.sprite.Sprite):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2):
        super().__init__()
        self.image : pygame.surface.Surface = image
        self.rect = self.image.get_rect(midbottom=pos)
        self.solid = False
        self.pushable = False
        self.phasing = False

        self.knockback_vel = pygame.Vector2(0, 0)
        self.knockback_firction : int = 1.1
        self.knockback_cutoff : float = 1

        self.pos : pygame.Vector2 = pygame.Vector2(self.rect.x, self.rect.y)
        self.prev_pos : pygame.Vector2 = self.pos.copy()
        self.direction = pygame.Vector2(0,0)
        self.movement_direction = pygame.Vector2(0,0)
        self.vel = pygame.Vector2(0,0)
        self.speed = 1

    def set_direction(self,direction : pygame.Vector2) -> None:
        self.movement_direction.xy = direction.xy

    def calculate_velocity(self) -> None:
        self.direction.xy = self.movement_direction.xy
        self.vel.xy = self.direction.xy * self.speed

    def fixed_update(self) -> None:
        self.pos.xy = self.rect.topleft
        self.prev_pos.xy = self.pos.xy

    def update(self, dt : float) -> None:
        pass



    