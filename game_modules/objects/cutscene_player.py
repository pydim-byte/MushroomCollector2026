from __future__ import annotations
from game_modules.objects.static_image import StaticImage
import pygame


class CutscenePlayer(StaticImage):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2, frame_duration : float):
        super().__init__(image, pos)
        
        self.frame_amount : int = self.rect.width // 800
        self.current_frame : int = 0

        self.frame_time : float = 0
        self.frame_duration : float = frame_duration

    def update(self, dt : float) -> None:
        self.frame_time += dt
        if self.frame_time >= self.frame_duration:
            self.current_frame += 1
            self.current_frame %= self.frame_amount-1
            self.frame_time -= self.frame_duration

    def draw(self, screen : pygame.surface.Surface, aplha : float) -> None:

        draw_rect = pygame.Rect(self.current_frame * 800, 0, 800, 600)
        draw_image = self.image.subsurface(draw_rect)
        screen.blit(draw_image, self.rect)

