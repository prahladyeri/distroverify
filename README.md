![pypi](https://img.shields.io/pypi/v/distroverify.svg)
![license](https://img.shields.io/github/license/prahladyeri/distroverify.svg)
![last-commit](https://img.shields.io/github/last-commit/prahladyeri/distroverify.svg)
![docs](https://readthedocs.org/projects/distroverify/badge/?version=latest)
[![donate](https://img.shields.io/badge/-Donate-blue.svg?logo=paypal)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JM8FUXNFUK6EU)
[![follow](https://img.shields.io/twitter/follow/prahladyeri.svg?style=social)](https://twitter.com/prahladyeri)

# distroverify

![project logo](https://raw.githubusercontent.com/prahladyeri/distroverify/master/logo.png)

Utility to verify any linux distro file (*.iso) for its integrity.

# Installation

	pip install distroverify

# Usage

	> distroverify ubuntu-mate-16.04.5-desktop-amd64.iso
	Distro Verify version 1.0.1
	Utility to verify any linux distro file (*.iso) for its integrity

	match success:  ubuntu-mate
	verification url: http://cdimage.ubuntu.com/ubuntu-mate/releases/16.04.5/release/SHA1SUMS
	calculating hash...
	done
	response hash: 2ace65436195d122b8ce0cfc106728c2922dd350
	calculated hash: 2ace65436195d122b8ce0cfc106728c2922dd350
	match:  True

# Note

You shouldn't change the name of the iso file (for example, `ubuntu-mate-19.04-desktop-amd64.iso`) because this tool uses regular expressions to match them and then look up its hash on the corresponding distro's URL.