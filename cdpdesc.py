##
## Create interface descriptions based off LLDP neighbors
## show lldp neighbor on switch
## copy/paste meat of output containing IPs and hostnames to a file
## run this script against file
## python desc.py <file>
##

import sys
import re

inputFile = sys.argv[1]

try:
	with open(inputFile) as fObj:
		cdpNeighbors = fObj.readlines()
except FileNotFoundError:
	cdpNeighbors = None

neighbors = []
alert = 1

for cdpNeighbor in cdpNeighbors:
	hostname = re.findall(r'^[^SEP|sep][a-zA-Z]{4}\w+', cdpNeighbor)

	if hostname:
		description = hostname[0].upper()
	elif re.search(r'\w\w\w\s\d+\/\d+\/\d+|\w\w\w\s\d+\/\d+', cdpNeighbor):
		localInterface, remoteInterface = re.findall(r'\w\w\w\s\d+\/\d+\/\d+|\w\w\w\s\d+\/\d+', cdpNeighbor)
		
		localInterface, localPort = re.findall(r'^\w\w|\d+\/\d+\/\d+|\d+\/\d+', localInterface)
		localInterface = f'{localInterface}{localPort}'
		
		remoteInterface, remotePort = re.findall(r'^\w\w|\d+\/\d+\/\d+|\d+\/\d+', remoteInterface)
		description = f'{description} {remoteInterface}{remotePort}'
		
		# normally only RWAs run CDP not LLDP, will combine desc.py and cdpdesc.py to one script
		# added SWDs for interface descriptions on RWAs
		if 'RWA' in description or 'SWD' in description:
			neighbors.append({'interface':localInterface, 'alert':alert, 'description':description})

for nei in neighbors:
	print('interface {0}'.format(nei['interface']))
	print('description {0}"TYPE":"LAN","MON":1,"ALERT":{1},"DESC":"{2}"{3}'.format('{', nei['alert'], nei['description'], '}'))

