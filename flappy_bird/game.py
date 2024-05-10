"""Flappy bird game."""

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
        width: int,
        height: int,
        screen: pygame.Surface,
        font: pygame.font.Font,
        font_color: tuple[int, ...],
        birds: list[pygame.Surface],
        pipe: pygame.Surface,
        floor: pygame.Surface,
        background: pygame.Surface,
    ):
        self.width = width
        self.height = height
        self.screen = screen
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

    def draw(self, birds, pipes, floor, score, generation, game_time):
        self.screen.blit(self.background, (0, 0))
        floor.draw(self.screen)
        for pipe in pipes:
            pipe.draw(self.screen)
        for bird in birds:
            bird.draw(self.screen)

        score_text = self.font.render("Score: " + str(score), 1, self.font_color)
        self.screen.blit(score_text, (self.width - 15 - score_text.get_width(), 15))

        game_time_text = self.font.render("Timer: " + str(game_time) + " s", 1, self.font_color)
        self.screen.blit(game_time_text, (self.width - 15 - game_time_text.get_width(), 15 + score_text.get_height()))

        generation_text = self.font.render("Generation: " + str(generation - 1), 1, self.font_color)
        self.screen.blit(generation_text, (15, 15))

        bird_text = self.font.render("Birds Alive: " + str(len(birds)), 1, self.font_color)
        self.screen.blit(bird_text, (15, 15 + generation_text.get_height()))

        progress_text = self.font.render("Pipes Remained: " + str(len(pipes) - score), 1, self.font_color)
        self.screen.blit(progress_text, (15, 15 + generation_text.get_height() + bird_text.get_height()))

        pygame.display.update()

    def get_index(self, pipes, birds):

        bird_x = birds[0].x

        list_distance = [pipe.x + pipe.width - bird_x for pipe in pipes]

        index = list_distance.index(min(i for i in list_distance if i >= 0))
        return index

    def main(self, genomes, config):
        generation = settings.GENERATION
        generation += 1

        score = 0
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        floor = Floor(settings.FLOOR_STARTING_POSITION, self.floor)
        pipes = [
            Pipe(settings.PIPE_STARTING_POSITION + i * settings.PIPE_HORIZONTAL_GAP, self.top_pipe, self.bottom_pipe)
            for i in range(settings.PIPE_MAX_NUM)
        ]
        models = []
        genomes_list = []
        birds = []

        for _, genome in genomes:
            birds.append(Bird(settings.BIRD_STARTING_X_POSITION, settings.BIRD_STARTING_Y_POSITION, self.birds))
            genome.fitness = 0
            genomes_list.append(genome)
            model = neat.nn.FeedForwardNetwork.create(genome, config)
            models.append(model)

        run = True

        while run is True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if score >= settings.MAX_SCORE or not birds:
                run = False
                break

            game_time = round((pygame.time.get_ticks() - start_time) / 1000, 2)

            clock.tick(settings.FPS)

            floor.move()

            pipe_input_index = self.get_index(pipes, birds)

            passed_pipes = []
            for pipe in pipes:
                pipe.move()
                if pipe.x + pipe.width < birds[0].x:
                    passed_pipes.append(pipe)

            score = len(passed_pipes)

            for index, bird in enumerate(birds):
                bird.move()
                delta_x = bird.x - pipes[pipe_input_index].x
                delta_y_top = bird.y - pipes[pipe_input_index].top_pipe_height
                delta_y_bottom = bird.y - pipes[pipe_input_index].bottom_pipe_top_left
                net_input = (delta_x, delta_y_top, delta_y_bottom)
                output = models[index].activate(net_input)

                if output[0] > settings.THRESHOLD_TO_JUMP:
                    bird.jump()

                bird_failed = self.check_collision(bird, pipes[pipe_input_index], floor)

                genomes_list[index].fitness = game_time + score - bird_failed * settings.FAILED_PUNISHMENT

                if bird_failed:
                    models.pop(index)
                    genomes_list.pop(index)
                    birds.pop(index)

            self.draw(birds, pipes, floor, score, generation, game_time)

        pygame.quit()
