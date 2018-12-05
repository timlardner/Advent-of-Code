from copy import deepcopy
import requests

puzzle = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""

puzzle = requests.get('https://aoc.intae.it/24').text

bridges = []

def create_nodes(puzzle):
    extra_node = Node('0/0')
    return [extra_node] + [Node(line) for line in puzzle.split('\n')]

class Node:
    def __init__(self, string):
        tmp = string.split('/')
        self.left = int(tmp[0].strip())
        self.right = int(tmp[1].strip())
        
        self.left_next = None
        self.right_next = None
        self.next = None
        
    def available(self):
        avail = []
        if self.left_next == None:
            avail.append(self.left)
        if self.right_next == None:
            avail.append(self.right)
        return avail

    def join(self, node):
        self.next = node
        #print('Joining {} to {}'.format(self, node))
        if self.left_next is None and self.left in node.available():
            self.left_next = node
            if self.left == node.left:
                node.left_next = self
                #print('Attached left of {} to left of previous node'.format(node))
            else:
                node.right_next = self
                #print('Attached right of {} to left of previous node'.format(node))
        else:
            self.right_next = node
            if node.left_next == None and self.right == node.left:
                node.left_next = self
                #print('Attached left of {} to right of previous node'.format(node))
            else:
                node.right_next = self
                #print('Attached right of {} to right of previous node'.format(node))
        #print(node.available())
        
    def get_total(self):
        return self.left + self.right
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.left == other.left and self.right == other.right
    
    def __str__(self):
        return '{},{}'.format(self.left, self.right)
        
class Bridge:
    def __init__(self):
        self.nodes = []
        
    def add(self, node):
        if self.nodes:
            if not self.can_join(node):
                raise Exception('Cannot join these nodes')
            self.nodes[-1].join(node)
        self.nodes.append(node)
        
    def can_join(self, node):
        avail = self.nodes[-1].available()
        #print('Checking to see if {} is in the node {}'.format(avail, node))
        return (node.left in avail or node.right in avail)
    
    def __str__(self):
        if not self.nodes:
            return 'Empty bridge'
        return ' -> '.join([str(node) for node in self.nodes])
    
    def get_level(self):
        level = 0
        this_node = self.nodes[0]
        while this_node:
            level += this_node.get_total()
            this_node = this_node.next
        return level
        

def do_next(bridge, available_nodes, level):
    old_bridge = deepcopy(bridge)
    available_nodes = deepcopy(available_nodes)
    #print(old_bridge)
    nodes_we_can_join = [node for node in available_nodes if old_bridge.can_join(node)]
    if not nodes_we_can_join:
        bridges.append(old_bridge)
        #print('Reached end at {}'.format(old_bridge))
        return
    for node in nodes_we_can_join:
        #print([str(node) for node in nodes_we_can_join])
        #print('Joining {} to end of list'.format(node))
        next_bridge = deepcopy(old_bridge)
        next_bridge.add(node)
        available_nodes.remove(node)
        do_next(next_bridge, available_nodes, level+1)
    
nodes = create_nodes(puzzle)
for start_point in nodes:
    available_nodes = deepcopy(nodes) 
    bridge = Bridge()
    available_nodes.remove(start_point)
    bridge.add(start_point)
    do_next(bridge, available_nodes, 0)
    # Only run once
    break
    
best_level = 0
best_bridge = None
for iter_bridge in bridges:
    level = iter_bridge.get_level()
    if level > best_level:
        best_level = level
        best_bridge = iter_bridge
print(best_level)
print(best_bridge)
