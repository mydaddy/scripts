#
## ssh to 10.252.30.10 (Aruba 8.5 master)
## no paging
## show switches
## copy/paste meat of output containing IPs and hostnames to a file
## run this script against file
## python dns_check.py <file>
#

import os
import subprocess
import sys
import re

inputFile = sys.argv[1]

try:
	with open(inputFile) as fObj:
		ArubaOS8Cntrls = fObj.read()
except FileNotFoundError:
	ArubaOS8Cntrls = None

regex = r"^(\d+.\d+.\d+.\d+)\s+None\s+(\w+)"
matches = re.finditer(regex, ArubaOS8Cntrls, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
	# print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

	# print(match.groups()[0], match.groups()[1])
	
	cmd = 'nslookup ' + match.groups()[1]
	
	# os.system(cmd)
	
	# subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	
	# with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
		# print(proc.stdout.read())

	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# print(proc.stdout.read())

	nslookupError = proc.stderr.read()

	if nslookupError:
		print('Failed: match.groups()[1]')
	# else:
		# print('All good!')
	
	# break
	
	# for groupNum in range(0, len(match.groups())):
		# groupNum = groupNum + 1

		# print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

