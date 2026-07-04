from __future__ import annotations
from typing import TYPE_CHECKING
from game_modules.namings import StateName
from game_modules.states.state import State
from game_modules.assets_loader import AssetsLoader
from game_modules.world import World
import pygame


class MainMenu(State):
    STARTING_MENU_PAGE : int = 0
    STARTING_MENU_ITEM : int = 0
    def __init__(self):
        super().__init__()
        self.world = World(state=StateName.MAIN_MENU)
        self.assets_loader = AssetsLoader()
        self.assets = self.assets_loader.assets
        self.menu_page_one : list[str] = ["ГРАТИ", "РІВНІ"] 
        self.menu_page_two : list[str] = ["СКІНИ", "ВИХІД"]
        self.menu_pages : list[list[str]] = [self.menu_page_one, self.menu_page_two]
        self.current_menu_page : int = MainMenu.STARTING_MENU_PAGE
        self.current_menu_item : int = MainMenu.STARTING_MENU_ITEM
        self.menu_items_colors : list[pygame.color.Color] = [pygame.color.Color(255, 85, 85),
                                                             pygame.color.Color(235, 135, 85)]
        self.menu_actions = [[self.start_game, self.enter_level_menu],
                             [self.enter_skin_menu, self.quit_game]]

    def start_game(self) -> None:
        self.quit = True
        if World.GAMEPLAY_LEVEL != 1:
            self.next_state = StateName.CUTSCENE
        else:
            self.next_state = StateName.GAMEPLAY

    def enter_level_menu(self) -> None:
        self.quit = True
        self.next_state = StateName.LEVEL_MENU

    def enter_skin_menu(self) -> None:
        self.quit = True
        self.next_state = StateName.SKINS_MENU

    def quit_game(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def menu_up(self) -> None:
        if self.current_menu_item == 0 and self.current_menu_page == 0:
            return
        elif self.current_menu_item == 1 and self.current_menu_page == 0:
            self.current_menu_item = 0
        elif self.current_menu_item == 0 and self.current_menu_page == 1:
            self.current_menu_item = 1
            self.current_menu_page = 0
        elif self.current_menu_item == 1 and self.current_menu_page == 1:
            self.current_menu_item = 0

    def menu_down(self) -> None:
        if self.current_menu_item == 1 and self.current_menu_page == 1:
            return
        elif self.current_menu_item == 0 and self.current_menu_page == 0:
            self.current_menu_item = 1
        elif self.current_menu_item == 1 and self.current_menu_page == 0:
            self.current_menu_item = 0
            self.current_menu_page = 1
        elif self.current_menu_item == 0 and self.current_menu_page == 1:
            self.current_menu_item = 1

    def handle_inputs(self, inputs : dict[pygame.event.Event, bool]) -> None:
        if inputs[pygame.K_UP]:
            self.menu_up()
        elif inputs[pygame.K_DOWN]:
            self.menu_down()
        elif inputs[pygame.K_SPACE]:
            self.menu_actions[self.current_menu_page][self.current_menu_item]()

    def fixed_update(self) -> None:
        for obj in self.world.dynamic_objects:
            obj.fixed_update()

    def update(self,dt : float) -> None:
        self.world.all_sprites.update(dt)
        MainMenu.STARTING_MENU_PAGE = self.current_menu_page
        MainMenu.STARTING_MENU_ITEM = self.current_menu_item

    def draw_menu_pages(self, screen : pygame.surface.Surface) -> None:
        menu_items = self.menu_pages[self.current_menu_page]

        for i, text in enumerate(menu_items):
            item_color = self.menu_items_colors[0] if i == self.current_menu_item else self.menu_items_colors[1]
            item_surf = self.assets["PressStart2P.ttf"].render(text, False, item_color)
            item_rect = item_surf.get_rect()
            item_rect.centerx = pygame.display.get_window_size()[0]//2
            item_rect.y = (320 + i*60) - i*item_rect.height
            screen.blit(item_surf, item_rect)

    def draw_menu_arrow(self, screen : pygame.surface.Surface) -> None:
        if self.current_menu_page == 0:
            arrow_image = self.assets["arrow_down.png"]
            arrow_centerx = pygame.display.get_window_size()[0]//2
            arrow_y = 410
        elif self.current_menu_page == 1:
            arrow_image = self.assets["arrow_up.png"]
            arrow_centerx = pygame.display.get_window_size()[0]//2
            arrow_y = 280
        arrow_rect =arrow_image.get_rect()
        arrow_rect.centerx = arrow_centerx
        arrow_rect.y = arrow_y
        screen.blit(arrow_image, arrow_rect)

    def draw(self, screen : pygame.surface.Surface, alpha : float) -> None:
        for sprite in self.world.all_sprites:
            sprite.draw(screen, alpha)
        self.draw_menu_pages(screen)
        self.draw_menu_arrow(screen)

