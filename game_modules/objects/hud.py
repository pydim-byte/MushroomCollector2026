from __future__ import annotations
from game_modules.objects.static_image import StaticImage
import pygame


class Hud(StaticImage):
    def __init__(self, image : pygame.surface.Surface, pos : pygame.Vector2, font : pygame.font.Font):
        super().__init__(image, pos)
        self.font : pygame.font.Font = font
        self.level : int = 0
        self.collected_mushrooms : int = 0
        self.total_mushrooms : int = 20

    def draw_level_text(self, screen : pygame.surface.Surface) -> None:
        level_text = f"РІВЕНЬ:{self.level}"
        level_text_surf = self.font.render(level_text, True, "white")
        level_text_rect = level_text_surf.get_rect()
        level_text_rect.left = self.rect.left + 10
        level_text_rect.centery = self.rect.centery
        screen.blit(level_text_surf, level_text_rect)

    def draw_mushrooms_text(self, screen : pygame.surface.Surface) -> None:
        level_text = f"ГРИБІВ ЗІБРАНО:{self.collected_mushrooms}/{self.total_mushrooms}"
        level_text_surf = self.font.render(level_text, True, "white")
        level_text_rect = level_text_surf.get_rect()
        level_text_rect.right = self.rect.right - 10
        level_text_rect.centery = self.rect.centery
        screen.blit(level_text_surf, level_text_rect)

    def draw(self, screen : pygame.surface.Surface, aplha : float) -> None:
        super().draw(screen, aplha)
        self.draw_level_text(screen)
        self.draw_mushrooms_text(screen)

