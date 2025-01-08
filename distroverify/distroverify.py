""" Script to verify integrity of a given .iso file

"""
import requests
import argparse
import os, sys
import time
import hashlib
import json
import re
from urllib.parse import urlparse
from distroverify import __title__, __description__, __version__

""" 
Examples:

 openSUSE-Leap-15.1-KDE-Live-x86_64-Current.iso
 openSUSE-Leap-15.1-GNOME-Live-x86_64-Current.iso
 ubuntu-16.04.6-desktop-i386.iso
 ubuntu-16.04.6-server-i386.iso
 linuxmint-19.1-mate-64bit
 debian-live-9.9.0-amd64-gnome.iso
 debian-9.3.0-amd64-DVD-1.iso
 Fedora-Workstation-Live-x86_64-30-1.2.iso
 Fedora-Workstation-netinst-x86_64-30-1.2.iso

https://download.fedoraproject.org/pub/fedora/linux/releases/30/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-30-1.2.iso
https://download.fedoraproject.org/pub/fedora/linux/releases/30/Server/x86_64/iso/Fedora-Server-dvd-x86_64-30-1.2.iso
https://ftp.heanet.ie/mirrors/linuxmint.com/stable/19.1/sha256sum.txt
"""

colors = { 
    "red": "\033[1;31m",
    "blue": "\033[1;34m",
    "cyan": "\033[1;36m",
    "green": "\033[0;32m",
    "reset": "\033[0;0m",
    "bold": "\033[;1m",
    "reverse": "\033[;7m",
    'black': '\x1b[30m',
    'magenta': '\x1b[35m',
    'white': '\x1b[37m',
    'yellow': '\x1b[33m',   
}

patterns = {
    'ubuntu-mate': r'ubuntu-mate-(.*)-(.*)-(.*)\.iso',
    'ubuntu-gnome': r'ubuntu-gnome-(.*)-(.*)-(.*)\.iso',
    'xubuntu': r'xubuntu-(.*)-(.*)-(.*)\.iso',
    'lubuntu': r'lubuntu-(.*)-(.*)-(.*)\.iso',
    'ubuntu': r'ubuntu-(.*)-(.*)-(.*)\.iso',
    'opensuse-leap': r'openSUSE-Leap-(.*)-(.*)-(.*)-(.*)-Current\.iso',
    'linuxmint': 'linuxmint-(.*)-(.*)-(.*).iso',
    'debian-live': 'debian-live-(.*)-(.*)-(.*).iso',
    'debian-dvd': 'debian-(.*)-(.*)-DVD-(.*).iso',
    'fedora-live': 'Fedora-Workstation-Live-(.*)-(.*)-(.*).iso',
    'fedora-netinst': 'Fedora-Workstation-netinst-(.*)-(.*)-(.*).iso',
}

urls =  {
    'ubuntu-mate': 'http://cdimage.ubuntu.com/ubuntu-mate/releases/%s/release/SHA256SUMS',
    'ubuntu-gnome': 'http://cdimage.ubuntu.com/ubuntu-gnome/releases/%s/release/SHA256SUMS',
    'xubuntu': 'http://cdimage.ubuntu.com/xubuntu/releases/%s/release/SHA256SUMS',
    'lubuntu': 'http://cdimage.ubuntu.com/lubuntu/releases/%s/release/SHA256SUMS',
    'ubuntu': 'https://cdimage.ubuntu.com/ubuntu/releases/%s/release/SHA256SUMS',
    'opensuse-leap': 'https://download.opensuse.org/distribution/leap/%s/%s/%s.sha256',
    'linuxmint': 'https://mirror.dogado.de/linuxmint-cd/stable/%s/sha256sum.txt',
    'debian-live': {
        'archive': 'https://cdimage.debian.org/mirror/cdimage/archive/{ver}-live/{arch}/iso-hybrid/SHA256SUMS',
        'release': 'https://cdimage.debian.org/mirror/cdimage/release/{ver}-live/{arch}/iso-hybrid/SHA256SUMS'
    },
    'debian-dvd': {
        'archive': 'https://cdimage.debian.org/mirror/cdimage/archive/{ver}/{arch}/iso-dvd/SHA256SUMS',
        'release': 'https://cdimage.debian.org/mirror/cdimage/release/{ver}/{arch}/iso-dvd/SHA256SUMS'
    },
    'fedora-live': 'https://mirrors.tuna.tsinghua.edu.cn/fedora/releases/{ver}/Workstation/{arch}/iso/Fedora-Workstation-{ver}-{sver}-{arch}-CHECKSUM',
    'fedora-netinst': 'https://mirrors.tuna.tsinghua.edu.cn/fedora/releases/{ver}/Workstation/{arch}/iso/Fedora-Workstation-{ver}-{sver}-{arch}-CHECKSUM',
}

# ubuntu_releases_url = "http://releases.ubuntu.com/{ver}/SHA256SUMS"
# ubuntu_old_releases_url = "http://old-releases.ubuntu.com/releases/{ver}/SHA256SUMS" #ubuntu-18.04.4-live-server-amd64.iso

ubuntu_alt_releases_urls = [
    "http://releases.ubuntu.com/{ver}/SHA256SUMS",
    "http://old-releases.ubuntu.com/releases/{ver}/SHA256SUMS",
]

def fileexists(filepath):
    """Check for existence of a file
    
    :param filepath: Full path to a file
    :return: Full path to the file if it exists, None otherwise
    """
    try:
        if os.path.isfile(filepath):
            return filepath
        else:
            print("There is no file at:" + filepath)
            exit()
    except Exception as ex:
            print(ex)

def verify(match, distro, file_name, full_file_name, get_download_link=False):
    """Verify the matched distro file for its integrity.
    
    :param match: Matched regex value
    :param distro: Matched distro
    :param file_name: Distro file basename
    :param full_file_name: Full Path to distro file
    :return: True if verification succeeds, False if it fails, None if distro couldn't be verified
    """
    if distro in ['ubuntu', 'ubuntu-mate', 'xubuntu', 'kubuntu', 'lubuntu', 'ubuntu-budgie', 'ubuntu-gnome', 'ubuntu-core', 'ubuntu-server', 'ubuntu-touch', 'ubuntu-touch-custom', 'ubuntu-kylin', 'ubuntu-studio']:
        ver = match.groups()[0]
        typ = match.groups()[1]
        arch = match.groups()[2]
        url = urls[distro] % ver
        print("version: %s, type: %s, arch: %s" % (ver, typ, arch))
    elif distro == 'linuxmint':
        ver = match.groups()[0]
        typ = match.groups()[1]
        arch = match.groups()[2]
        #url = (urls[distro] % (ver, typ, arch))
        url = urls[distro] % ver
        print("version: %s, type: %s, arch: %s" % (ver, typ, arch))
    elif distro == 'opensuse-leap':
        ver = match.groups()[0]
        typ = match.groups()[1]
        dist = match.groups()[2]
        arch = match.groups()[3]
        url = (urls[distro] % (ver, dist.lower(), file_name))
        print("version: %s, type: %s, dist: %s, arch: %s" % (ver, typ, dist, arch))
    elif distro == 'debian-live':
        ver = match.groups()[0]
        arch = match.groups()[1]
        typ = match.groups()[2]
        #arch = match.groups()[3]
        url = urls[distro] #(urls[distro] % (ver, dist.lower(), file_name))
        print("version: %s, type: %s, arch: %s" % (ver, typ, arch))
    elif distro == 'debian-dvd':
        ver = match.groups()[0]
        arch = match.groups()[1]
        dvdnum = match.groups()[2]
        #typ = match.groups()[3]
        #arch = match.groups()[3]
        url = urls[distro] #(urls[distro] % (ver, dist.lower(), file_name))
        print("version: %s, arch: %s, dvdnum: %s" % (ver, arch, dvdnum))
    elif distro in ['fedora-live', 'fedora-netinst']:
        arch = match.groups()[0]
        ver = match.groups()[1]
        sver = match.groups()[2]
        url = urls[distro].format(ver=ver, sver=sver, arch=arch)
        print("version: %s, subversion: %s, arch: %s" % (ver, sver, arch))
    else:
        print("unknown distro")
        return
    
    if get_download_link:
        print("fetching dl link:")
        if distro not in ['debian-live', 'debian-dvd']:
            parts = urlparse(url)
            base = parts.path.split('/')[:-1]
            base = "/".join(base)
            new_url = parts.scheme + "://" + parts.netloc +  base
            new_url += "/" + file_name
            print(new_url)
        else:
            pass
        return
        
    print('verification url(s):', url)
    print('calculating hash...')
    hash = hashlib.sha256()
    with open(full_file_name,'rb') as fp:
        for chunk in iter(lambda: fp.read(4096), b""):
            hash.update(chunk)
    strhash = hash.hexdigest()
    strhash = strhash.strip()

    print(colors['blue'])
    print(strhash)
    print('fetching official hash...')
    
    if distro in ['debian-live', 'debian-dvd']:
        print("trying archive url...")
        turl = url['archive'].format(ver=ver, arch=arch)
        resp = requests.get(turl)
        if resp.status_code == 404:
            print("failed. now trying release url...")
            turl = url['release'].format(ver=ver, arch=arch)
            resp = requests.get(turl)
            if resp.status_code == 404:
                print("failed. looks like they don't have this anymore!")
                return
            else:
                print("success")
        else:
            print("success")
    else:
        resp = requests.get(url)
    
    #ss = resp.text
    status_code = resp.status_code
    is_found = False
    if distro in ['fedora-live', 'fedora-netinst']:
        for line in resp.text.splitlines():
            if file_name in line and line.startswith("SHA256 ("):
                #line.split("SHA256 (")[1].split(")")[0]
                urlhash = line.split("=")[1].strip()
                is_found = True
                break
    elif distro in ['opensuse-leap']:
        urlhash = resp.text.splitlines()[3].strip()
        is_found = True
    else: # ubuntu family, linuxmint, debian-live, debian-dvd
        for item in resp.text.splitlines():
            if item.endswith(file_name):
                urlhash = item.split(" ")[0]
                is_found = True
                break
    if distro == 'ubuntu' and is_found == False:
        print('trying alt releases url(s)...')
        for alt_url in ubuntu_alt_releases_urls:
            url = alt_url.format(ver=ver)
            print("trying:", url)
            resp = requests.get(url)
            for item in resp.text.splitlines():
                if item.endswith(file_name):
                    urlhash = item.split(" ")[0]
                    is_found = True
                    break
        if not is_found: # try replacing "_live" in the version
            for alt_url in ubuntu_alt_releases_urls:
                url = alt_url.format(ver=ver.replace("-live", ""))
                print("trying:", url)
                resp = requests.get(url)
                for item in resp.text.splitlines():
                    if item.endswith(file_name):
                        urlhash = item.split(" ")[0]
                        is_found = True
                        break
    if is_found:
        is_correct = (urlhash == strhash)
        print(colors['green'] if is_correct else colors['red'])
        print('calculated hash:', strhash)
        print('official hash:',urlhash)
        print('match: ', is_correct)
        if is_correct:
            print("looks like {fname} is genuine".format(fname=file_name))
        else:
            print("looks like {fname} is not genuine".format(fname=file_name))
        return is_correct
    else:
        print("hash not found in the response file")

def main(args=[]):
    """Main entry point of script, process given args using argparse module
    
    :param args: List of arguments to be processed
    """
    if len(args) == 0:
        args = sys.argv[1:]        
    # if '-v' in args or '--version' in args:
        # print("%s version %s" % (__title__, __version__))
        # return
    parser = argparse.ArgumentParser(epilog="examples:\n distroverify /Desktop/Somewhere/ubuntu-mate-19.04-desktop-amd64.iso\n distroverify ubuntu-mate-19.04-desktop-amd64", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('distro_file', help='Distro name or filename')
    parser.add_argument('-dl', '--download-link', help='Show download links for named distro instead', action='store_true')
    # parser.add_argument('-n', '--name-of-distro',help='Name of distro to download (EX: ubuntu-mate-19.04-desktop-amd64)', default='')
    parser.add_argument('-v', '--version', help='Version', action='store_true')
    args = parser.parse_args(args)
    
    if args.version:
        print("%s version %s" % (__title__, __version__))
        return
    elif args.download_link:
        for distro in patterns.keys():
            pattern = patterns[distro]
            match = re.match(pattern, args.distro_file + ".iso")
            if match != None:
                verify(match, distro, args.distro_file + ".iso", args.distro_file + ".iso", True)
                print(colors['reset'])
        print("pattern doesn't match with any distros known to me")
        return
    
    if args.distro_file == "":
        print("distro_file argument cannot be blank")
        return
    elif not os.path.isfile(args.distro_file):
        print("No file exists at:", args.distro_file)
        return
    
    full_file_name = args.distro_file
    args.distro_file = os.path.basename(args.distro_file)
    for distro in patterns.keys():
        pattern = patterns[distro]
        match = re.match(pattern, args.distro_file)
        if match != None:
            break

    if match == None:
        print("pattern doesn't match with any distros known to me")
        return None
    else:
        print("distro detected: ", distro)
        verify(match, distro, args.distro_file, full_file_name)
        print(colors['reset'])

if __name__ == "__main__":
    main()
