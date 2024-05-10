"""Floor."""

import pygame

from flappy_bird.settings import settings


class Floor:
    """Class that implements the game floor.

    Attributes:
        floors: Floor images.
        width: Width of floor
        x1: x-coordinate of first floor.
        x2: x-coordinate of second floor.
        x3: x-coordinate of third floor.
        y: y-coordinate of floor.
    """

    def __init__(self, y: int, floor: pygame.Surface):
        self.floors = [floor] * 3
        self.width = floor.get_width()
        self.x1 = 0
        self.x2 = self.width
        self.x3 = self.width * 2
        self.y = y

    def move(self) -> None:
        """Moves the game floor."""
        self.x1 -= settings.FLOOR_VELOCITY
        self.x2 -= settings.FLOOR_VELOCITY
        self.x3 -= settings.FLOOR_VELOCITY
        if self.x1 + self.width < 0:
            self.x1 = self.x3 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width
        if self.x3 + self.width < 0:
            self.x3 = self.x2 + self.width

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the floor of the game."""
        screen.blit(self.floors[0], (self.x1, self.y))
        screen.blit(self.floors[1], (self.x2, self.y))
        screen.blit(self.floors[2], (self.x3, self.y))
