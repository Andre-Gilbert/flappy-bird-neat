"""Game entrypoint."""

import neat
import pygame

from flappy_bird.settings import settings
from flappy_bird.stats import draw_net, plot_species, plot_stats

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


def main(config_file):
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file
    )

    # Create a neat.population.Population object using the Config object created above
    neat_pop = neat.population.Population(config)

    # show the summary statistics of the learning progress
    neat_pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    neat_pop.add_reporter(stats)

    neat_pop.run(main, settings.MAX_GEN)

    winner = stats.best_genome()

    node_names = {-1: "delta_x", -2: "delta_y_top", -3: "delta_y_bottom", 0: "Jump or Not"}
    draw_net(config, winner, True, node_names=node_names)
    plot_stats(stats, ylog=False, view=True)
    plot_species(stats, view=True)

    print("\nBest genome:\n{!s}".format(winner))


if __name__ == "__main__":
    main("neat.txt")
