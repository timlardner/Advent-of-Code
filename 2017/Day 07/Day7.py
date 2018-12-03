import requests

input = requests.get('https://aoc.intae.it/7').text

lines = input.split('\n')

name_list = []
link_list = []

for line in lines:
	splitline = line.split('->')
	name_list.append(splitline[0].split()[0])
	if len(splitline) > 1:
		links = splitline[1].split(',')
		for link in links:
			link_list.append(link.strip())
			
for name in name_list:
	if name not in link_list:
		print(name)

