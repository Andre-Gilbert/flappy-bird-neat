"""Flappy bird game."""

from typing import Any

import neat
import pygame

from flappy_bird.bird import Bird
from flappy_bird.floor import Floor
from flappy_bird.pipe import Pipe
from flappy_bird.settings import settings


class Game:
    """Class that implements the flappy bird game.

    Attributes:
        width: Screen width.
        height: Screen height.
        screen: pygame screen.
        font: Font.
        font: Font color.
        birds: Bird images.
        bottom_pipe: Bottom pipe image.
        top_pipe: Top pipe image.
        floor: Floor image.
        background: Background image.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
        font: pygame.font.Font,
        font_color: tuple[int, ...],
        birds: list[pygame.Surface],
        pipe: pygame.Surface,
        floor: pygame.Surface,
        background: pygame.Surface,
    ):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.font_color = font_color
        self.birds = birds
        self.bottom_pipe = pipe
        self.top_pipe = pygame.transform.flip(pipe, False, True)
        self.floor = floor
        self.background = background

    def check_collision(self, bird: Bird, pipe: Pipe, floor: Floor) -> bool:
        """Checks if the bird collided with terrain."""
        bird_mask = bird.get_mask()
        top_pipe_mask, bottom_pipe_mask = pipe.get_masks()

        top_pipe_offset = (round(pipe.x - bird.x), round(pipe.top_pipe_top_left - bird.y))
        bottom_pipe_offset = (round(pipe.x - bird.x), round(pipe.bottom_pipe_top_left - bird.y))

        return bool(
            bird_mask.overlap(top_pipe_mask, top_pipe_offset) is not None
            or bird_mask.overlap(bottom_pipe_mask, bottom_pipe_offset) is not None
            or bird.y + bird.get_height() > floor.y
            or bird.y < 0
        )

    def draw(
        self,
        birds: list[Bird],
        pipes: list[Pipe],
        floor: Floor,
        score: int,
        generation: int,
        game_time: float,
    ) -> None:
        """Draws the game."""
        self.screen.blit(self.background, (0, 0))

        # Draw moving floor
        floor.draw(self.screen)

        # Draw moving pipes
        for pipe in pipes:
            pipe.draw(self.screen)

        # Draw flapping birds
        for bird in birds:
            bird.draw(self.screen)

        # Render game updates
        game_time_text = self.font.render("Timer: " + str(game_time) + " s", 1, self.font_color)
        self.screen.blit(game_time_text, (self.width - 15 - game_time_text.get_width(), 15))

        score_text = self.font.render("Score: " + str(score), 1, self.font_color)
        self.screen.blit(score_text, (self.width - 15 - score_text.get_width(), 15 + game_time_text.get_height()))

        generation_text = self.font.render("Generation: " + str(generation - 1), 1, self.font_color)
        self.screen.blit(generation_text, (15, 15))

        bird_text = self.font.render("Birds alive: " + str(len(birds)), 1, self.font_color)
        self.screen.blit(bird_text, (15, 15 + generation_text.get_height()))

        pygame.display.update()

    def get_pipe_index(self, pipes: list[Pipe], birds: list[Bird]) -> int:
        """Gets the index of the pipe."""
        distances = [pipe.x + pipe.width - birds[0].x for pipe in pipes]
        index = distances.index(min(i for i in distances if i >= 0))
        return index

    def main(self, genomes_with_id: list[tuple], config: Any) -> None:
        """Runs the game."""
        generation = settings.GENERATION
        generation += 1
        score = 0
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        # Create floor, pipes, birds, genomes, and models
        floor = Floor(settings.FLOOR_STARTING_POSITION, self.floor)
        pipes = [
            Pipe(settings.PIPE_STARTING_POSITION + i * settings.PIPE_HORIZONTAL_GAP, self.top_pipe, self.bottom_pipe)
            for i in range(settings.PIPE_MAX_NUM)
        ]
        models = []
        genomes = []
        birds = []

        for _, genome in genomes_with_id:
            birds.append(Bird(settings.BIRD_STARTING_X_POSITION, settings.BIRD_STARTING_Y_POSITION, self.birds))
            genome.fitness = 0
            genomes.append(genome)
            model = neat.nn.FeedForwardNetwork.create(genome, config)
            models.append(model)

        # Game loop
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if score >= settings.MAX_SCORE or not birds:
                run = False
                break

            game_time = round((pygame.time.get_ticks() - start_time) / 1000, 2)
            clock.tick(settings.FPS)

            # Move floor, pipes
            floor.move()
            passed_pipes = []
            for pipe in pipes:
                pipe.move()
                if pipe.x + pipe.width < birds[0].x:
                    passed_pipes.append(pipe)

            # Score equals number of passed pipes
            score = len(passed_pipes)

            # Move bird, pass model input, and update fitness
            pipe_index = self.get_pipe_index(pipes, birds)
            for index, bird in enumerate(birds):
                bird.move()

                delta_x = bird.x - pipes[pipe_index].x
                delta_y_top = bird.y - pipes[pipe_index].top_pipe_height
                delta_y_bottom = bird.y - pipes[pipe_index].bottom_pipe_top_left

                output = models[index].activate((delta_x, delta_y_top, delta_y_bottom))

                # tanh activation function, output will be between -1 and 1
                # jump if output > 0.5
                if output[0] > settings.THRESHOLD_TO_JUMP:
                    bird.jump()

                bird_died = self.check_collision(bird, pipes[pipe_index], floor)
                genomes[index].fitness = game_time + score - bird_died * settings.PUNISHMENT
                if bird_died:
                    models.pop(index)
                    genomes.pop(index)
                    birds.pop(index)

            self.draw(birds, pipes, floor, score, generation, game_time)

        pygame.quit()
