from __future__ import annotations
from typing import Dict, Union
import pygame
from ..globals import GameScreen, PlayerStats
from .dynamic_object import DynamicObject


class Boss(DynamicObject):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2, get_player_pos, spawn_spores, spawn_super_mushroom):
        super().__init__(image, pos)
        self.get_player_pos = get_player_pos
        self.spawn_spores = spawn_spores
        self.spawn_super_mushroom = spawn_super_mushroom
        self.type : str = 'boss'
        self.acceleration : int = 1
        self.speed : int = 0
        self.max_speed : int = PlayerStats.PLAYER_MAX_MOVEMENT_SPEED - 1

        self.spore_to_spaw : int = 18
        self.boss_time : bool = 0.0
        self.boss_phases : list[Dict[str, Union[str, float]]] = [{"name" : "wait", "duration" : 2.0},
                                                                 {"name" : "chase", "duration" : 10.0},
                                                                 {"name" : "move_to_center", "duration" : 2.0},
                                                                 {"name" : "shoot_player", "duration" : 16.0},
                                                                {"name" : "spawn_super_mushroom", "duration" : 2.0},]
        
        self.hp : int = 3
        self.current_phase_index : int = 0
        self.current_phase : Dict[str, Union[str, float]] = self.boss_phases[self.current_phase_index]

        self.shoot_time : float = 0
        self.shoot_cooldown : float = 0.8

    def set_direction(self, direction="to_player") -> pygame.Vector2:
        if self.current_phase["name"] in ["wait", "shoot_player", "spawn_super_mushroom"]:
            return
        if self.current_phase["name"] == "move_to_center":
            boss_center = pygame.Vector2(self.rect.center)
            map_center = pygame.Vector2(800//2, (600 -40)//2)
            vec_to_center = map_center - boss_center
            if vec_to_center.length() < 8:
                self.movement_direction.xy = (0, 0)
                return
            if vec_to_center.length() != 0:
                vec_to_center.normalize_ip()
            self.movement_direction.xy = vec_to_center.xy
            return

        player_pos : pygame.Vector2 = self.get_player_pos()
        dirrection_to_player_x = player_pos.x - self.rect.centerx
        dirrection_to_player_y = player_pos.y - self.rect.centery
        direction_to_player_vec = pygame.Vector2(dirrection_to_player_x, dirrection_to_player_y)
        if direction_to_player_vec.length() != 0:
            direction_to_player_vec.normalize_ip()
        self.movement_direction.xy = direction_to_player_vec.xy

    def calculate_velocity(self) -> None:
        self.set_direction()
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

    def update(self, dt):
        self.boss_time += dt
        if self.boss_time >= self.current_phase["duration"]:
            self.boss_time = 0
            self.current_phase_index += 1
            self.current_phase_index %= len(self.boss_phases)
            self.current_phase = self.boss_phases[self.current_phase_index]
            if self.current_phase["name"] == "spawn_super_mushroom": self.spawn_super_mushroom()
        elif self.current_phase["name"] == "shoot_player":
            self.shoot_time += dt
            if self.shoot_time >= self.shoot_cooldown:
                self.spawn_spores()
                self.shoot_time = 0

    def draw(self, surf : pygame.surface.Surface, alpha : float) -> None:
        alpha_pos = self.pos * alpha + self.prev_pos * (1 - alpha)
        draw_rect = self.rect.copy()
        draw_rect.topleft = alpha_pos
        surf.blit(self.image, draw_rect)
        #pygame.draw.circle(surf, "red", self.rect.center, 200, width=4)