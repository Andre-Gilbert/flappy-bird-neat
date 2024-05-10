"""Flappy bird game."""

import neat
import pygame

from flappy_bird.bird import Bird
from flappy_bird.floor import Floor
from flappy_bird.pipe import Pipe
from flappy_bird.settings import settings


class Game:
    """Class that implements the flappy bird game."""

    def __init__(self, width, height, screen, font, font_color, birds, bottom_pipe, top_pipe, floor, background):
        self.width = width
        self.height = height
        self.screen = screen
        self.font = font
        self.font_color = font_color
        self.birds = birds
        self.bottom_pipe = bottom_pipe
        self.top_pipe = top_pipe
        self.floor = floor
        self.background = background

    def check_collision(self, bird: Bird, pipe: Pipe, floor: Floor) -> bool:
        bird_mask = pygame.mask.from_surface(bird.bird)
        top_pipe_mask = pygame.mask.from_surface(pipe.top_pipe)
        bottom_pipe_mask = pygame.mask.from_surface(pipe.bottom_pipe)

        sky_height = 0
        floor_height = floor.y
        bird_lower_end = bird.y + bird.bird.get_height()

        top_pipe_offset = (round(pipe.x - bird.x), round(pipe.top_pipe_top_left - bird.y))
        bottom_pipe_offset = (round(pipe.x - bird.x), round(pipe.bottom_pipe_top_left - bird.y))

        top_pipe_intersection_point = bird_mask.overlap(top_pipe_mask, top_pipe_offset)
        bottom_pipe_intersection_point = bird_mask.overlap(bottom_pipe_mask, bottom_pipe_offset)

        return bool(
            top_pipe_intersection_point is not None
            or bottom_pipe_intersection_point is not None
            or bird_lower_end > floor_height
            or bird.y < sky_height
        )

    def draw(self, screen, birds, pipes, floor, score, generation, game_time):
        screen.blit(self.background, (0, 0))

        screen.blit(floor.floors[0], (floor.x1, floor.y))
        screen.blit(floor.floors[1], (floor.x2, floor.y))
        screen.blit(floor.floors[2], (floor.x3, floor.y))

        for pipe in pipes:
            screen.blit(pipe.top_pipe, (pipe.x, pipe.top_pipe_top_left))
            screen.blit(pipe.bottom_pipe, (pipe.x, pipe.bottom_pipe_top_left))

        for bird in birds:
            rotated_image, rotated_rect = bird.animation()
            screen.blit(rotated_image, rotated_rect)

        score_text = self.font.render("Score: " + str(score), 1, self.font_color)
        screen.blit(score_text, (self.width - 15 - score_text.get_width(), 15))

        game_time_text = self.font.render("Timer: " + str(game_time) + " s", 1, self.font_color)
        screen.blit(game_time_text, (self.width - 15 - game_time_text.get_width(), 15 + score_text.get_height()))

        generation_text = self.font.render("Generation: " + str(generation - 1), 1, self.font_color)
        screen.blit(generation_text, (15, 15))

        bird_text = self.font.render("Birds Alive: " + str(len(birds)), 1, self.font_color)
        screen.blit(bird_text, (15, 15 + generation_text.get_height()))

        progress_text = self.font.render("Pipes Remained: " + str(len(pipes) - score), 1, self.font_color)
        screen.blit(progress_text, (15, 15 + generation_text.get_height() + bird_text.get_height()))
        pygame.display.update()

    def get_index(self, pipes, birds):

        bird_x = birds[0].x

        list_distance = [pipe.x + pipe.width - bird_x for pipe in pipes]

        index = list_distance.index(min(i for i in list_distance if i >= 0))
        return index

    def main(self, genomes, config):
        generation = settings.GENERATION
        screen = self.screen
        generation += 1

        score = 0
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        floor = Floor(settings.FLOOR_STARTING_POSITION, self.floor)
        pipes_list = [
            Pipe(settings.PIPE_STARTING_POSITION + i * settings.PIPE_HORIZONTAL_GAP, self.top_pipe, self.bottom_pipe)
            for i in range(settings.PIPE_MAX_NUM)
        ]

        models_list = []
        genomes_list = []
        birds_list = []

        for _, genome in genomes:
            birds_list.append(Bird(settings.BIRD_STARTING_X_POSITION, settings.BIRD_STARTING_Y_POSITION, self.birds))
            genome.fitness = 0
            genomes_list.append(genome)
            model = neat.nn.FeedForwardNetwork.create(genome, config)
            models_list.append(model)

        run = True

        while run is True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if score >= settings.MAX_SCORE or not birds_list:
                run = False
                break

            game_time = round((pygame.time.get_ticks() - start_time) / 1000, 2)

            clock.tick(settings.FPS)

            floor.move()

            pipe_input_index = self.get_index(pipes_list, birds_list)

            passed_pipes = []
            for pipe in pipes_list:
                pipe.move()
                if pipe.x + pipe.width < birds_list[0].x:
                    passed_pipes.append(pipe)

            score = len(passed_pipes)

            for index, bird in enumerate(birds_list):
                bird.move()
                delta_x = bird.x - pipes_list[pipe_input_index].x
                delta_y_top = bird.y - pipes_list[pipe_input_index].top_pipe_height
                delta_y_bottom = bird.y - pipes_list[pipe_input_index].bottom_pipe_top_left
                net_input = (delta_x, delta_y_top, delta_y_bottom)
                output = models_list[index].activate(net_input)

                if output[0] > settings.THRESHOLD_TO_JUMP:
                    bird.jump()

                bird_failed = self.check_collision(bird, pipes_list[pipe_input_index], floor)

                genomes_list[index].fitness = game_time + score - bird_failed * settings.FAILED_PUNISHMENT

                if bird_failed:
                    models_list.pop(index)
                    genomes_list.pop(index)
                    birds_list.pop(index)

            self.draw(screen, birds_list, pipes_list, floor, score, generation, game_time)
        pygame.quit()
