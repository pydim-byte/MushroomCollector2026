from __future__ import annotations
from game_modules.objects.static_image import StaticImage
import pygame


class BossHud(StaticImage):
    def __init__(self, hud_image, full_heart : pygame.surface.Surface, empty_heart : pygame.surface.Surface, pos : pygame.Vector2, font : pygame.font.Font, player, boss):
        super().__init__(hud_image, pos)
        self.full_heart : pygame.surface.Surface = full_heart
        self.empty_heart : pygame.surface.Surface = empty_heart
        self.player = player
        self.boss = boss
        self.font : pygame.font.Font = font

    def draw(self, screen, aplha):
        super().draw(screen, aplha)
        for h in range(3):
            h_image = self.full_heart
            h_rect = h_image.get_rect()
            h_rect.left = 10 + (10 + h_rect.width) * h
            h_rect.centery = self.rect.centery
            screen.blit(h_image, h_rect)
        for h in range(3-self.player.hp):
            h_empty = h + 1
            h_image = self.empty_heart
            h_rect = h_image.get_rect()
            h_rect.left = 10 + (10 + h_rect.width) * (3 - h_empty)
            h_rect.centery = self.rect.centery
            screen.blit(h_image, h_rect)

        for h in range(3):
            h_image = self.full_heart
            h_rect = h_image.get_rect()
            h_rect.right = 800 - (10 + (10 + h_rect.width) * h)
            h_rect.centery = self.rect.centery
            screen.blit(h_image, h_rect)
        for h in range(3-self.boss.hp):
            h_empty = h + 1
            h_image = self.empty_heart
            h_rect = h_image.get_rect()
            h_rect.right = 800 - (10 + (10 + h_rect.width) * (3 - h_empty))
            h_rect.centery = self.rect.centery
            screen.blit(h_image, h_rect)


