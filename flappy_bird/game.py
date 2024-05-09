"""Flappy bird game."""

import pygame

from flappy_bird.bird import Bird
from flappy_bird.floor import Floor
from flappy_bird.pipe import Pipe


def check_collision(bird: Bird, pipe: Pipe, floor: Floor) -> bool:
    bird_mask = pygame.mask.from_surface(bird.bird)
    top_pipe_mask = pygame.mask.from_surface(pipe.top_pipe)
    bottom_pipe_mask = pygame.mask.from_surface(pipe.bottom_pipe)

    sky_height = 0
    floor_height = floor.y
    bird_lower_end = bird.y + bird.bird.get_height()

    top_pipe_offset = (round(pipe.x - bird.x), round(pipe.top_pipe_topleft - bird.y))
    bottom_pipe_offset = (round(pipe.x - bird.x), round(pipe.bottom_pipe_topleft - bird.y))

    top_pipe_intersection_point = bird_mask.overlap(top_pipe_mask, top_pipe_offset)
    bottom_pipe_intersection_point = bird_mask.overlap(bottom_pipe_mask, bottom_pipe_offset)

    return bool(
        top_pipe_intersection_point is not None
        or bottom_pipe_intersection_point is not None
        or bird_lower_end > floor_height
        or bird.y < sky_height
    )


def draw(screen, birds, pipes, floor, score, generation, game_time):
    screen.blit(BG_IMG, (0, 0))

    # draw the moving floor
    screen.blit(floor.IMGS[0], (floor.x1, floor.y))  # draw the first floor image
    screen.blit(floor.IMGS[1], (floor.x2, floor.y))  # draw the second floor image
    screen.blit(floor.IMGS[2], (floor.x3, floor.y))  # draw the third floor image

    # draw the moving pipes
    for pipe in pipes:
        screen.blit(pipe.top_pipe_img, (pipe.x, pipe.top_pipe_topleft))  # draw the pipe on the top
        screen.blit(pipe.bottom_pipe_img, (pipe.x, pipe.bottom_pipe_topleft))  # draw the pipe on the bottom

    # draw the animated birds
    for bird in birds:
        rotated_image, rotated_rect = bird.animation()
        screen.blit(rotated_image, rotated_rect)

    # add additional information
    score_text = FONT.render("Score: " + str(score), 1, FONT_COLOR)  # set up the text to show the scores
    screen.blit(score_text, (SCREEN_WIDTH - 15 - score_text.get_width(), 15))  # draw the scores

    game_time_text = FONT.render(
        "Timer: " + str(game_time) + " s", 1, FONT_COLOR
    )  # set up the text to show the progress
    screen.blit(
        game_time_text, (SCREEN_WIDTH - 15 - game_time_text.get_width(), 15 + score_text.get_height())
    )  # draw the progress

    generation_text = FONT.render(
        "Generation: " + str(generation - 1), 1, FONT_COLOR
    )  # set up the text to show the number of generation
    screen.blit(generation_text, (15, 15))  # draw the generation

    bird_text = FONT.render(
        "Birds Alive: " + str(len(birds)), 1, FONT_COLOR
    )  # set up the text to show the number of birds alive
    screen.blit(bird_text, (15, 15 + generation_text.get_height()))  # draw the number of birds alive

    progress_text = FONT.render(
        "Pipes Remained: " + str(len(pipes) - score), 1, FONT_COLOR
    )  # set up the text to show the progress
    screen.blit(progress_text, (15, 15 + generation_text.get_height() + bird_text.get_height()))  # draw the progress

    pygame.display.update()


def main(genomes, config):

    global generation, SCREEN  # use the global variable gen and SCREEN
    screen = SCREEN
    generation += 1  # update the generation

    score = 0  # initiate score to 0
    clock = pygame.time.Clock()  # set up a clock object to help control the game framerate
    start_time = pygame.time.get_ticks()  # reset the start_time after every time we update our generation

    floor = Floor(floor_starting_y_position)  # build the floor
    pipes_list = [
        Pipe(pipe_starting_x_position + i * pipe_horizontal_gap) for i in range(pipe_max_num)
    ]  # build the pipes and seperate them by pipe_horizontal_gap

    models_list = []  # create an empty list to store all the training neural networks
    genomes_list = []  # create an empty list to store all the training genomes
    birds_list = []  # create an empty list to store all the training birds

    for genome_id, genome in genomes:  # for each genome
        birds_list.append(
            Bird(bird_starting_x_position, bird_starting_y_position)
        )  # create a bird and append the bird in the list
        genome.fitness = 0  # start with fitness of 0
        genomes_list.append(genome)  # append the genome in the list
        model = neat.nn.FeedForwardNetwork.create(
            genome, config
        )  # set up the neural network for each genome using the configuration we set
        models_list.append(model)  # append the neural network in the list

    run = True

    while run is True:  # when we run the program

        # check the event of the game and quit if we close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        # stop the game when the score exceed the maximum score
        # break the loop and restart when no bird left
        if score >= max_score or len(birds_list) == 0:
            run = False
            break

        game_time = round((pygame.time.get_ticks() - start_time) / 1000, 2)  # record the game time for this generation

        clock.tick(
            FPS
        )  # update the clock, run at FPS frames per second (FPS). This can be used to help limit the runtime speed of a game.

        floor.move()  # move the floor

        pipe_input_index = get_index(pipes_list, birds_list)  # get the input index of the pipes list

        passed_pipes = []  # create an empty list to hold all the passed pipes
        for pipe in pipes_list:
            pipe.move()  # move the pipe
            if pipe.x + pipe.IMG_WIDTH < birds_list[0].x:  # if the bird passed the pipe
                passed_pipes.append(pipe)  # append the pipe to the passed pipes list

        score = len(
            passed_pipes
        )  # calculate the score of the game, which equals to the number of pipes the bird passed

        for index, bird in enumerate(birds_list):
            bird.move()  # move the bird
            delta_x = (
                bird.x - pipes_list[pipe_input_index].x
            )  # input 1: the horizontal distance between the bird and the pipe
            delta_y_top = (
                bird.y - pipes_list[pipe_input_index].top_pipe_height
            )  # input 2: the vertical distance between the bird and the top pipe
            delta_y_bottom = (
                bird.y - pipes_list[pipe_input_index].bottom_pipe_topleft
            )  # input 3: the vertical distance between the bird and the bottom pipe
            net_input = (delta_x, delta_y_top, delta_y_bottom)
            # input the bird's distance from the pipes to get the output of whether to jump or not
            output = models_list[index].activate(net_input)

            if output[0] > prob_threshold_to_jump:
                bird.jump()

            bird_failed = check_collision(bird, pipes_list[pipe_input_index], floor)

            genomes_list[index].fitness = game_time + score - bird_failed * failed_punishment

            if bird_failed:
                models_list.pop(index)
                genomes_list.pop(index)
                birds_list.pop(index)

        draw(screen, birds_list, pipes_list, floor, score, generation, game_time)
