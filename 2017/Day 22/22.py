import requests
from datetime import datetime

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 0
        
    def infect(self):
        self.state = 2
        
        
    def toggle_infection(self):
        self.state += 1
        self.state %= 4
        return 1 if self.state == 2 else 0 

class NodeManager:
    def __init__(self, puzzle, debug=False):
        self.nodes = {}
        self.debug = debug
        self.build_map_from_input(puzzle)
        
    def get_key(self, x, y):
        return '{},{}'.format(x, y)
        
    def add_at(self, x, y, infected=False, key=None):
        new_node = Node(x, y)
        if not key:
            key = self.get_key(x, y)
        if infected:
            new_node.infect()
        self.nodes[key] = new_node
        return new_node
        
    def get_node(self, x, y):
        key = self.get_key(x, y)
        if key in self.nodes:
            return self.nodes[key]
        
        new_node = self.add_at(x, y, key=key)
        return new_node
    
    def build_map_from_input(self, puzzle):
        origin = int((len(puzzle.split('\n')[0])-1)/2)
        lines = puzzle.split('\n')
        for y_idx, line in enumerate(lines):
            y_pos = y_idx - origin
            for x_idx, char in enumerate(list(line)):
                x_pos = x_idx - origin
                if self.debug:
                    print('Adding {} at ({},{})'.format(char, x_pos, y_pos))
                infected = char == '#'
                self.add_at(x_pos, y_pos*-1, infected=infected)
                
    def print_range(self, to_print):
        def state_to_char(state):
            if state == 0:
                return '.'
            elif state == 1:
                return 'W'
            elif state == 2:
                return '#'
            elif state == 3:
                return 'F'
        output = ''
        for y_pos in range(-to_print, to_print+1):
            for x_pos in range(-to_print, to_print+1):
                output += state_to_char(self.get_node(x_pos, y_pos*-1).state)
            output += '\n'
        print(output)
                
class Virus:
    def __init__(self, nodes):
        self.nodes = nodes
        self.x = 0
        self.y = 0
        self.direction = 0 # 0 is up, 1 is right, 2 is down, 3 is left
        self.infection_counter = 0
        
    def step(self):
        current_node = self.nodes.get_node(self.x, self.y)
        self.direction = self.direction + current_node.state -1
        self.direction %= 4 # Ensure we're using one of the 4 allowed directions
        if self.nodes.debug:
            print('State is {}'.format(current_node.state))
            print('New direction is {}'.format(self.direction))
        
        self.infection_counter += current_node.toggle_infection()
        self.move()
    
    def move(self):
        if self.direction == 0:
            self.y += 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y -= 1
        elif self.direction == 3:
            self.x -= 1
        
    def do_steps(self, n_steps):
        for _ in range(n_steps):
            self.step()
        return self.infection_counter

puzzle = """..#
#..
..."""

puzzle = requests.get('https://aoc.intae.it/22').text

nm = NodeManager(puzzle, debug=False)
virus = Virus(nm)
start = datetime.now()
print(virus.do_steps(10000000))
print('Completed run in {} seconds'.format((datetime.now() - start).total_seconds()))
#nm.print_range(30)
