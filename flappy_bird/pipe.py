"""Pipe."""

import random

import pygame

from flappy_bird.settings import settings


class Pipe:
    """Class that implements a game pipe.

    Attributes:
        top_pipe: Top pipe image.
        bottom_pipe: Bottom pipe image.
        x: x-coordinate of pipe.
        top_pipe_height: Top pipe height.
        top_pipe_top_left: Top left corner of top pipe.
        bottom_pipe_top_left: Top left corner of bottom pipe.
        velocity: Moving speed of pipe.
        vertical_gap: Gap between pipes.
        width: Pipe image width.
        height: Pipe image height.
    """

    def __init__(self, x: int, top_pipe: pygame.Surface, bottom_pipe: pygame.Surface):
        self.top_pipe = top_pipe
        self.bottom_pipe = bottom_pipe
        self.x = x
        self.velocity = settings.PIPE_VELOCITY
        self.vertical_gap = settings.PIPE_VERTICAL_GAP
        self.width = top_pipe.get_width()
        self.height = top_pipe.get_height()
        self.top_pipe_height = random.randrange(settings.PIPE_TOP_MIN_HEIGHT, settings.PIPE_TOP_MAX_HEIGHT)
        self.top_pipe_top_left = self.top_pipe_height - self.height
        self.bottom_pipe_top_left = self.top_pipe_height + self.vertical_gap

    def move(self) -> None:
        """Moves the pipe."""
        self.x -= self.velocity

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the pipe."""
        screen.blit(self.top_pipe, (self.x, self.top_pipe_top_left))
        screen.blit(self.bottom_pipe, (self.x, self.bottom_pipe_top_left))

    def get_masks(self) -> pygame.mask.Mask:
        """Gets the masks of the pipes."""
        return pygame.mask.from_surface(self.top_pipe), pygame.mask.from_surface(self.bottom_pipe)
