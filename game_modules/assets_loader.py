from __future__ import annotations
from typing import TYPE_CHECKING, Union
from typing import Generator, Tuple
import pygame, os


def filepath_generator() -> Generator[Tuple[str, str]]:
    for dirpath, dirnames, filenames in os.walk("assets"):
        if dirnames:
            continue
        for file in filenames:
            path_to_file = os.path.join(dirpath, file)
            yield file, path_to_file

class AssetsLoader():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.assets : dict[str, Union[pygame.surface.Surface, pygame.mixer.Sound, str, pygame.font.Font]] = {}
            self.fonts_data : dict[str, int] = {"PressStart2P.ttf" : 20}
            self.assets_to_load : int = 0
            self.assets_loaded : int = 0
            self.all_loaded = False
            self.parse_folders()
            self.filepath_generator = filepath_generator()
            self._initialized = True

    def parse_folders(self) -> None:
        for dirpath, dirnames, filenames in os.walk("assets"):
            for file in filenames:
                if dirnames:
                    continue
                self.assets_to_load +=1

    def load_assets(self) -> None:
        if self.assets_loaded < self.assets_to_load:
            self.assets_loaded +=1
            file, path_to_file = next(self.filepath_generator)
            if file.endswith("ttf") : self.load_font(file, path_to_file)
            if file.endswith("png") : self.load_image(file, path_to_file)
            if file.endswith("mp3") : self.load_music(file, path_to_file)
            if file.endswith("wav") : self.load_sound(file, path_to_file)
        else:
            self.all_loaded = True       

    def load_font(self, font : str , path : str) -> None:
        for font_name, size in self.fonts_data.items():
            if font_name == font:
                loaded_font = pygame.font.Font(path, size)
                self.assets[font] = loaded_font

    def load_image(self, image : str , path : str) -> None:
        loaded_image = pygame.image.load(path)
        self.assets[image] = loaded_image

    def load_music(self, music : str , path : str) -> None:
        self.assets[music] = path

    def load_sound(self, sound : str , path : str) -> None:
        loaded_sound = pygame.mixer.Sound(path)
        loaded_sound.set_volume(0.6)
        self.assets[sound] = loaded_sound