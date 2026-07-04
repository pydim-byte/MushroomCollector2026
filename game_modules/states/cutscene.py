from __future__ import annotations
from typing import TYPE_CHECKING
from game_modules.namings import StateName
from game_modules.states.state import State
from game_modules.assets_loader import AssetsLoader
from game_modules.world import World
import pygame


class Cutscene(State):
    def __init__(self):
        super().__init__()
        self.world = World(state=StateName.CUTSCENE)
        self.assets_loader = AssetsLoader()
        self.assets = self.assets_loader.assets

    def next_level(self) -> None:
        self.quit = True
        self.next_state = StateName.GAMEPLAY

    def handle_inputs(self, inputs : dict[pygame.event.Event, bool]) -> None:
        if inputs[pygame.K_SPACE]:
            self.next_level()

    def fixed_update(self) -> None:
        for obj in self.world.dynamic_objects:
            obj.fixed_update()

    def update(self,dt : float) -> None:
        self.world.all_sprites.update(dt)

    def draw_menu_items(self, screen : pygame.surface.Surface) -> None:
        title_surf = self.assets["PressStart2P.ttf"].render("НАТИСНІТЬ ПРОБІЛ, ЩОБ ПРОПУСТИТИ", False, "white")
        title_rect = title_surf.get_rect()
        title_rect.centerx = pygame.display.get_window_size()[0]//2
        title_rect.centery = 500
        screen.blit(title_surf, title_rect)

    def draw(self, screen : pygame.surface.Surface, alpha : float) -> None:
        for sprite in self.world.all_sprites:
            sprite.draw(screen, alpha)
        self.draw_menu_items(screen)

