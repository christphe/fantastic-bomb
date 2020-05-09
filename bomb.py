""" the bomb """

import stage

rects_bomb = [
    [413, 563, 16, 16]
]

def explode(current_stage, position, player_position):
    """ explode bomb """
    player_dead = False
    explosions = [position]
    if position[1] + 1 < len(current_stage):
        explosions.append((position[0], position[1] + 1))
    if position[1] - 1 >= 0:
        explosions.append((position[0], position[1] - 1))
    if position[0] + 1 < len(current_stage[0]):
        explosions.append((position[0] + 1, position[1]))
    if position[0] - 1 >= 0:
        explosions.append((position[0] - 1, position[1]))
    for exp in explosions:
        if player_position == exp:
            player_dead = True
        stage.destroy_block(current_stage, exp)
    return player_dead

def draw(offset, step, image, dest, position):
    """ draw bomb """
    if position is not None:
        dest.blit(image, (offset[0] + (
            position[0] * step), offset[1] + (position[1] * step)), rects_bomb[0])

def drop(current_stage, position):
    """ drop bomb """
    stage.set_tile(current_stage, position, 'b')
