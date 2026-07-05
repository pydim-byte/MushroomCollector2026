from __future__ import annotations
from typing import TYPE_CHECKING
from game_modules.globals import SkinsUnlocks
from game_modules.namings import StateName
from game_modules.states.state import State
from game_modules.assets_loader import AssetsLoader
from game_modules.world import World
import pygame


class Shop(State):
    def __init__(self):
        super().__init__()
        self.world = World(state=StateName.LEVEL_COMPLETE)
        self.assets_loader = AssetsLoader()
        self.assets = self.assets_loader.assets
        self.menu_items : list[str] = ["ЗВІЛЬНИТИ (120 ГРИБІВ)", "ПРОПУСТИТИ"]
        self.current_menu_item : int = 0
        self.colors : list[pygame.color.Color] = [pygame.color.Color(255,255,255),
                                                       pygame.color.Color(150, 150, 150)]
        self.actions = [self.next_level ,self.quit_menu]

    def next_level(self) -> None:
        self.quit = True
        self.next_state = StateName.LEVEL_COMPLETE
        self.next_state = StateName.NEW_SKIN
        World.TOTAL_MUSHROOMS_COLLECTED -= 120

    def quit_menu(self) -> None:
        self.quit = True
        self.next_state = StateName.LEVEL_COMPLETE

    def menu_up(self) -> None:
        if self.current_menu_item == 0:
            return
        self.current_menu_item -= 1

    def menu_down(self) -> None:
        if self.current_menu_item == 1:
            return
        self.current_menu_item += 1

    def handle_inputs(self, inputs : dict[pygame.event.Event, bool]) -> None:
        if inputs[pygame.K_UP]:
            self.menu_up()
        elif inputs[pygame.K_DOWN]:
            self.menu_down()
        elif inputs[pygame.K_SPACE]:
            self.actions[self.current_menu_item]()

    def fixed_update(self) -> None:
        for obj in self.world.dynamic_objects:
            obj.fixed_update()

    def update(self,dt : float) -> None:
        self.world.all_sprites.update(dt)

    def draw_menu_items(self, screen : pygame.surface.Surface) -> None:
        for i, item in enumerate(self.menu_items):
            item_color = self.colors[0] if i == self.current_menu_item else self.colors[1]
            item_text = item
            item_surf = self.assets["PressStart2P.ttf"].render(item_text, False, item_color)
            item_rect = item_surf.get_rect()
            item_rect.centerx = pygame.display.get_window_size()[0]//2
            item_rect.centery = 250 + i*100
            screen.blit(item_surf, item_rect)

        cage_surf = self.assets["cage.png"]
        cage_rect = cage_surf.get_rect()
        cage_rect.centerx = pygame.display.get_window_size()[0]//2
        cage_rect.centery = 150
        screen.blit(cage_surf, cage_rect)

    def draw(self, screen : pygame.surface.Surface, alpha : float) -> None:
        for sprite in self.world.all_sprites:
            sprite.draw(screen, alpha)
        self.draw_menu_items(screen)

