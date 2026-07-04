from __future__ import annotations
from typing import TYPE_CHECKING
from game_modules.namings import StateName
from game_modules.states.state import State
from game_modules.assets_loader import AssetsLoader
from game_modules.world import World
import pygame


class LoadingScreen(State):
    def __init__(self):
        super().__init__()
        self.assets_loader = AssetsLoader()

    def update(self,dt : float) -> None:
        if self.assets_loader.assets_loaded == self.assets_loader.assets_to_load:
            self.quit = True
            self.next_state = StateName.MAIN_MENU

    def draw_loading_bar(self, screen : pygame.surface.Surface) -> None:
        outline_rect = pygame.Rect(0, 0, 612, 40)
        outline_rect.centerx = 800//2
        outline_rect.centery = (600//2)
        pygame.draw.rect(screen, "black", outline_rect, width=4)

        loading_rect = pygame.Rect(0, 0, ((outline_rect.width - 8)//self.assets_loader.assets_to_load * self.assets_loader.assets_loaded), outline_rect.height - 12)
        loading_rect.left = outline_rect.left + 6
        loading_rect.centery = outline_rect.centery
        pygame.draw.rect(screen, "black", loading_rect)

    def draw(self, screen : pygame.surface.Surface, alpha : float) -> None:
        self.draw_loading_bar(screen)