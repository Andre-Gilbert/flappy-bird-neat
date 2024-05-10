"""Game entrypoint."""

import neat
import pygame

from flappy_bird.game import Game
from flappy_bird.neat import draw_net, plot_species, plot_stats
from flappy_bird.settings import settings

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FONT = pygame.font.SysFont("comicsansms", 20)
FONT_COLOR = (255, 255, 255)

BIRDS = [
    pygame.image.load("./assets/bird-mid-flap.png"),
    pygame.image.load("./assets/bird-up-flap.png"),
    pygame.image.load("./assets/bird-down-flap.png"),
]

BOTTOM_PIPE = pygame.image.load("./assets/pipe.png")
TOP_PIPE = pygame.transform.flip(BOTTOM_PIPE, False, True)
FLOOR = pygame.image.load("./assets/floor.png")
BACKGROUND = pygame.transform.scale(pygame.image.load("./assets/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))


def main(config_file: str) -> None:
    """Runs flappy bird with NEAT."""
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )
    population = neat.population.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    game = Game(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        screen=SCREEN,
        font=FONT,
        font_color=FONT_COLOR,
        birds=BIRDS,
        bottom_pipe=BOTTOM_PIPE,
        top_pipe=TOP_PIPE,
        floor=FLOOR,
        background=BACKGROUND,
    )
    population.run(game.main, settings.MAX_GEN)
    winner = stats.best_genome()
    nodes = {
        -1: "delta_x",
        -2: "delta_y_top",
        -3: "delta_y_bottom",
        0: "Jump or Not",
    }
    draw_net(config, winner, True, node_names=nodes)
    plot_stats(stats, ylog=False, view=True)
    plot_species(stats, view=True)

    print(f"\nBest genome:\n{winner!s}")


if __name__ == "__main__":
    main(config_file="neat.txt")
