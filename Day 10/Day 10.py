import requests

lengths = [ord(x.strip()) for x in requests.get('https://aoc.intae.it/10').text]

lengths += [17, 31, 73, 47, 23]
numbers = list(range(256))

skip_size = 0
index = 0
n_rounds = 64

def compute_hash(array, num=16):
	new_hash = []
	idx = 0
	width = 16
	for _ in range(num):
		result = 0
		for item in array[idx:idx+width]:
			result ^= item
		new_hash.append(result)
		idx += width
	return new_hash

def pick_array(array, index, length):
	new_list = []
	while len(new_list)<length:
		index = index % len(array)
		new_list.append(array[index])
		index += 1
	return new_list
	
def put_array(array, index, to_reverse):
	while to_reverse:
		index = index % len(array)
		array[index] = to_reverse.pop()
		index += 1
	return array
	
for round in range(n_rounds):	
	for item in lengths:
		to_reverse = pick_array(numbers, index, item)
		numbers = put_array(numbers, index, to_reverse)
		index = index + item + skip_size
		skip_size += 1

#print(numbers[0] * numbers[1])
hash = compute_hash(numbers)
print(len(hash))
hex = ['{:02x}'.format(x) for x in hash]
print(''.join(hex))

test = '65 ^ 27 ^ 9 ^ 1 ^ 4 ^ 3 ^ 40 ^ 50 ^ 91 ^ 7 ^ 6 ^ 0 ^ 2 ^ 5 ^ 68 ^ 22'
test = [int(x.strip()) for x in test.split('^')]
print(test)
print(compute_hash(test, 1))
