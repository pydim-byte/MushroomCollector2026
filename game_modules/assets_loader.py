from __future__ import annotations
from typing import TYPE_CHECKING, Union
import pygame, os


class AssetsLoader():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.assets : dict[str, Union[pygame.surface.Surface, pygame.mixer.Sound, str, pygame.font.Font]] = {}
        self.fonts_data : dict[str, int] = {"PressStart2P.ttf" : 20}
        self.load_assets()

    def load_assets(self) -> None:
        for dirpath, dirnames, filenames in os.walk("assets"):
            if dirnames:
                continue
            for file in filenames:
                path_to_file = os.path.join(dirpath, file)
                if file.endswith("ttf") : self.load_font(file, path_to_file)
                if file.endswith("png") : self.load_image(file, path_to_file)
                if file.endswith("mp3") : self.load_music(file, path_to_file)
                if file.endswith("wav") : self.load_sound(file, path_to_file)
                

    def load_font(self, font : str , path : str) -> None:
        for font_name, size in self.fonts_data.items():
            if font_name == font:
                loaded_font = pygame.font.Font(path, size)
                self.assets[font] = loaded_font

    def load_image(self, image : str , path : str) -> None:
        loaded_image = pygame.image.load(path).convert_alpha()
        self.assets[image] = loaded_image

    def load_music(self, music : str , path : str) -> None:
        self.assets[music] = path

    def load_sound(self, sound : str , path : str) -> None:
        loaded_sound = pygame.mixer.Sound(path)
        loaded_sound.set_volume(0.6)
        self.assets[sound] = loaded_sound