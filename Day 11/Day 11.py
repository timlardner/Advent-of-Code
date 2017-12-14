import requests
import matplotlib.pyplot as plt

def steps_home(current_position):
	n_x_steps = abs(current_position['x']) / 0.5
	n_y_steps = max(abs(current_position['y']) - abs(current_position['x']), 0)
	steps = int(n_x_steps + n_y_steps)
	return steps

string = requests.get('https://aoc.intae.it/11').text
path = string.split(',')
start = {'x': 0, 'y': 0}
furthest = 0
x = []
y = []

current_position = start
for step in path:
	if step == 'ne':
		current_position['x'] += 0.5
		current_position['y'] += 0.5
	if step == 'n':
		current_position['y'] += 1.0
	if step == 'nw':
		current_position['x'] -= 0.5
		current_position['y'] += 0.5
	if step == 'sw':
		current_position['x'] -= 0.5
		current_position['y'] -= 0.5
	if step == 's':
		current_position['y'] -= 1.0
	if step == 'se':
		current_position['x'] += 0.5
		current_position['y'] -= 0.5
	x.append(current_position['x'])
	y.append(current_position['y'])
	furthest = max(furthest, steps_home(current_position))
		
	
print(steps_home(current_position))
print(furthest)

plt.scatter(x, y)
plt.show()

