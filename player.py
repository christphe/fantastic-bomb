""" the player """

import pygame
import config
import assets
import stage

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

SPEED = 0.01


def init_events():
    """ init events """
    return [False, False, False, False, False]


class Player:
    """ player """
    position = None
    speed = 1
    start_position = (1, 1)
    colour = 0
    joystick = None
    direction = config.DIR_DOWN
    move_time = 0
    bombs = 0
    max_bombs = 2
    pixel_position = None
    events = []

    def __init__(self, position, joystick=None):
        self.position = position
        self.pixel_position = position * config.STEP
        self.start_position = position
        self.joystick = joystick

    def die(self):
        """ die """
        self.position = self.start_position
        self.pixel_position = self.start_position

    def draw(self, offset, dest):
        """ draw bomb """
        dest.blit(assets.data.character_spritesheet, (
            offset[0] + (self.pixel_position[0] * config.STEP),
            offset[1] + (self.pixel_position[1] * config.STEP) - 10
        ), player_rects[self.colour][self.direction])

    def read_axis(self, axis):
        """ read axis and store events """
        axis_x, axis_y = axis
        if axis_x > 0.2:
            self.events[config.EVT_RIGHT] = True
        elif axis_y > 0.2:
            self.events[config.EVT_DOWN] = True
        elif axis_x < -0.2:
            self.events[config.EVT_LEFT] = True
        elif axis_y < -0.2:
            self.events[config.EVT_UP] = True

    def get_events(self):
        """ get input events """
        self.events = init_events()

        if self.joystick:
            if self.joystick.get_numaxes() > 0:
                self.read_axis((self.joystick.get_axis(0),
                                self.joystick.get_axis(1)))
            if self.joystick.get_numhats() > 0:
                self.read_axis(self.joystick.get_hat(0))

            if self.joystick.get_button(0):
                self.events[config.EVT_BOMB] = True
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.events[config.EVT_UP] = True
            elif keys[pygame.K_DOWN]:
                self.events[config.EVT_DOWN] = True
            elif keys[pygame.K_LEFT]:
                self.events[config.EVT_LEFT] = True
            elif keys[pygame.K_RIGHT]:
                self.events[config.EVT_RIGHT] = True
            elif keys[pygame.K_SPACE]:
                self.events[config.EVT_BOMB] = True

    def move(self, current_stage):
        """ move """
        if self.move_time is None:
            self.move_time = pygame.time.get_ticks()
        self.get_events()
        destination = None
        if self.events[config.EVT_UP]:
            destination = (
                self.position[0], self.position[1] - 1)
            self.direction = config.DIR_UP
        elif self.events[config.EVT_DOWN]:
            destination = (
                self.position[0], self.position[1] + 1)
            self.direction = config.DIR_DOWN
        elif self.events[config.EVT_LEFT]:
            destination = (
                self.position[0] - 1, self.position[1])
            self.direction = config.DIR_LEFT
        elif self.events[config.EVT_RIGHT]:
            destination = (
                self.position[0] + 1, self.position[1])
            self.direction = config.DIR_RIGHT

        if destination is not None:
            if stage.get_tile(current_stage, destination) != " ":
                destination = self.position
            time = pygame.time.get_ticks() - self.move_time
            self.pixel_position = (self.pixel_position[0] + ((destination[0] - self.pixel_position[0]) * SPEED * time),
                                    self.pixel_position[1] + ((destination[1] - self.pixel_position[1]) * SPEED * time))

        self.position = (round(self.pixel_position[0]), round(self.pixel_position[1]))
        self.move_time = pygame.time.get_ticks()

    def on_bomb_dropped(self):
        """ dop bomb """
        self.bombs += 1

    def on_bomb_exploded(self):
        """ dop bomb """
        self.bombs -= 1
