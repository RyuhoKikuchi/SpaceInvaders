from emoji_projection import stage, del_stage, proj
from termcolor import colored


shield_list = []
shield_endurance = 2
shield_X = 3
shield_Y = 14

for first_layer in range(4):
	shield_X += 6
	shield_list.append([shield_X, shield_Y])
	shield_X += 1
	shield_list.append([shield_X, shield_Y])
for second_third_layers in range(2):
	shield_X = 4
	shield_Y += 1
	for layer in range(4):
		shield_X += 4
		shield_list.append([shield_X, shield_Y])
		for blocks in range(3):
			shield_X += 1
			shield_list.append([shield_X, shield_Y])
shield_X = 4
shield_Y += 1
for last_layer in range(4):
	shield_X += 4
	shield_list.append([shield_X, shield_Y])
	shield_X += 3
	shield_list.append([shield_X, shield_Y])

for visualize in shield_list:
	stage(visualize[0], visualize[1], colored('〓', 'magenta'))
proj()
del_stage()