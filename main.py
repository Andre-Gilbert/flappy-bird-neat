"""Game entrypoint."""

import neat
import pygame

from flappy_bird.game import Game
from flappy_bird.neat import draw_neural_network, plot_species, plot_stats
from flappy_bird.settings import settings

pygame.init()

WIDTH = 400
HEIGHT = 600


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
        width=WIDTH,
        height=HEIGHT,
        font=pygame.font.SysFont("comicsansms", 20),
        font_color=(255, 255, 255),
        birds=[
            pygame.image.load("./assets/bird-mid-flap.png"),
            pygame.image.load("./assets/bird-up-flap.png"),
            pygame.image.load("./assets/bird-down-flap.png"),
        ],
        pipe=pygame.image.load("./assets/pipe.png"),
        floor=pygame.image.load("./assets/floor.png"),
        background=pygame.transform.scale(pygame.image.load("./assets/background.png"), (WIDTH, HEIGHT)),
    )
    population.run(game.main, settings.MAX_GEN)
    winner = stats.best_genome()
    nodes = {
        -1: "delta_x",
        -2: "delta_y_top",
        -3: "delta_y_bottom",
        0: "Jump or Not",
    }
    draw_neural_network(config, winner, True, nodes=nodes)
    plot_stats(stats, y_log=False, view=True)
    plot_species(stats, view=True)
    print(f"\nBest genome:\n{winner!s}")


if __name__ == "__main__":
    main(config_file="neat.txt")
