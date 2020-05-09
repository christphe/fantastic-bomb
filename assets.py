""" assets """
import os
import pygame
import config


class Data:
    """ Assets Data """
    character_spritesheet = None
    tiles = None
    background = None


    def load(self):
        """ load data """
        self.character_spritesheet = pygame.image.load(
            os.path.join("assets", "character-spritesheet.png"))
        self.character_spritesheet.set_colorkey((64, 144, 56))
        self.tiles = pygame.image.load(
            os.path.join("assets", "world-tiles.png"))
        self.background = pygame.image.load(
            os.path.join("assets", "background.png"))
        self.background = pygame.transform.scale(self.background, config.fake_screen_res)

data = Data()
