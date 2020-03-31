import sys
import re

inputFile = sys.argv[1]

try:
	with open(inputFile) as fObj:
		lldpNeighbors = fObj.readlines()
except FileNotFoundError:
	lldpNeighbors = None

neighbors = []

for lldpNeighbor in lldpNeighbors:
	# hostname, localInterface, remoteInterface = re.findall(r'^\w+|\w\w\d+/\d+/\d+|\w\w\d+/\d+', lldpNeighbor)
	
	hostname = re.findall(r'^\w+', lldpNeighbor)[0].upper()
	
	# and len(hostname) > 12
	if not 'SEP' in hostname:
		if 'WAP' in hostname:
			alert = 0
			localInterface = re.findall(r'\w\w\d+/\d+/\d+|\w\w\d+/\d+', lldpNeighbor)[0]
			description = hostname
		elif re.match(r'^VL\d{1,2}$', hostname):
			alert = 1
			localInterface = hostname.replace('VL', 'Vlan')
			description = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\w+$', lldpNeighbor)[0]
		else:
			alert = 1
			localInterface, remoteInterface = re.findall(r'\w\w\d+/\d+/\d+|\w\w\d+/\d+', lldpNeighbor)
			description = '{0} {1}'.format(hostname, remoteInterface)

		neighbors.append({'interface':localInterface, 'alert':alert, 'description':description})

for nei in neighbors:
	print('interface {0}'.format(nei['interface']))
	print('description {0}"TYPE":"LAN","MON":1,"ALERT":{1},"DESC":"{2}"{3}'.format('{', nei['alert'], nei['description'], '}'))

