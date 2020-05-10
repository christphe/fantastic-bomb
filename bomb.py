""" the bomb """

import pygame
import config
import stage
import assets

BOMB_COOLDOWN = 3000
rects_bomb = [
    [413, 563, 16, 16]
]
rects_explosion = [
    [345, 512, 16, 16]
]
EXPLOSION_DURATION = 200

class Bomb:
    """ Bomb """

    position = None
    explosion_time = 0
    power = 0
    owner = None
    exploding = None
    explosions = []

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

    def explode(self, current_stage, players, bombs):
        """ explode bomb """
        if self.exploding is not None:
            return

        self.exploding = pygame.time.get_ticks() + EXPLOSION_DURATION

        if self.owner:
            self.owner.on_bomb_exploded()

        self.explosions = [self.position]
        for i in range(1, self.power + 1):
            position = (self.position[0], self.position[1] + i)
            self.explosions.append(position)
            if self.stop_explosion(current_stage, position):
                break
        for i in range(1, self.power + 1):
            position = (self.position[0], self.position[1] - i)
            self.explosions.append(position)
            if self.stop_explosion(current_stage, position):
                break
        for i in range(1, self.power + 1):
            position = (self.position[0] + i, self.position[1])
            self.explosions.append(position)
            if self.stop_explosion(current_stage, position):
                break
        for i in range(1, self.power + 1):
            position = (self.position[0] - i, self.position[1])
            self.explosions.append(position)
            if self.stop_explosion(current_stage, position):
                break
        for exp in self.explosions:
            for p in players:
                if p.position == exp:
                    p.die()
            for b in bombs:
                if (exp == b.position
                    and b.exploding is None):
                    b.explode(current_stage, players, bombs)
            stage.destroy_block(current_stage, exp)

    def draw(self, offset, dest):
        """ draw bomb """
        dest.blit(assets.data.tiles, (
            offset[0] + (self.position[0] * config.STEP),
            offset[1] + (self.position[1] * config.STEP)
        ), rects_bomb[0])

        for exp in self.explosions:
            dest.blit(assets.data.tiles, (
                offset[0] + (exp[0] * config.STEP),
                offset[1] + (exp[1] * config.STEP)
            ), rects_explosion[0])



def drop(current_stage, position):
    """ drop bomb """
    stage.set_tile(current_stage, position, 'b')
    return Bomb(position, 2)
