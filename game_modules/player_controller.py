from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_modules.objects.player import Player
import pygame


class PlayerController:
    def __init__(self,player : Player):
        self.player = player

    def handle_inputs(self, inputs : dict[pygame.event.Event, bool]) -> None:
        move_direction = pygame.Vector2(0,0)
        if inputs[pygame.K_LEFT]:
            move_direction.x = -1
        if inputs[pygame.K_RIGHT]:
            move_direction.x = 1
        if inputs[pygame.K_UP]:
            move_direction.y = -1
        if inputs[pygame.K_DOWN]:
            move_direction.y = 1
        if move_direction.length() != 0: move_direction.normalize_ip()
        self.player.set_direction(move_direction)
        
        if inputs[pygame.K_SPACE]:
            pass