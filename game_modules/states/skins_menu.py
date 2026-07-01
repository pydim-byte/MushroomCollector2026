from __future__ import annotations
from typing import TYPE_CHECKING
from game_modules.namings import StateName
from game_modules.states.state import State
from game_modules.assets_loader import AssetsLoader
from game_modules.world import World
import pygame


class SkinsMenu(State):
    def __init__(self):
        super().__init__()
        self.world = World(state=StateName.SKINS_MENU)
        self.assets_loader = AssetsLoader()
        self.assets = self.assets_loader.assets
        self.menu_items : list[str] = ["ДАЛІ", "ВИБРАТИ", "МЕНЮ"] 
        self.current_menu_item : int = 0
        self.menu_items_colors : list[pygame.color.Color] = [pygame.color.Color(200, 85, 85),
                                                             pygame.color.Color(80, 80, 80)] 
        self.menu_actions = [self.next_skin, self.choose_skin, self.quit_menu]

    def next_skin(self) -> None:
        pass

    def choose_skin(self) -> None:
        pass

    def quit_menu(self) -> None:
        self.quit = True
        self.next_state = StateName.MAIN_MENU

    def menu_up(self) -> None:
        if self.current_menu_item == 0:
            return
        self.current_menu_item -=1

    def menu_down(self) -> None:
        if self.current_menu_item == 2:
            return
        self.current_menu_item +=1

    def handle_inputs(self, inputs : dict[pygame.event.Event, bool]) -> None:
        if inputs[pygame.K_UP]:
            self.menu_up()
        elif inputs[pygame.K_DOWN]:
            self.menu_down()
        elif inputs[pygame.K_SPACE]:
            self.menu_actions[self.current_menu_item]()

    def fixed_update(self) -> None:
        for obj in self.world.dynamic_objects:
            obj.fixed_update()

    def update(self,dt : float) -> None:
        self.world.all_sprites.update(dt)

    def draw_menu_pages(self, screen : pygame.surface.Surface) -> None:
        for i, text in enumerate(self.menu_items):
            item_color = self.menu_items_colors[0] if i == self.current_menu_item else self.menu_items_colors[1]
            item_surf = self.assets["PressStart2P.ttf"].render(text, False, item_color)
            item_rect = item_surf.get_rect()
            item_rect.centerx = pygame.display.get_window_size()[0]//2
            item_rect.y = (320 + i*60) - i*item_rect.height
            screen.blit(item_surf, item_rect)

    def draw(self, screen : pygame.surface.Surface, alpha : float) -> None:
        for sprite in self.world.all_sprites:
            sprite.draw(screen, alpha)
        self.draw_menu_pages(screen)

