import pygame
from typing import Tuple
from ..globals import GameScreen, PlayerStats
from .dynamic_object import DynamicObject


class Player(DynamicObject):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2, super_player, skin : pygame.surface.Surface, skin_offset : Tuple[int, int]):
        super().__init__(image, pos)
        self.normal_player : pygame.surface.Surface = image.copy()
        self.super_player : pygame.surface.Surface = super_player
        self.skin = skin
        self.skin_offset = skin_offset
        self.super : bool = False
        self.type : str = 'player'
        self.acceleration : int = 1
        self.speed : int = 0
        self.max_speed : int = PlayerStats.PLAYER_MAX_MOVEMENT_SPEED

        self.hp : int = 3
        self.super_time : float = 0

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

    def start_super_state(self) -> None:
        self.super = True
        self.super_time += 5
        self.image = self.super_player

    def update(self, dt):
        if self.super and self.super_time > 0:
            self.super_time -= dt
        elif self.super and self.super_time <= 0:
            self.super = False
            self.super_time = 0
            self.image = self.normal_player

            

    def draw(self, surf : pygame.surface.Surface, alpha : float) -> None:
        alpha_pos = self.pos * alpha + self.prev_pos * (1 - alpha)
        draw_rect = self.rect.copy()
        draw_rect.topleft = alpha_pos
        surf.blit(self.image, draw_rect)
        if self.skin:
            skin_rect = draw_rect.copy()
            skin_rect.move_ip(self.skin_offset)
            surf.blit(self.skin, skin_rect)