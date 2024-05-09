"""Pipe."""

import random

import pygame

from flappy_bird.settings import settings


class Pipe:
    """Class that implements a game pipe."""

    def __init__(self, x: int, top_pipe: pygame.Surface, bottom_pipe: pygame.Surface):
        self.top_pipe = top_pipe
        self.bottom_pipe = bottom_pipe
        self.x = x
        self.top_pipe_height = 0
        self.top_pipe_top_left = 0
        self.bottom_pipe_top_left = 0
        self._velocity = settings.PIPE_VELOCITY
        self._vertical_gap = settings.PIPE_VERTICAL_GAP
        self._width = top_pipe.get_width()
        self._height = top_pipe.get_height()
        self.random_height()

    def move(self) -> None:
        self.x -= self._velocity

    def random_height(self) -> None:
        self.top_pipe_height = random.randrange(settings.PIPE_TOP_MIN_HEIGHT, settings.PIPE_TOP_MAX_HEIGHT)
        self.top_pipe_top_left = self.top_pipe_height - self._height
        self.bottom_pipe_top_left = self.top_pipe_height + self._vertical_gap
