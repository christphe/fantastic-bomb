""" the bomb """

import pygame
import config
import stage
import assets

BOMB_COOLDOWN = 3000
rects_bomb = [
    [413, 563, 16, 16]
]


class Bomb:
    """ Bomb """

    position = None
    explosion_time = 0
    power = 0
    owner = None

    def __init__(self, position, power=1):
        self.position = position
        self.explosion_time = pygame.time.get_ticks() + BOMB_COOLDOWN
        self.power = power

    def stop_explosion(self, current_stage, position):
        """ check if bomb explosion has to stop """
        tile = stage.get_tile(current_stage, position)
        if tile != " ":
            return True
        return False

    def explode(self, current_stage, player_position):
        """ explode bomb """
        player_dead = False
        explosions = [self.position]
        for i in range(1, self.power + 1):
            position = (self.position[0], self.position[1] + i)
            explosions.append(position)
            if self.stop_explosion(current_stage, position):
                break
        for i in range(1, self.power + 1):
            position = (self.position[0], self.position[1] - i)
            explosions.append(position)
            if self.stop_explosion(current_stage, position):
                break
        for i in range(1, self.power + 1):
            position = (self.position[0] + i, self.position[1])
            explosions.append(position)
            if self.stop_explosion(current_stage, position):
                break
        for i in range(1, self.power + 1):
            position = (self.position[0] - i, self.position[1])
            explosions.append(position)
            if self.stop_explosion(current_stage, position):
                break
        for exp in explosions:
            if player_position == exp:
                player_dead = True
            stage.destroy_block(current_stage, exp)
        return player_dead

    def draw(self, offset, dest):
        """ draw bomb """
        dest.blit(assets.data.tiles, (
            offset[0] + (self.position[0] * config.STEP),
            offset[1] + (self.position[1] * config.STEP)
        ), rects_bomb[0])


def drop(current_stage, position):
    """ drop bomb """
    stage.set_tile(current_stage, position, 'b')
    return Bomb(position, 2)
