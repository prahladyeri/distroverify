import requests
import argparse
import os, sys
import time
import hashlib
import json
import re
from distroverify import __title__, __description__, __version__

# examples:
# openSUSE-Leap-15.1-KDE-Live-x86_64-Current.iso
# openSUSE-Leap-15.1-GNOME-Live-x86_64-Current.iso
# debian-live-9.9.0-amd64-gnome.iso
# ubuntu-16.04.6-desktop-i386.iso
# ubuntu-16.04.6-server-i386.iso

patterns = {
	'ubuntu-mate': r'ubuntu-mate-(.*)-(.*)-(.*)\.iso',
	'ubuntu-gnome': r'ubuntu-gnome-(.*)-(.*)-(.*)\.iso',
	'xubuntu': r'xubuntu-(.*)-(.*)-(.*)\.iso',
	'lubuntu': r'lubuntu-(.*)-(.*)-(.*)\.iso',
	'ubuntu': r'ubuntu-(.*)-(.*)-(.*)\.iso',
	'opensuse-leap': r'openSUSE-Leap-(.*)-(.*)-(.*)-(.*)-Current\.iso',
}
urls = {
	'ubuntu-mate': 'http://cdimage.ubuntu.com/ubuntu-mate/releases/%s/release/SHA1SUMS',
	'ubuntu-gnome': 'http://cdimage.ubuntu.com/ubuntu-gnome/releases/%s/release/SHA1SUMS',
	'xubuntu': 'http://cdimage.ubuntu.com/xubuntu/releases/%s/release/SHA1SUMS',
	'lubuntu': 'http://cdimage.ubuntu.com/lubuntu/releases/%s/release/SHA1SUMS',
	'ubuntu': 'http://cdimage.ubuntu.com/ubuntu/releases/%s/release/SHA1SUMS',
	'opensuse-leap': 'https://download.opensuse.org/distribution/leap/%s/%s/'
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

def verify(match, distro, file_name, full_file_name):
	# print("release_version: %s" % release_version)
	# print("ds: %s" % ds)
	# print("arch: %s" % arch)

	if distro in ['ubuntu', 'ubuntu-mate', 'xubuntu', 'kubuntu', 'lubuntu', 'ubuntu-budgie', 'ubuntu-gnome', 'ubuntu-core', 'ubuntu-server', 'ubuntu-touch', 'ubuntu-touch-custom', 'ubuntu-kylin', 'ubuntu-studio']:
		ver = match.groups()[0]
		typ = match.groups()[1]
		arch = match.groups()[2]
		url = urls[distro] % ver
		print("version: %s, type: %s, arch: %s" % (ver, typ, arch))
	elif distro == 'opensuse-leap':
		ver = match.groups()[0]
		typ = match.groups()[1]
		dist = match.groups()[2]
		arch = match.groups()[3]
		url = (urls[distro] % (ver, dist.lower())) + file_name + ".sha1"
		print("version: %s, type: %s, dist: %s, arch: %s" % (ver, typ, dist, arch))
	else:
		print("unknown distro")
		return
	print('verification url:', url)
	print('calculating hash...')
	hash = hashlib.sha1()
	with open(full_file_name,'rb') as fp:
		for chunk in iter(lambda: fp.read(4096), b""):
			hash.update(chunk)
	strhash = hash.hexdigest()
	strhash = strhash.strip()
	print('done. fetching official hash')
	resp = requests.get(url)
	ss = resp.text
	#print(ss.split("\n"))
	is_found = False
	if distro in ['opensuse-leap']:
		urlhash = ss.split(" ")[0]
		is_found = True
		# print('ss.split():', ss.split())
		# for line in ss.split():
			# if file_name in line:
				# is_found = True
				# urlhash = line.split()[0]
				# break
	else: # ubuntu family of distros
		for item in ss.split("\n"):
			if item.endswith(file_name):
				urlhash = item.split(" ")[0]
				is_found = True
				break
	if is_found:
		is_correct = (urlhash == strhash)
		print('calculated hash:', strhash)
		print('response hash:',urlhash)
		print('match: ', is_correct)
		return is_correct
	else:
		print("hash not found in the response file")
		return

def process(args):
	if '-v' in args or '--version' in args:
		print("%s version %s" % (__title__, __version__))
		return
	parser = argparse.ArgumentParser()
	parser.add_argument('distro_file', type=fileexists, help='Distro File Location EX: /Desktop/Somewhere/ubuntu-mate-19.04-desktop-amd64.iso')
	parser.add_argument('-v', '--version', help='Version', action='store_true')
	args = parser.parse_args(args)
	
	full_file_name = args.distro_file
	args.distro_file = os.path.basename(args.distro_file)
	for distro in patterns.keys():
		pattern = patterns[distro]
		match = re.match(pattern, args.distro_file)
		if match != None:
			#print('match: ', match, 'distro: ', distro)
			break

	if match == None:
		print("Filename pattern doesn't match with any distros.")
		return None
	else:
		print("match success: ", distro)
		return verify(match, distro, args.distro_file, full_file_name)

def main():
	process(sys.argv[1:])

if __name__ == "__main__":
	main()