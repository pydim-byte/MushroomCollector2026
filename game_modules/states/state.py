from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..namings import StateName
import pygame


class State():
    def __init__(self):
        self.quit : bool = False
        self.next_state : StateName = None

    def handle_inputs(self, inputs : dict[pygame.event.Event, bool]) -> None:
        pass

    def fixed_update(self) -> None:
        pass

    def update(self,dt : float) -> None:
        pass

    def draw(self, screen : pygame.surface.Surface, alpha : float) -> None:
        pass