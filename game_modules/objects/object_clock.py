from __future__ import annotations
from typing import Callable
import pygame


class ObjectClock():
    def __init__(self, duration : float, action : Callable):
        self.current_time : float = 0.0
        self.duration : float = duration
        self.action : Callable = action
        self.max_spawn = None
        self.spawned = 0

    def update(self, dt : float) -> None:
        self.current_time += dt
        if self.current_time >= self.duration:
            self.current_time = 0
            self.spawned += 1
            if self.max_spawn and self.spawned <= self.max_spawn:
                self.action()
            elif self.max_spawn is None:
                self.action()