from __future__ import annotations
import pygame, random


class GameGrid():
    def __init__(self):
        '''
        20x15 grid
        each cell " " is 40x40 tile on 800x600 grid 
        objects spawn on midbottom point of the cell(e.g. |10x|20y| for the topleft cell)
        x -> means objects can be spawn there 
        o -> normal objects cant be spawn there
        '''
        self.grid : list[list[str]] = [
            ["x","x","x","x","x","x","x","x","x","x","x","x","x","x","x","x","x","x","x","x"],
            ["x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"],
            ["x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"],
            ["x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"], # key cell is at |3y|17x| or midbottom [700x, 160y] 
            ["x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"],
            ["x","x","x","x","x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"],
            ["x","x","x","x","x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"],
            ["x","x","p","x","x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"], # player cell is at |7y|2x| or midbottom [100x, 320y] 
            ["x","x","x","x","x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"],
            ["x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"],
            ["x","x","x","x","x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"],
            ["x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"], # chest cell is at |11y|17x| or midbottom [700x, 480y] 
            ["x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"],
            ["x","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","o","x"],
            ["x","x","x","x","x","x","x","x","x","x","x","x","x","x","x","x","x","x","x","x"],
            ]
        self.cell_size = 40

    def get_normal_object_spawn_pos(self) -> pygame.Vector2:
        random_col_index = random.randint(0, len(self.grid)-1)
        random_col = self.grid[random_col_index]
        random_row : str | None = None
        while "o" not in random_col:
            random_col_index = random.randint(0, len(self.grid)-1)
            random_col = self.grid[random_col_index]
        while random_row != "o":
            random_row_index = random.randint(0, len(random_col)-1)
            random_row = random_col[random_row_index]
        self.grid[random_col_index][random_row_index] = "x"
        pos = pygame.Vector2(20 + random_row_index * 40, 40 + random_col_index * 40)
        return pos
    
    def get_late_object_spawn_pos(self) -> pygame.Vector2:
        random_col_index = random.randint(2, len(self.grid)-2)
        random_col = self.grid[random_col_index]
        random_row_index = random.randint(1, len(random_col)-2)
        random_row = random_col[random_row_index]
        pos = pygame.Vector2(20 + random_row_index * 40, 40 + random_col_index * 40)
        return pos

