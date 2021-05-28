from copy import deepcopy
import itertools


class Projection():

    def __init__(self):
        self.projectiles = []
        self.screen = []


    def stage(self, x, y, char):
        projectile = [y, x, char]
        self.projectiles.append(projectile); self.projectiles.sort()
        self.screen = deepcopy(self.projectiles)
        last_index = -1
        for entry in self.screen:
            if last_index >= 0:
                if entry[0] == self.projectiles[last_index][0]:
                    entry[1] -= self.projectiles[last_index][1]
                entry[0] -= self.projectiles[last_index][0]
            entry[1] -= 1; last_index += 1
            entry[0], entry[1] = entry[0] * '\n', entry[1] * ' '


    def proj(self):
        print(''.join(list(itertools.chain.from_iterable(self.screen))))


if __name__ == '__main__':
    testDrive = Projection()
    for i in range(5, 25, 5):
        testDrive.stage(i, i, str(i))
    testDrive.proj()
    del testDrive