"""NEAT visualizations."""

import copy
import warnings
from typing import Any

import graphviz
import matplotlib.pyplot as plt
import neat
import numpy as np


def plot_stats(
    statistics: neat.StatisticsReporter,
    y_log: bool = False,
    view: bool = False,
    filename: str = "avg_fitness.svg",
) -> None:
    """Plots the population's average and best fitness."""
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    generation = range(len(statistics.most_fit_genomes))
    best_fitness = [genome.fitness for genome in statistics.most_fit_genomes]
    avg_fitness = np.array(statistics.get_fitness_mean())
    stdev_fitness = np.array(statistics.get_fitness_stdev())

    plt.plot(generation, avg_fitness, "b-", label="average")
    plt.plot(generation, avg_fitness - stdev_fitness, "g-.", label="-1 sd")
    plt.plot(generation, avg_fitness + stdev_fitness, "g-.", label="+1 sd")
    plt.plot(generation, best_fitness, "r-", label="best")

    plt.title("Population's average and best fitness")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.grid()
    plt.legend(loc="best")

    if y_log:
        plt.gca().set_yscale("symlog")
    plt.savefig(filename)
    if view:
        plt.show()
    plt.close()


def plot_species(statistics: neat.StatisticsReporter, view: bool = False, filename: str = "speciation.svg") -> None:
    """Visualizes speciation."""
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    species_sizes = statistics.get_species_sizes()
    num_generations = len(species_sizes)
    curves = np.array(species_sizes).T

    _, ax = plt.subplots()
    ax.stackplot(range(num_generations), *curves)

    plt.title("Speciation")
    plt.ylabel("Size per Species")
    plt.xlabel("Generations")

    plt.savefig(filename)
    if view:
        plt.show()
    plt.close()


def draw_neural_network(
    config: Any,
    genome: Any,
    view: bool = False,
    filename: str | None = None,
    nodes: dict | None = None,
    show_disabled: bool = True,
    prune_unused: bool = False,
    node_colors: bool = None,
    graph_format: str = "svg",
) -> graphviz.Digraph:
    """Draws a neural network given a genome."""
    if graphviz is None:
        warnings.warn("This display is not available due to a missing optional dependency (graphviz)")
        return

    nodes = nodes or {}
    node_colors = node_colors or {}
    dot = graphviz.Digraph(
        format=graph_format,
        node_attr={"shape": "circle", "fontsize": "9", "height": "0.2", "width": "0.2"},
    )

    inputs = set()
    for k in config.genome_config.input_keys:
        inputs.add(k)
        name = nodes.get(k, str(k))
        input_attrs = {"style": "filled", "shape": "box", "fillcolor": node_colors.get(k, "lightgray")}
        dot.node(name, _attributes=input_attrs)

    outputs = set()
    for k in config.genome_config.output_keys:
        outputs.add(k)
        name = nodes.get(k, str(k))
        node_attrs = {"style": "filled", "fillcolor": node_colors.get(k, "lightblue")}
        dot.node(name, _attributes=node_attrs)

    if prune_unused:
        connections = set()
        for cg in genome.connections.values():
            if cg.enabled or show_disabled:
                connections.add((cg.in_node_id, cg.out_node_id))

        used_nodes = copy.copy(outputs)
        pending = copy.copy(outputs)
        while pending:
            new_pending = set()
            for a, b in connections:
                if b in pending and a not in used_nodes:
                    new_pending.add(a)
                    used_nodes.add(a)
            pending = new_pending
    else:
        used_nodes = set(genome.nodes.keys())

    for n in used_nodes:
        if n in inputs or n in outputs:
            continue
        attrs = {"style": "filled", "fillcolor": node_colors.get(n, "white")}
        dot.node(str(n), _attributes=attrs)

    for connected_genome in genome.connections.values():
        if connected_genome.enabled or show_disabled:
            genome_input, genome_output = connected_genome.key
            a = nodes.get(genome_input, str(genome_input))
            b = nodes.get(genome_output, str(genome_output))
            style = "solid" if connected_genome.enabled else "dotted"
            color = "green" if connected_genome.weight > 0 else "red"
            width = str(0.1 + abs(connected_genome.weight / 5.0))
            dot.edge(a, b, _attributes={"style": style, "color": color, "penwidth": width})

    dot.render(filename, view=view)
    return dot
