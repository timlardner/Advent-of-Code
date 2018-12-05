from collections import defaultdict
import requests

puzzle = ['set a 1',
'add a 2',
'mul a a',
'mod a 5',
'snd a',
'set a 0',
'rcv a',
'jgz a -1',
'set a 1',
'jgz a -2']

puzzle = requests.get('https://aoc.intae.it/23').text.split('\n')

idx = 0
mc = 0
registers = defaultdict(int)
count = 0
last_sound = 0

#print(registers)

while idx < len(puzzle):
    #print(registers)
    count += 1
    next_instruction = puzzle[idx].split()
    #print(next_instruction)
    register = next_instruction[1]
    if len(next_instruction) == 3:
        val = next_instruction[2]
        #print(val)
        try:
            val = int(val)
        except:
            val = registers[val]
    if next_instruction[0] == 'add':
        registers[register] += val
    if next_instruction[0] == 'sub':
        registers[register] -= val
    if next_instruction[0] == 'mul':
        registers[register] *= val
        mc += 1
    if next_instruction[0] == 'mod':
        registers[register] %= val
    if next_instruction[0] == 'set':
        registers[register] = val
    if next_instruction[0] == 'jnz':
        if registers[register] != 0:
            idx += val
            #print('Jumping')
            #print(idx)
            continue
    if next_instruction[0] == 'jgz':
        if registers[register] > 0:
            idx += val
            #print('Jumping')
            #print(idx)
            continue
    idx += 1

print(mc)


