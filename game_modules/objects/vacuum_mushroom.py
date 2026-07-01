import pygame
from ..globals import GameScreen, PlayerStats
from .dynamic_object import DynamicObject


class VacuumMushroom(DynamicObject):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2, get_player_pos):
        super().__init__(image, pos)
        self.solid = False
        self.get_player_pos = get_player_pos
        self.type : str = 'vacuum_mushroom'
        self.acceleration : int = 1
        self.speed : int = 0
        self.max_speed : int = 1

    def set_direction(self, direction="to_player") -> pygame.Vector2:
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
        self.vel.xy = self.direction.xy * self.speed

    def fixed_update(self) -> None:
        self.rect.clamp_ip(0, 40, GameScreen.SCREEN_WIDTH, GameScreen.SCREEN_HEIGHT - self.rect.height)
        super().fixed_update()

    def draw(self, surf : pygame.surface.Surface, alpha : float) -> None:
        alpha_pos = self.pos * alpha + self.prev_pos * (1 - alpha)
        draw_rect = self.rect.copy()
        draw_rect.topleft = alpha_pos
        surf.blit(self.image, draw_rect)


    