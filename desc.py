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
		lldpNeighbors = fObj.readlines()
except FileNotFoundError:
	lldpNeighbors = None

neighbors = []

for lldpNeighbor in lldpNeighbors:
	# hostname, localInterface, remoteInterface = re.findall(r'^\(^[^SEP][a-zA-Z]+\d{1,})|(\w\w\d+\/\d+\/\d+)|(\w\w\d+\/\d+)', lldpNeighbor)
	# (^[^SEP][a-zA-Z]+\d{1,})|(\w\w\d+\/\d+\/\d+)|(\w\w\d+\/\d+)		- begining with alpha (not SEP), unlimited length, with at least 1 or more digits	// can do Vlan interfaces but easier to pick up other crap
	# (^[^SEP][a-zA-Z]{10}\d{0,})|(\w\w\d+\/\d+\/\d+)|(\w\w\d+\/\d+)	- begining with alpha (not SEP), at least 10 or more, can have digits or not		// can't do Vlan interfaces with this
	# other portions of regex
	# (\w\w\d+\/\d+\/\d+)	- example Gi1/0/1 or Te1/1/1
	# (\w\w\d+\/\d+)		- example Gi0/1 or Fa0/1
	
	# need to figure out how to handle Vlans and other misc crap
	# maybe pass an argument for Vlans like -vlan or create a seperate script since that output comes from show int desc, not from show lldp nei
	# also need to handle show cdp nei output
	
	# hostname = re.findall(r'^[^SEP][a-zA-Z]+\d{1,}', lldpNeighbor) - failed on CENCO225
	hostname = re.findall(r'^[^SEP|sep][a-zA-Z]{4}\w+', lldpNeighbor) # added lowercase sep for phones and first 5 chars of hostname are alpha

	if hostname:
		hostname = hostname[0].upper()

		if 'WAP' in hostname:
			alert = 0
			localInterface = re.findall(r'\w\w\d+/\d+/\d+|\w\w\d+/\d+', lldpNeighbor)[0]
			description = hostname
		elif re.match(r'^VL\d{1,2}$', hostname): # maybe use re.search instead?
			alert = 1
			localInterface = hostname.replace('VL', 'Vlan')
			description = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\w+$', lldpNeighbor)[0]
		elif re.search(r'\w\w\w\s\d+\/\d+\/\d+|\w\w\w\s\d+\/\d+', lldpNeighbor): # WTF is this for?
			print('!!! FOUND ONE !!!')
		else:
			alert = 1
			localInterface, remoteInterface = re.findall(r'\w\w\d+/\d+/\d+|\w\w\d+/\d+', lldpNeighbor)
			description = '{0} {1}'.format(hostname, remoteInterface)

		neighbors.append({'interface':localInterface, 'alert':alert, 'description':description})

for nei in neighbors:
	print('interface {0}'.format(nei['interface']))
	print('description {0}"TYPE":"LAN","MON":1,"ALERT":{1},"DESC":"{2}"{3}'.format('{', nei['alert'], nei['description'], '}'))

