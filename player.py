""" the player """

import pygame
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

MOVE_COOLDOWN = 200


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

    def __init__(self, position, joystick=None):
        self.position = position
        self.start_position = position
        self.joystick = joystick

    def die(self):
        """ die """
        self.position = self.start_position

    def draw(self, offset, dest):
        """ draw bomb """
        dest.blit(assets.data.character_spritesheet, (
            offset[0] + (self.position[0] * config.STEP),
            offset[1] + (self.position[1] * config.STEP) - 10
        ), player_rects[self.colour][self.direction])

    def read_axis(self, events, axis):
        """ read axis and store events """
        axis_x, axis_y = axis
        if axis_x > 0.2:
            events[config.EVT_RIGHT] = True
        elif axis_y > 0.2:
            events[config.EVT_DOWN] = True
        elif axis_x < -0.2:
            events[config.EVT_LEFT] = True
        elif axis_y < -0.2:
            events[config.EVT_UP] = True

    def get_events(self):
        """ get input events """
        events = init_events()

        if self.joystick:
            self.read_axis(events, (self.joystick.get_axis(0), self.joystick.get_axis(1)))
            self.read_axis(events, self.joystick.get_hat(0))

            if self.joystick.get_button(0):
                events[config.EVT_BOMB] = True
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                events[config.EVT_UP] = True
            elif keys[pygame.K_DOWN]:
                events[config.EVT_DOWN] = True
            elif keys[pygame.K_LEFT]:
                events[config.EVT_LEFT] = True
            elif keys[pygame.K_RIGHT]:
                events[config.EVT_RIGHT] = True
            elif keys[pygame.K_SPACE]:
                events[config.EVT_BOMB] = True

        return events

    def can_move(self):
        """ check if can move """
        return (self.move_time + MOVE_COOLDOWN) < pygame.time.get_ticks()

    def on_bomb_dropped(self):
        """ dop bomb """
        self.bombs += 1

    def on_bomb_exploded(self):
        """ dop bomb """
        self.bombs -= 1
