#!/usr/bin/env python3

""" Fantastic Bomb """
import os
import pygame
import config
import assets
import stage
import bomb
import player


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

    current_stage = stage.stage1

    stage_size = (len(current_stage[0]) *
                  config.STEP, len(current_stage) * config.STEP)
    offset = ((config.fake_screen_res[0] - stage_size[0]) // 2,
              (config.fake_screen_res[1] - stage_size[1]) // 2)
    bombs = []
    max_bombs = 2

    joysticks = [pygame.joystick.Joystick(
        i) for i in range(pygame.joystick.get_count())]
    players = []
    players.append(player.Player((1, 1)))
    players[0].position = (13, 11)
    players[0].colour = config.COLOUR_BLACK
    for joy in joysticks:
        joy.init()
        players.append(player.Player((1, 1), joy))

    # main loop
    while running:
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        for current_player in players:
            events = current_player.get_events()
            old_position = current_player.position
            # event handling, gets all event from the event queue
            if current_player.can_move():
                if events[config.EVT_UP]:
                    current_player.position = (
                        current_player.position[0], current_player.position[1] - 1)
                    current_player.direction = config.DIR_UP
                elif events[config.EVT_DOWN]:
                    current_player.position = (
                        current_player.position[0], current_player.position[1] + 1)
                    current_player.direction = config.DIR_DOWN
                elif events[config.EVT_LEFT]:
                    current_player.position = (
                        current_player.position[0] - 1, current_player.position[1])
                    current_player.direction = config.DIR_LEFT
                elif events[config.EVT_RIGHT]:
                    current_player.position = (
                        current_player.position[0] + 1, current_player.position[1])
                    current_player.direction = config.DIR_RIGHT

                if stage.get_tile(current_stage, current_player.position) != " ":
                    current_player.position = old_position
                else:
                    current_player.move_time = pygame.time.get_ticks()

            if (events[config.EVT_BOMB]
                    and len(bombs) < max_bombs
                    and stage.get_tile(current_stage, current_player.position) == ' '):
                bombs.append(bomb.drop(current_stage, current_player.position))

        for current_bomb in bombs:
            if current_bomb.explosion_time < pygame.time.get_ticks():
                # player_dead = current_bomb.explode(current_stage, current_bomb.position)
                current_bomb.explode(current_stage, current_bomb.position)
                bombs.remove(current_bomb)
                # if player_dead:
                #     current_bomb.position = (1, 1)

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

        for current_bomb in bombs:
            current_bomb.draw(offset, fake_screen)
        for current_player in players:
            current_player.draw(offset, fake_screen)

        screen.blit(pygame.transform.scale(
            fake_screen, config.screen_res), (0, 0))
        pygame.display.flip()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
