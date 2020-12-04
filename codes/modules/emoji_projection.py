from copy import deepcopy
import itertools
from termcolor import colored


def del_stage():
    global projectiles; del projectiles
    global screen; del screen

def stage(x, y, char):
    projectile = [x, y, char]
    global projectiles  # Checking if this usage is first time.
    if 'projectiles' not in globals():
        projectiles = list()
    # Swapping X and Y, adding new one, and ordering it.
    projectile[0], projectile[1] = projectile[1], projectile[0]
    projectiles.append(projectile); projectiles.sort()
    #  Adjustment to printable
    global screen
    screen = deepcopy(projectiles)
    last_index = -1
    for entry in screen:
        if last_index >= 0:
            if entry[0] == projectiles[last_index][0]:
                entry[1] -= projectiles[last_index][1]
            entry[0] -= projectiles[last_index][0]
        entry[1] -= 1; last_index += 1
        # Attaching newline codes and spaces
        entry[0] = entry[0] * '\n'
        entry[1] = entry[1] * colored('〓', 'grey')

def proj():
    global screen
    print(''.join(list(itertools.chain.from_iterable(screen))))