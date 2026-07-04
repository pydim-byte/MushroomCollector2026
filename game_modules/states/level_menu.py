from __future__ import annotations
from typing import TYPE_CHECKING
from game_modules.namings import StateName
from game_modules.states.state import State
from game_modules.assets_loader import AssetsLoader
from game_modules.world import World
import pygame


class LevelMenu(State):
    def __init__(self):
        super().__init__()
        self.world = World(state=StateName.LEVEL_MENU)
        self.assets_loader = AssetsLoader()
        self.assets = self.assets_loader.assets
        self.levels : list[int] = [i for i in range(1, 11)]
        self.selected : int = 1
        self.level_color : list[pygame.color.Color] = [pygame.color.Color(255, 85, 85),
                                                             pygame.color.Color(235, 135, 85)]
        self.actions = [self.play_selected_level if i != 10 else self.quit_menu for i in self.levels]

    def play_selected_level(self) -> None:
        self.quit = True
        World.GAMEPLAY_LEVEL = self.selected
        if World.GAMEPLAY_LEVEL != 1:
            self.next_state = StateName.CUTSCENE
        else:
            self.next_state = StateName.GAMEPLAY

    def quit_menu(self) -> None:
        self.quit = True
        self.next_state = StateName.MAIN_MENU

    def menu_up(self) -> None:
        if self.selected == 1:
            return
        self.selected -= 1

    def menu_down(self) -> None:
        if self.selected == 10:
            return
        self.selected += 1

    def handle_inputs(self, inputs : dict[pygame.event.Event, bool]) -> None:
        if inputs[pygame.K_UP]:
            self.menu_up()
        elif inputs[pygame.K_DOWN]:
            self.menu_down()
        elif inputs[pygame.K_SPACE]:
            self.actions[self.selected-1]()

    def fixed_update(self) -> None:
        for obj in self.world.dynamic_objects:
            obj.fixed_update()

    def update(self,dt : float) -> None:
        self.world.all_sprites.update(dt)

    def draw_levels(self, screen : pygame.surface.Surface) -> None:
        for i, level in enumerate(self.levels):
            level_color = self.level_color[0] if level == self.selected else self.level_color[1]
            level_text = f"РІВЕНЬ {level}" if level != 10 else "МЕНЮ"
            level_surf = self.assets["PressStart2P.ttf"].render(level_text, False, level_color)
            level_rect = level_surf.get_rect()
            level_rect.centerx = pygame.display.get_window_size()[0]//2
            level_rect.y = 200 + i*40
            screen.blit(level_surf, level_rect)

    def draw(self, screen : pygame.surface.Surface, alpha : float) -> None:
        for sprite in self.world.all_sprites:
            sprite.draw(screen, alpha)
        self.draw_levels(screen)

