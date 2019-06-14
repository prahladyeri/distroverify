import requests
import argparse
import os, sys
import time
import hashlib
import json
import re
from distroverify import __title__, __description__, __version__

patterns = {
	'ubuntu-mate': r'ubuntu-mate-(.*)-(.*)-(.*)\.iso',
}
urls = {
	'ubuntu-mate': 'http://cdimage.ubuntu.com/ubuntu-mate/releases/%s/release/SHA1SUMS',
}

def fileexists(filepath):
	try:
		if os.path.isfile(filepath):
			return filepath
		else:
			print("There is no file at:" + filepath)
			exit()
	except Exception as ex:
			print(ex)

def verify(distro, release_version, file_name, full_file_name):
	if distro == 'ubuntu-mate':
		url = urls[distro] % release_version
	print('verifyication url:', url)
	print('calculating file hash...')
	hash = hashlib.sha1()
	with open(full_file_name,'rb') as fp:
		for chunk in iter(lambda: fp.read(4096), b""):
			hash.update(chunk)
	strhash = hash.hexdigest()
	strhash = strhash.strip()
	print('done')
	resp = requests.get(url)
	urlhash = resp.text.split(" ")[0]
	print('response hash:',urlhash)
	print('calculated hash:', strhash)
	print('match: ', urlhash == strhash)

def main():
	banner = """%s version %s
%s

Copyright (c) 2019 Prahlad Yeri.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
""" % (__title__, __version__, __description__)
	print(banner)
	parser = argparse.ArgumentParser()
	parser.add_argument('distro_file', type=fileexists, help='Distro File Location EX: /Desktop/Somewhere/ubuntu-mate-19.04-desktop-amd64.iso')
	parser.add_argument('-v', '--version', help='Version', action='store_true')
	args = parser.parse_args()
	
	if args.version:
		sys.exit()
	
	full_file_name = args.distro_file
	args.distro_file = os.path.basename(args.distro_file)
	for distro in patterns.keys():
		pattern = patterns[distro]
		match = re.match(pattern, args.distro_file)
		#print(match)
		if match != None:
			break

	if match == None:
		print("Filename pattern doesn't match with any distros. Currently, we support only ubuntu.")
		sys.exit()
	else:
		print("match success: ", distro)
		release_version = match.groups()[0]
		ds = match.groups()[1]
		arch = match.groups()[2]
		# print("release_version: %s" % release_version)
		# print("ds: %s" % ds)
		# print("arch: %s" % arch)
		verify(distro, release_version, args.distro_file, full_file_name)
		sys.exit()

	#calculate hash of file
	hash = hashlib.sha1()
	with open(args.distro_file,'rb') as fp:
		for chunk in iter(lambda: fp.read(4096), b""):
			hash.update(chunk)
	strhash = hash.hexdigest()
		
		
	#scan(strhash.strip(), args.log_output) #args.verbose

if __name__ == "__main__":
	main()