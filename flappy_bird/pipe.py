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
        self.velocity = settings.PIPE_VELOCITY
        self.vertical_gap = settings.PIPE_VERTICAL_GAP
        self.width = top_pipe.get_width()
        self.height = top_pipe.get_height()
        self.random_height()

    def move(self) -> None:
        """Moves the pipe."""
        self.x -= self.velocity

    def random_height(self) -> None:
        """Generates the height of the pipe randomly."""
        self.top_pipe_height = random.randrange(settings.PIPE_TOP_MIN_HEIGHT, settings.PIPE_TOP_MAX_HEIGHT)
        self.top_pipe_top_left = self.top_pipe_height - self.height
        self.bottom_pipe_top_left = self.top_pipe_height + self.vertical_gap
