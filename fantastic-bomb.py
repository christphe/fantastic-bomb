#!/usr/bin/env python3

""" Fantastic Bomb """
import os
import pygame
import stage
import bomb

DIR_UP = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_RIGHT = 3

COLOUR_WHITE = 0
COLOUR_BLACK = 1
COLOUR_BLUE = 2

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

EVT_UP = 0
EVT_DOWN = 1
EVT_LEFT = 2
EVT_RIGHT = 3
EVT_BOMB = 4


def init_events():
    """ init events """
    return [False, False, False, False, False]


def main():
    """ main function """
    pygame.init()
    screen_res = (1280, 1024)
    fake_screen_res = (320, 240)
    screen = pygame.display.set_mode(
        screen_res, pygame.HWSURFACE | pygame.DOUBLEBUF)
    fake_screen = pygame.Surface(fake_screen_res)

    icon = pygame.image.load(os.path.join("assets", "icon.png"))
    pygame.display.set_icon(icon)

    pygame.display.set_caption("Fantatstic Bomb")
    running = True

    character_spritesheet = pygame.image.load(
        os.path.join("assets", "character-spritesheet.png"))
    character_spritesheet.set_colorkey((64, 144, 56))
    tiles = pygame.image.load(
        os.path.join("assets", "world-tiles.png"))
    background = pygame.image.load(
        os.path.join("assets", "background.png"))
    background = pygame.transform.scale(background, fake_screen_res)
    player_position = (1, 1)
    direction = DIR_RIGHT
    step = 16

    current_stage = stage.stage1
    rects = player_rects[COLOUR_WHITE]

    stage_size = (len(current_stage[0]) *
                  step, len(current_stage) * step)
    offset = ((fake_screen_res[0] - stage_size[0]) // 2,
              (fake_screen_res[1] - stage_size[1]) // 2)
    bomb_position = None
    bomb_dropped = 0
    bomb_cooldown = 3000

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
                events[EVT_RIGHT] = True
            elif axis_y > 0.2:
                events[EVT_DOWN] = True
            elif axis_x < -0.2:
                events[EVT_LEFT] = True
            elif axis_y < -0.2:
                events[EVT_UP] = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            events[EVT_UP] = True
        elif keys[pygame.K_DOWN]:
            events[EVT_DOWN] = True
        elif keys[pygame.K_LEFT]:
            events[EVT_LEFT] = True
        elif keys[pygame.K_RIGHT]:
            events[EVT_RIGHT] = True

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.JOYBUTTONDOWN and bomb_position is None:
                events[EVT_BOMB] = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bomb_position is None:
                    events[EVT_BOMB] = True
                if event.key == pygame.K_F1:
                    rects = player_rects[0]
                if event.key == pygame.K_F2:
                    rects = player_rects[1]
                if event.key == pygame.K_F3:
                    rects = player_rects[2]
                if event.key == pygame.K_ESCAPE:
                    running = False

        can_move = ((move_time + move_cooldown) < pygame.time.get_ticks())
        if events[EVT_UP] and can_move:
            player_position = (
                player_position[0], player_position[1] - 1)
            direction = DIR_UP
        elif events[EVT_DOWN] and can_move:
            player_position = (
                player_position[0], player_position[1] + 1)
            direction = DIR_DOWN
        elif events[EVT_LEFT] and can_move:
            player_position = (
                player_position[0] - 1, player_position[1])
            direction = DIR_LEFT
        elif events[EVT_RIGHT] and can_move:
            player_position = (
                player_position[0] + 1, player_position[1])
            direction = DIR_RIGHT

        if (player_position[1] >= len(current_stage) or player_position[1] < 0) or (player_position[0] >= len(current_stage[0]) or player_position[0] < 0) or (stage.get_tile(current_stage, player_position) != " "):
            player_position = old_position
        elif can_move:
            move_time = pygame.time.get_ticks()

        if events[EVT_BOMB] and bomb_position is None:
            bomb_position = player_position
            bomb.drop(current_stage, player_position)
            bomb_dropped = pygame.time.get_ticks()

        if bomb_position is not None and bomb_dropped + bomb_cooldown < pygame.time.get_ticks():
            player_dead = bomb.explode(
                current_stage, bomb_position, player_position)
            bomb_position = None
            if player_dead:
                player_position = (1, 1)

        fake_screen.blit(background, (0, 0))
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
                    tiles,
                    (offset[0] + col_number * step,
                     offset[1] + line_number * step),
                    (tile[0], tile[1], step, step))
                col_number += 1
            line_number += 1

        bomb.draw(offset, step, tiles, fake_screen, bomb_position)
        fake_screen.blit(character_spritesheet,
                         (offset[0] + (player_position[0] * step), offset[1] + (player_position[1] * step) - 10), rects[direction])

        screen.blit(pygame.transform.scale(fake_screen, screen_res), (0, 0))
        pygame.display.flip()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
