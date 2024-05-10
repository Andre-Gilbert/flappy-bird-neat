"""Bird."""

import pygame

from flappy_bird.settings import settings


class Bird:
    """Class that implements a bird."""

    def __init__(self, x: int, y: int, birds: list[pygame.Surface]):
        self.birds = birds
        self.bird = birds[0]
        self.x = x
        self.y = y
        self.fly_angle = 0
        self.time = 0
        self.velocity = 0
        self.animation_time_count = 0

    def move(self) -> None:
        """Moves the bird."""
        self.time += 1
        displacement = self.velocity * self.time + (1 / 2) * settings.BIRD_ACCELERATION * self.time**2
        displacement = min(displacement, settings.BIRD_MAX_DISPLACEMENT)
        self.y = self.y + displacement
        if displacement < 0:
            if self.fly_angle < settings.BIRD_MAX_UP_ANGLE:
                self.fly_angle += max(
                    settings.BIRD_ANGULAR_ACCELERATION * (settings.BIRD_MAX_UP_ANGLE - self.fly_angle),
                    settings.BIRD_MIN_INCREMENTAL_ANGLE,
                )
            else:
                self.fly_angle = settings.BIRD_MAX_UP_ANGLE
        else:
            if self.fly_angle > settings.BIRD_MAX_DOWN_ANGLE:
                self.fly_angle -= abs(
                    min(
                        settings.BIRD_ANGULAR_ACCELERATION * (settings.BIRD_MAX_DOWN_ANGLE - self.fly_angle),
                        -settings.BIRD_MIN_INCREMENTAL_ANGLE,
                    )
                )
            else:
                self.fly_angle = settings.BIRD_MAX_DOWN_ANGLE

    def jump(self) -> None:
        """Makes the bird jump."""
        self.velocity = settings.BIRD_JUMP_VELOCITY
        self.time = 0

    def animation(self) -> tuple:
        """Animates the bird."""
        self.animation_time_count += 1
        if self.fly_angle < -45:
            self.bird = self.birds[0]
            self.animation_time_count = 0
        elif self.animation_time_count < settings.BIRD_ANIMATION_TIME:
            self.bird = self.birds[0]
        elif self.animation_time_count < settings.BIRD_ANIMATION_TIME * 2:
            self.bird = self.birds[1]
        elif self.animation_time_count < settings.BIRD_ANIMATION_TIME * 3:
            self.bird = self.birds[2]
        elif self.animation_time_count < settings.BIRD_ANIMATION_TIME * 4:
            self.bird = self.birds[1]
        else:
            self.bird = self.birds[0]
            self.animation_time_count = 0

        rotated_image = pygame.transform.rotate(self.bird, self.fly_angle)
        origin_img_center = self.bird.get_rect(topleft=(self.x, self.y)).center
        rotated_rect = rotated_image.get_rect(center=origin_img_center)
        return rotated_image, rotated_rect
