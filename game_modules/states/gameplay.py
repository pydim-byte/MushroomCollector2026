from __future__ import annotations
from typing import TYPE_CHECKING
from .state import State
import pygame, sys
from game_modules.globals import SkinsUnlocks
from game_modules.namings import StateName
from game_modules.states.state import State
from game_modules.world import World
from game_modules.player_controller import PlayerController
from game_modules.physic_manager import PhysicManager


class Gameplay(State):
    def __init__(self):
        super().__init__()
        self.world = World(state=StateName.GAMEPLAY)
        self.physic_manager = PhysicManager(self.world)
        self.player_controller = PlayerController(self.world.player)

    def restart_level(self) -> None:
        self.quit = True
        self.next_state = StateName.GAMEPLAY

    def quit_to_menu(self) -> None:
        self.quit = True
        self.next_state = StateName.MAIN_MENU 

    def game_over(self) -> None:
        self.quit = True
        self.next_state = StateName.GAME_OVER

    def complete_level(self) -> None:
        self.quit = True
        World.TOTAL_MUSHROOMS_COLLECTED += 20
        if World.GAMEPLAY_LEVEL in SkinsUnlocks.LEVELS_WITH_SHOP:
            if World.TOTAL_MUSHROOMS_COLLECTED >= 120:
                self.next_state = StateName.SHOP
                return
            
        if World.GAMEPLAY_LEVEL in SkinsUnlocks.LEVELS_WITH_SKINS:
            if not SkinsUnlocks.SKINS[World.GAMEPLAY_LEVEL]["unlocked"]:
                self.next_state = StateName.NEW_SKIN
                return
        if World.GAMEPLAY_LEVEL != 9:
            World.GAMEPLAY_LEVEL += 1
        self.next_state = StateName.LEVEL_COMPLETE



    def handle_inputs(self, inputs : dict[pygame.event.Event, bool]) -> None:
        if inputs[pygame.K_SPACE]:
            print("bad one")
        if inputs[pygame.K_r]:
            self.restart_level()
        elif inputs[pygame.K_ESCAPE]:
            self.quit_to_menu()
        self.player_controller.handle_inputs(inputs)

    def fixed_update(self) -> None:
        self.physic_manager.fixed_update()
        for obj in self.world.dynamic_objects:
            obj.fixed_update()

    def update(self,dt : float) -> None:
        if not self.world.player.alive():
            self.game_over()
        if self.world.collected_mushrooms >= 20:
            self.complete_level()
        if World.GAMEPLAY_LEVEL == 9:
            if self.world.player.hp <= 0:
                self.game_over()
            elif self.world.boss.hp <= 0:
                self.complete_level()
        for clock in self.world.object_clocks:
            clock.update(dt)
        self.world.all_sprites.update(dt)

    def draw(self, screen : pygame.surface.Surface, alpha : float) -> None:
        for sprite in self.world.all_sprites:
            sprite.draw(screen, alpha)