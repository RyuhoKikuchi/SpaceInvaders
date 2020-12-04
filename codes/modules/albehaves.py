from copy import copy
from os import system
from random import randint
from time import sleep

direction = 1  # These variables will be arguments
slowness = 2
step = 0
allist = []

fired_laser = []

# DO PUT THIS BEFORE LOOP IN MAIN PROCESS
x = 8  # USE ONCE, THAT'S IT
y = 5  # Do not forget to declarate list named allist before
for horde in range(52):
    allist.append([x, y])
    x += 2
    if x == 34:
        y += 1
        x = 8

def attack():
    global allist
    global fired_laser
    if len(fired_laser) < 2:
        maximization = []
        chosenX = randint(min(allist)[0], max(allist)[0])
        for maximazingY in allist:
            if maximazingY[0] == chosenX:
                maximization.append(maximazingY)
        fired_laser.append(copy(max(maximization)))
    for down in fired_laser:
        down[1] += 1
        if down[1] >= 15:
            fired_laser.remove(down)

while True:
    step += 1
    if step == slowness:
        system('clear')
        print(allist)
        if direction == 1:
            for shiftX in allist:
                shiftX[0] += 1
                if max(allist)[0] == 40:
                    direction = 2
        elif direction == 2:
            for shiftY in allist:
                shiftY[1] += 1
            direction = 3
        elif direction == 3:
            for shiftX in allist:
                shiftX[0] -= 1
                if min(allist)[0] == 11:
                    direction = 4
        elif direction == 4:
            for shiftY in allist:
                shiftY[1] += 1
            direction = 1
        step = 0
    attack()
    print(allist)
    print(fired_laser)
    sleep(4)
