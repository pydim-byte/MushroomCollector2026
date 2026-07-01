from __future__ import annotations
from typing import TYPE_CHECKING, Dict
import pygame, sys
from game_modules.globals import GameScreen, GameUpdate
from game_modules.assets_loader import AssetsLoader
from game_modules.namings import StateName
from game_modules.states.state import State
from game_modules.states.main_menu import MainMenu
from game_modules.states.level_menu import LevelMenu
from game_modules.states.skins_menu import SkinsMenu
from game_modules.states.gameplay import Gameplay
from game_modules.states.level_complete import LevelComplete
from game_modules.states.game_over import GameOver


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.Surface((GameScreen.SCREEN_WIDTH,GameScreen.SCREEN_HEIGHT))
        self.display = pygame.display.set_mode((GameScreen.DISPLAY_WIDTH,GameScreen.DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()
        self.inputs = {pygame.K_LEFT : False, pygame.K_RIGHT : False, pygame.K_UP : False, pygame.K_DOWN : False, pygame.K_r : False, pygame.K_SPACE : False, pygame.K_ESCAPE : False}
        self.held_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

        self.assets_loader = AssetsLoader()
        pygame.mixer.music.load(self.assets_loader.assets["yoshi.mp3"])
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        self.states : dict[StateName, State] = {StateName.MAIN_MENU : MainMenu,
                                                StateName.GAMEPLAY : Gameplay,
                                                StateName.LEVEL_MENU : LevelMenu,
                                                StateName.SKINS_MENU : SkinsMenu,
                                                StateName.LEVEL_COMPLETE : LevelComplete,
                                                StateName.GAME_OVER : GameOver}
        self.state : State = MainMenu()

    def handle_events(self, event : pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type in [pygame.KEYUP, pygame.KEYDOWN]:
            self.handle_key_events(event) 

    def handle_key_events(self, event : pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            for inpput_key in self.inputs:
                if event.key == inpput_key:
                    self.inputs[inpput_key] = True

        if event.type == pygame.KEYUP:
            for inpput_key in self.inputs:
                if event.key == inpput_key:
                    self.inputs[inpput_key] = False

    def handle_inputs(self) -> None:
        self.state.handle_inputs(self.inputs)
        if not isinstance(self.state, Gameplay):
            for k in self.inputs:
                self.inputs[k] = False
        else:
            for k in self.inputs:
                if k not in self.held_keys:
                    self.inputs[k] = False

    def flip_state(self) -> None:
        for k in self.inputs: self.inputs[k] = False
        self.state = self.states[self.state.next_state]()

    def fixed_update(self) -> None:
        self.state.fixed_update()

    def update(self,dt : float) -> None:
        self.state.update(dt)
        if self.state.quit:
            self.flip_state()

    def draw(self, alpha : float) -> None:
        self.screen.fill("black")
        self.state.draw(self.screen, alpha)
        self.display.blit(pygame.transform.scale(self.screen,self.display.get_size()),(0,0))
        pygame.display.flip()

    def run(self) -> None:
        accumulator = 0
        while True:
            dt = self.clock.tick(GameUpdate.FPS) / 1000
            dt = min(dt,0.1)
            accumulator += dt

            while accumulator >= dt:
                for event in pygame.event.get() : self.handle_events(event)
                self.handle_inputs()
                self.fixed_update()
                accumulator -= 1/GameUpdate.FIXED_TPS

            alpha = accumulator / dt

            self.update(dt)
            self.draw(alpha)

game = Game()
game.run()