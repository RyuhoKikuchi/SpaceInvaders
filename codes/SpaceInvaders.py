import copy as cp
from getkey import getkey, keys
from modules import emoji_projection as ep
from os import system
from random import choice
import sys
from termcolor import colored
import termios
import time as tm
from timeout_decorator import timeout, TimeoutError


theme = 'green'

score = 0000  # Initial score starting from zero

rocket = [5, 19, '🚀']

life = 3
life_one = rocket[2]
life_two = rocket[2]


class tickout:
    @timeout(0.07)
    def key():
        global key
        key = ''
        try:
            key = getkey()
        except KeyboardInterrupt:
            pass


def albehaves():
    global allist
    global aldirection
    global alslowness
    global alstep
    global fire_frequency
    remains = len(allist)
    if 52 >= remains > 40:
        alslowness = 18
    elif 40 >= remains > 32:
        alslowness = 16
    elif 32 >= remains > 26:
        alslowness = 14
    elif 26 >= remains > 21:
        alslowness = 12
    elif 21 >= remains > 16:
        alslowness = 10
    elif 16 >= remains > 12:
        alslowness = 9
        if remains <= 14:
            fire_frequency = 1
    elif 12 >= remains > 9:
        alslowness = 7
    elif 9 >= remains > 4:
        alslowness = 6
    elif 4 >= remains > 2:
        alslowness = 4
    elif remains == 2:
        alslowness = 2
    elif remains == 1:
        alslowness = 1
    alstep += 1
    if alstep >= alslowness:
        if aldirection == 1:
            for shiftX in allist:
                shiftX[0] += 1
                if max(allist)[0] == 40:
                    aldirection = 2
        elif aldirection == 2:
            for shiftY in allist:
                shiftY[1] += 1
            aldirection = 3
        elif aldirection == 3:
            for shiftX in allist:
                shiftX[0] -= 1
                if min(allist)[0] == 1:
                    aldirection = 4
        elif aldirection == 4:
            for shiftY in allist:
                shiftY[1] += 1
            aldirection = 1
        alstep = 0


def attack():
    global allist
    global fired_laser
    global laser_slowness
    global laser_tick
    laser_tick += 1
    try:
        if len(fired_laser) < fire_frequency:  # Creating and firing lasers
            maximization = []
            choiceX = []
            for choosingYcolumn in allist:
                choiceX.append(choosingYcolumn[0])
            chosenX = choice(choiceX)
            for maximazingY in allist:
                if maximazingY[0] == chosenX:
                    maximization.append(maximazingY)
                    copied_maximazation = cp.copy(max(maximization))
                    copied_maximazation[1] += 1
            fired_laser.append(copied_maximazation)
    except:
        pass
    if laser_tick == laser_slowness:  # Moving lasers
        for down in fired_laser:
            down[1] += 1
            laser_tick = 0
            if down[1] >= 20:
                fired_laser.remove(down)


def cannon():
    global calist
    global caspeed
    global catick
    global score
    global caslowness
    global ufo
    global fired_laser
    catick += 1
    if catick == caslowness:
        for cannonball in calist:
            cannonball[1] -= caspeed
            avoid_skip_ball = [cannonball[0], cannonball[1] - 1]
            if cannonball[1] <= 2:
                calist.remove(cannonball)
                ep.stage(cannonball[0], cannonball[1], '💥')
            elif cannonball in allist:
                allist.remove(cannonball)
                calist.remove(cannonball)
                score += 20
                ep.stage(cannonball[0], cannonball[1], '💥')
            elif cannonball in fired_laser:
                fired_laser.remove(cannonball)
                calist.remove(cannonball)
                ep.stage(cannonball[0], cannonball[1], '💥')
            elif avoid_skip_ball in fired_laser:
                fired_laser.remove(avoid_skip_ball)
                calist.remove(cannonball)
                ep.stage(avoid_skip_ball[0], avoid_skip_ball[1], '💥')
            try:
                if cannonball in ufo:
                    del ufo
                    calist.remove(cannonball)
                    score += 100
                    ep.stage(cannonball[0], cannonball[1], '💥')
                elif cannonball[0] == ufo[0][0] - 1 and cannonball[1] == ufo[0][1]:
                    del ufo
                    calist.remove(cannonball)
                    score += 100
                    ep.stage(cannonball[0], cannonball[1], '💥')
            except:
                pass
        catick = 0


def fire(position):
    global calist
    global fireinterval
    global firetick
    if firetick == fireinterval:
        Posifire = cp.copy(position)
        Posifire[1] -= 1
        calist.append(Posifire)
        firetick = 0


def game_over():
	global fd
	w = 'white'
	message([[18, 4, colored('\033[1mG\033[1m', w)], [19, 4, colored('\033[1mA\033[1m', w)], [20, 4, colored('\033[1mM\033[1m', w)], [21, 4, colored('\033[1mE\033[1m', w)], [23, 4, colored('\033[1mO\033[1m', w)], [24, 4, colored('\033[1mV\033[1m', w)], [25, 4, colored('\033[1mE\033[1m', w)], [26, 4, colored('\033[1mR\033[1m', w)]])
	ep.del_stage()
	tm.sleep(2)
	system('clear')
	termios.tcsetattr(fd, termios.TCSANOW, old)
	sys.exit()


def ground_animation():
	global ground_list
	global fired_laser
	for damage in ground_list:
		damaged_list = [damage[0], damage[1] - 1]
		if damaged_list in fired_laser:
			damage[2] -= 1
			damage[3] = '‐–'
			if damage[2] <= -15:
				damage[3] = ' –'
		ep.stage(damage[0], damage[1], colored(damage[3], theme))


def key_control():
    global fd
    global old
    global key
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ECHO
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        try:
            tickout.key()
        except TimeoutError:
            pass
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, new)
        if key == ' ' or key == keys.UP:
            global rocket
            fire([rocket[0], rocket[1]])
        elif key == keys.RIGHT:
            MoveRight()
        elif key == keys.LEFT:
            MoveLeft()
        else:
            pass

def message(chars):
	system('clear')
	ep.proj()
	for shifting in chars:
		tm.sleep(0.1)
		ep.stage(shifting[0], shifting[1], shifting[2])
		system('clear')
		ep.proj()

def MoveRight():
    global rocket
    global rocket_pitch
    global rocket_stride
    global rocket_tick
    rocket_tick += 1
    if rocket[0] < 40 and rocket_tick >= rocket_pitch: 
        rocket[0] += rocket_stride
        rocket_tick = 0


def MoveLeft():
    global rocket
    global rocket_pitch
    global rocket_stride
    global rocket_tick
    rocket_tick += 1
    if rocket[0] > 1 and rocket_tick >= rocket_pitch:
        rocket[0] -= rocket_stride
        rocket_tick = 0


def shield():
    global calist
    global fired_laser
    global shield_list
    global shield_endurance
    for collide in shield_list:
        collided_position = [collide[0], collide[1]]
        if collided_position in allist:
            shield_list.remove(collide)
        elif collided_position in calist:
            calist.remove(collided_position)
            collide[2] -= 1
            if collide[2] == 0:
                shield_list.remove(collide)
                ep.stage(collide[0], collide[1], '💥')
        elif collided_position in fired_laser:
            fired_laser.remove(collided_position)
            collide[2] -= 1
            if collide[2] == 0:
                shield_list.remove(collide)
                ep.stage(collide[0], collide[1], '💥')


def success():
	global fd
	system('clear')
	ep.proj()
	tm.sleep(3)
	w = 'white'
	g = 'green'
	ep.del_stage()
	ep.stage(9, 0, colored('\033[1mSCORE<1>           HI-SCORE           SCORE<2>\033[1m', w))
	ep.stage(10, 1, colored(f'\033[1m{str(score).zfill(4)}              {str(score).zfill(4)}\033[1m', w))
	ep.stage(7, 21, colored(f'\033[1m 0            \033[1m', 'white'))
	ep.stage(23, 21, colored('\033[1mCREDIT 00\033[1m', 'white'))
	message([[17, 10, colored('\033[1m INSERT  COIN\033[1m', w)], [16, 13, colored('\033[1m <\033[1m', w)], [17, 13, colored('\033[1m1\033[1m', w)], [18, 13, colored('\033[1m O\033[1m', w)], [19, 13, colored('\033[1mR\033[1m', w)], 
	[20, 13, colored('\033[1m 2\033[1m', w)], [21, 13, colored('\033[1m P\033[1m', w)], [22, 13, colored('\033[1mL\033[1m', w)], [23, 13, colored('\033[1mA\033[1m', w)], [24, 13, colored('\033[1mY\033[1m', w)], 
	[25, 13, colored('\033[1mE\033[1m', w)], [26, 13, colored('\033[1mR\033[1m', w)], [27, 13, colored('\033[1mS\033[1m', w)], [28, 13, colored('\033[1m>\033[1m', w)], [16, 15, colored('\033[1m＊\033[1m', w)], 
	[17, 15, colored('\033[1m1\033[1m', w)], [18, 15, colored('\033[1m P\033[1m', w)], [19, 15, colored('\033[1mL\033[1m', w)], [20, 15, colored('\033[1mA\033[1m', w)], [21, 15, colored('\033[1mY\033[1m', w)], 
	[22, 15, colored('\033[1mE\033[1m', w)], [23, 15, colored('\033[1mR\033[1m', w)], [25, 15, colored('\033[1m 1\033[1m', w)], [26, 15, colored('\033[1m C\033[1m', w)], [27, 15, colored('\033[1mO\033[1m', w)], 
	[28, 15, colored('\033[1mI\033[1m', w)], [29, 15, colored('\033[1mN\033[1m', w)], [16, 17, colored('\033[1m＊\033[1m', g)], [17, 17, colored('\033[1m2\033[1m', g)], [18, 17, colored('\033[1m P\033[1m', g)], 
	[19, 17, colored('\033[1mL\033[1m', g)], [20, 17, colored('\033[1mA\033[1m', g)], [21, 17, colored('\033[1mY\033[1m', g)], [22, 17, colored('\033[1mE\033[1m', g)], [23, 17, colored('\033[1mR\033[1m', g)], 
	[24, 17, colored('\033[1mS\033[1m', g)], [26, 17, colored('\033[1m2\033[1m', g)], [27, 17, colored('\033[1m C\033[1m', g)], [28, 17, colored('\033[1mO\033[1m', g)], [29, 17, colored('\033[1mI\033[1m', g)], 
	[30, 17, colored('\033[1mN\033[1m', g)], [31, 17, colored('\033[1mS\033[1m', g)]])
	ep.del_stage()
	tm.sleep(2)
	system('clear')
	termios.tcsetattr(fd, termios.TCSANOW, old)
	sys.exit()


def ufo_behave():
	global ufo
	global ufo_slowness
	global ufo_tick
	global ufo_time_start
	ufo_tick += 1
	ufo_time_now = tm.time()
	ufo_timer = ufo_time_now - ufo_time_start
	if ufo_timer >= 42:
		ufo = [[40, 3]]
		ufo_time_start = tm.time()
	try:
		if ufo_tick == ufo_slowness:
			ufo_tick = 0
			ufo[0][0] -= 1
			if ufo[0][0] == 0:
				del ufo
	except:
		pass


system('clear')
tm.sleep(1.5)
w = 'white'
g = 'green'
ep.stage(9, 0, colored('\033[1mSCORE<1>           HI-SCORE           SCORE<2>\033[1m', w))
ep.stage(10, 1, colored(f'\033[1m{str(score).zfill(4)}              {str(score).zfill(4)}\033[1m', w))
ep.stage(7, 21, colored(f'\033[1m 0            \033[1m', 'white'))
ep.stage(23, 21, colored('\033[1mCREDIT 00\033[1m', 'white'))
message([[19, 5, colored('\033[1m P\033[1m', w)], [20, 5, colored('\033[1mL\033[1m', w)], [21, 5, colored('\033[1mA\033[1m', w)], [22, 5, colored('\033[1mY\033[1m', w)], [17, 7, colored('\033[1mS\033[1m', w)], [18, 7, colored('\033[1mP\033[1m', w)], [19, 7, colored('\033[1mA\033[1m', w)], [20, 7, colored('\033[1mC\033[1m', w)], [21, 7, colored('\033[1mE\033[1m', w)], [23, 7, colored('\033[1mI\033[1m', w)], [24, 7, colored('\033[1mN\033[1m', w)], [25, 7, colored('\033[1mV\033[1m', w)], [26, 7, colored('\033[1mA\033[1m', w)], [27, 7, colored('\033[1mD\033[1m', w)], [28, 7, colored('\033[1mE\033[1m', w)], [29, 7, colored('\033[1mR\033[1m', w)], [30, 7, colored('\033[1mS\033[1m', w)]])
tm.sleep(0.3)
ep.stage(15, 10, colored('\033[1m＊SCORE ADVANCE TABLE＊\033[1m', w))
ep.stage(17, 11, colored('\033[1m 🛸=\033[1m', w))
ep.stage(17, 12, colored(' 👾', g))
message([[18, 11, colored('\033[1m?\033[1m', w)], [19, 11, colored('\033[1m M\033[1m', w)], [20, 11, colored('\033[1mY\033[1m', w)], [21, 11, colored('\033[1mS\033[1m', w)], [22, 11, colored('\033[1mT\033[1m', w)], [23, 11, colored('\033[1mE\033[1m', w)], [24, 11, colored('\033[1mR\033[1m', w)], [25, 11, colored('\033[1mY\033[1m', w)], [18, 12, colored('\033[1m=\033[1m', g)], [19, 12, colored('\033[1m2\033[1m', g)], [20, 12, colored('\033[1m0\033[1m', g)], [21, 12, colored('\033[1m P\033[1m', g)], [22, 12, colored('\033[1mO\033[1m', g)], [23, 12, colored('\033[1mI\033[1m', g)], [24, 12, colored('\033[1mN\033[1m', g)], [25, 12, colored('\033[1mT\033[1m', g)], [26, 12, colored('\033[1mS\033[1m', g)]])
tm.sleep(0.4)
ep.del_stage()
ep.stage(9, 0, colored('\033[1mSCORE<1>           HI-SCORE           SCORE<2>\033[1m', w))
ep.stage(10, 1, colored(f'\033[1m{str(score).zfill(4)}              {str(score).zfill(4)}\033[1m', w))
ep.stage(19, 8, colored('\033[1m PUSH\033[1m', w))
ep.stage(15, 10, colored('\033[1m ONLY 1PLAYER  BUTTON\033[1m', w))
ep.stage(7, 21, colored(f'\033[1m 0            \033[1m', 'white'))
ep.stage(23, 21, colored('\033[1mCREDIT 00\033[1m', 'white'))
system('clear')
ep.proj()
tm.sleep(0.4)
ep.del_stage()
ep.stage(9, 0, colored('\033[1mSCORE<1>           HI-SCORE           SCORE<2>\033[1m', w))
ep.stage(10, 1, colored(f'\033[1m\033[05m{str(score).zfill(4)}\033[0m\033[0m', w))
ep.stage(11, 1, colored(f'\033[1m              {str(score).zfill(4)}\033[1m', w))
ep.stage(16, 9, colored('\033[1m PLAY PLAYER<1>\033[1m', w))
ep.stage(7, 21, colored(f'\033[1m 0            \033[1m', 'white'))
ep.stage(23, 21, colored('\033[1mCREDIT 00\033[1m', 'white'))
system('clear')
ep.proj()
tm.sleep(3.5)
ep.del_stage()
system('clear')
tm.sleep(0.2)


def main():
    global allist
    global calist
    global ch_theme
    global fireinterval
    global fired_laser
    global firetick
    global life
    global life_one
    global life_two
    global present_color
    global rocket
    global shield_list
    global theme
    while True:  # Game process
        if ch_theme == 75:
            ch_theme = 0
            present_color += 1
            if present_color == 7:
                present_color = 0
            theme = theme_colors[present_color]
        if firetick < fireinterval:
            firetick += 1
        albehaves()
        attack()
        ufo_behave()
        cannon()
        try:
            ep.stage(ufo[0][0], ufo[0][1], '🛸')
        except:
            pass
        shield()
        for shields in shield_list:
            ep.stage(shields[0], shields[1], colored('〓', theme))
        for alien in allist:
            ep.stage(alien[0], alien[1], '👾')
        key_control()  # for rocket
        ep.stage(9, 0, colored('\033[1mSCORE<1>           HI-SCORE           SCORE<2>\033[1m', 'white'))
        ep.stage(10, 1, colored(f'\033[1m{str(score).zfill(4)}              0000\033[1m', 'white'))
        for cannonball in calist:
            ep.stage(cannonball[0], cannonball[1], colored(' |', theme))
        ground_animation()  # bottom_separating_line
        if life == 2:
            life_two = '  '
        elif life == 1:
            life_one = '  '
        ep.stage(7, 21, colored(f'\033[1m {life}    {life_one} {life_two}   \033[1m', 'white'))
        ep.stage(23, 21, colored('\033[1mCREDIT 00\033[1m', 'white'))
        for shot in fired_laser:
            if shot[0] == rocket[0] and shot[1] == rocket[1]:
                ep.stage(shot[0], shot[1], '💥')
                ep.stage(0, 22, '')
                del shot
                system('clear')
                ep.proj()
                rocket[0] = 5
                tm.sleep(2)
                life -= 1
                if life == 0:
                    game_over()
            try:
                ep.stage(shot[0], shot[1], colored(' ☨', theme))
            except:
                pass
        ep.stage(rocket[0], rocket[1], rocket[2])
        if len(allist) == 0:
            system('clear')
            ep.proj()
            tm.sleep(2)
            break
        else:
            for alien in allist:
                if alien[1] == 18:
                    system('clear')
                    ep.proj()
                    tm.sleep(2)
                    game_over()
        system('clear')
        ep.proj()
        ep.del_stage()
        ch_theme += 1
        tm.sleep(0.007)

while True:
    try:
        ch_theme = 0
        present_color = 1
        theme = 'green'
        theme_colors = ['red','green','yellow','blue','magenta','cyan','white']

        rocket = [5, 19, '🚀']
        rocket_pitch = 3
        rocket_stride = 1
        rocket_tick = 0

        allist = []  # Creating aliens
        alien_X = 8
        alien_Y = 5
        for horde in range(52):
            allist.append([alien_X, alien_Y])
            alien_X += 2
            if alien_X == 34:
                alien_Y += 1
                alien_X = 8
        aldirection = 1
        alslowness = 18
        alstep = 0

        cacolor = theme  # Creating cannons
        calist = []
        caslowness = 1
        caspeed = 1  # Bigger number, less speed
        catick = 0

        fired_laser = []  # Creating lasers fired by aliens
        laser_slowness = 2
        fire_frequency = 2
        laser_tick = 0

        fireinterval = 8  # How frequently you can fire
        firetick = 8

        ground_list = []  # Creating ground
        ground_X = 0
        ground_Y = 20
        for ground in range(40):
            ground_list.append([ground_X, ground_Y, 2, '––'])
            ground_X += 1

        shield_list = []  # Creating shield blocks
        shield_endurance = 3
        shield_X = 3
        shield_Y = 14
        for first_layer in range(4):
            shield_X += 6
            shield_list.append([shield_X, shield_Y, shield_endurance])
            shield_X += 1
            shield_list.append([shield_X, shield_Y, shield_endurance])
        for second_third_layers in range(2):
            shield_X = 4
            shield_Y += 1
            for layer in range(4):
                shield_X += 4
                shield_list.append([shield_X, shield_Y, shield_endurance])
                for blocks in range(3):
                    shield_X += 1
                    shield_list.append([shield_X, shield_Y, shield_endurance])
        shield_X = 4
        shield_Y += 1
        for last_layer in range(4):
            shield_X += 4
            shield_list.append([shield_X, shield_Y, shield_endurance])
            shield_X += 3
            shield_list.append([shield_X, shield_Y, shield_endurance])

        ufo = []
        ufo_slowness = 3
        ufo_tick = 0
        ufo_time_start = tm.time() - 12
        main()
        ep.del_stage()
        ep.stage(9, 0, colored('\033[1mSCORE<1>           HI-SCORE           SCORE<2>\033[1m', 'white'))
        ep.stage(10, 1, colored(f'\033[1m{str(score).zfill(4)}              0000\033[1m', 'white'))
        ep.stage(7, 21, colored(f'\033[1m {life}    {life_one} {life_two}   \033[1m', 'white'))
        ep.stage(23, 21, colored('\033[1mCREDIT 00\033[1m', 'white'))
        system('clear')
        ep.proj()
        tm.sleep(1.5)
        ep.del_stage()
    except KeyboardInterrupt:
        ep.del_stage
        ep.stage(0, 45, '')
        success()
