from __future__ import annotations
from typing import Callable
import pygame


class ObjectClock():
    def __init__(self, duration : float, action : Callable):
        self.current_time : float = 0.0
        self.duration : float = duration
        self.action : Callable = action

    def update(self, dt : float) -> None:
        self.current_time += dt
        if self.current_time >= self.duration:
            self.action()
            self.current_time = 0