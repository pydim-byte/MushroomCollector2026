import pygame


class Barrier:
    def __init__(self,x : int, y : int, width : int, height : int):
        self.type : str = 'barrier'
        self.rect = pygame.Rect(x,y,width,height)

    def alive(self) -> bool:
        return True