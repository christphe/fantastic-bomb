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

rects_white = [
    (55, 20, 16, 26),
    (55, 45, 16, 26),
    (2, 44, 16, 26),
    (105, 47, 16, 26)
]

rects_black = [
    (55, 18, 16, 26),
    (55, 45, 16, 26),
    (2, 44, 16, 26),
    (260, 46, 16, 26)
]

def main():
    """ main function """
    pygame.init()
    screen = pygame.display.set_mode(
        (1280, 800), pygame.HWSURFACE | pygame.DOUBLEBUF)
    fake_screen = pygame.Surface((320, 200))

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
    player_position = (0, 0)
    direction = DIR_RIGHT
    step = 16
    offset = (56, 12)

    current_stage = stage.stage1
    rects = rects_white

    bomb_position = None
    bomb_dropped = 0
    bomb_cooldown = 3000

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.KEYDOWN:
                old_position = player_position
                if event.key == pygame.K_UP:
                    player_position = (player_position[0], player_position[1] - 1)
                    direction = DIR_UP
                elif event.key == pygame.K_DOWN:
                    player_position = (player_position[0], player_position[1] + 1)
                    direction = DIR_DOWN
                elif event.key == pygame.K_LEFT:
                    player_position = (player_position[0] - 1, player_position[1])
                    direction = DIR_LEFT
                elif event.key == pygame.K_RIGHT:
                    player_position = (player_position[0] + 1, player_position[1])
                    direction = DIR_RIGHT
                elif event.key == pygame.K_SPACE and bomb_position is None:
                    bomb_position = player_position
                    bomb.drop(current_stage, player_position)
                    bomb_dropped = pygame.time.get_ticks()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                if player_position[1] >= len(current_stage) or player_position[1] < 0:
                    player_position = old_position
                if player_position[0] >= len(current_stage[0]) or player_position[0] < 0:
                    player_position = old_position
                if stage.get_tile(current_stage, player_position) != " ":
                    player_position = old_position
        if bomb_position is not None and bomb_dropped + bomb_cooldown < pygame.time.get_ticks():
            player_dead = bomb.explode(current_stage, bomb_position, player_position)
            bomb_position = None
            if player_dead:
                player_position = (0, 0)

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

        screen.blit(pygame.transform.scale(fake_screen, (1280, 800)), (0, 0))
        #screen.blit(fake_screen, (0, 0))
        pygame.display.flip()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
