#!/usr/bin/env python3

""" Fantastic Bomb """
import os
import pygame
import stage
import bomb
import config
import assets

player_rects = [
    [
        (56, 20, 16, 26),
        (56, 45, 16, 26),
        (2, 44, 16, 26),
        (105, 47, 16, 26)
    ], [
        (211, 133, 16, 26),
        (211, 158, 16, 26),
        (157, 157, 16, 26),
        (260, 160, 16, 26)
    ], [
        (211, 20, 16, 26),
        (211, 45, 16, 26),
        (157, 44, 16, 26),
        (260, 47, 16, 26)
    ]
]


def init_events():
    """ init events """
    return [False, False, False, False, False]


def main():
    """ main function """
    pygame.init()
    screen = pygame.display.set_mode(
        config.screen_res, pygame.HWSURFACE | pygame.DOUBLEBUF)
    fake_screen = pygame.Surface(config.fake_screen_res)

    icon = pygame.image.load(os.path.join("assets", "icon.png"))
    pygame.display.set_icon(icon)

    pygame.display.set_caption("Fantatstic Bomb")
    running = True

    assets.data.load()

    player_position = (1, 1)
    direction = config.DIR_RIGHT

    current_stage = stage.stage1
    rects = player_rects[config.COLOUR_WHITE]

    stage_size = (len(current_stage[0]) *
                  config.STEP, len(current_stage) * config.STEP)
    offset = ((config.fake_screen_res[0] - stage_size[0]) // 2,
              (config.fake_screen_res[1] - stage_size[1]) // 2)
    bombs = []
    max_bombs = 2

    move_cooldown = 200
    move_time = 0

    joysticks = [pygame.joystick.Joystick(
        i) for i in range(pygame.joystick.get_count())]
    for joy in joysticks:
        joy.init()

    # main loop
    while running:
        events = init_events()
        # event handling, gets all event from the event queue
        old_position = player_position
        for joy in joysticks:
            axis_x, axis_y = (joy.get_axis(0), joy.get_axis(1))
            if axis_x > 0.2:
                events[config.EVT_RIGHT] = True
            elif axis_y > 0.2:
                events[config.EVT_DOWN] = True
            elif axis_x < -0.2:
                events[config.EVT_LEFT] = True
            elif axis_y < -0.2:
                events[config.EVT_UP] = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            events[config.EVT_UP] = True
        elif keys[pygame.K_DOWN]:
            events[config.EVT_DOWN] = True
        elif keys[pygame.K_LEFT]:
            events[config.EVT_LEFT] = True
        elif keys[pygame.K_RIGHT]:
            events[config.EVT_RIGHT] = True

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                events[config.EVT_BOMB] = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    events[config.EVT_BOMB] = True
                if event.key == pygame.K_F1:
                    rects = player_rects[0]
                if event.key == pygame.K_F2:
                    rects = player_rects[1]
                if event.key == pygame.K_F3:
                    rects = player_rects[2]
                if event.key == pygame.K_ESCAPE:
                    running = False

        can_move = ((move_time + move_cooldown) < pygame.time.get_ticks())
        if events[config.EVT_UP] and can_move:
            player_position = (
                player_position[0], player_position[1] - 1)
            direction = config.DIR_UP
        elif events[config.EVT_DOWN] and can_move:
            player_position = (
                player_position[0], player_position[1] + 1)
            direction = config.DIR_DOWN
        elif events[config.EVT_LEFT] and can_move:
            player_position = (
                player_position[0] - 1, player_position[1])
            direction = config.DIR_LEFT
        elif events[config.EVT_RIGHT] and can_move:
            player_position = (
                player_position[0] + 1, player_position[1])
            direction = config.DIR_RIGHT

        if (player_position[1] >= len(current_stage) or player_position[1] < 0) or (player_position[0] >= len(current_stage[0]) or player_position[0] < 0) or (stage.get_tile(current_stage, player_position) != " "):
            player_position = old_position
        elif can_move:
            move_time = pygame.time.get_ticks()

        if events[config.EVT_BOMB] and len(bombs) < max_bombs:
            bombs.append(bomb.drop(current_stage, player_position))

        for item in bombs:
            if (item.explosion_time < pygame.time.get_ticks()):
                player_dead = item.explode(current_stage, player_position)
                bombs.remove(item)
                if player_dead:
                    player_position = (1, 1)

        fake_screen.blit(assets.data.background, (0, 0))
        line_number = 0
        for line in current_stage:
            col_number = 0
            for block in line:
                if block == ' ':
                    tile = (328, 461)
                elif block == '░':
                    tile = (311, 461)
                elif block == '█':
                    tile = (294, 461)
                fake_screen.blit(
                    assets.data.tiles,
                    (offset[0] + col_number * config.STEP,
                     offset[1] + line_number * config.STEP),
                    (tile[0], tile[1], config.STEP, config.STEP))
                col_number += 1
            line_number += 1

        for item in bombs:
            item.draw(offset, fake_screen)
        fake_screen.blit(assets.data.character_spritesheet,
                         (offset[0] + (player_position[0] * config.STEP), offset[1] + (player_position[1] * config.STEP) - 10), rects[direction])

        screen.blit(pygame.transform.scale(
            fake_screen, config.screen_res), (0, 0))
        pygame.display.flip()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
