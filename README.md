![pypi](https://img.shields.io/pypi/v/distroverify.svg)
![python](https://img.shields.io/pypi/pyversions/distroverify.svg)
![implementation](https://img.shields.io/pypi/implementation/distroverify.svg)
<!-- https://img.shields.io/travis/prahladyeri/distroverify/master.svg -->
![docs](https://readthedocs.org/projects/distroverify/badge/?version=latest)
![license](https://img.shields.io/github/license/prahladyeri/distroverify.svg)
![last-commit](https://img.shields.io/github/last-commit/prahladyeri/distroverify.svg)
<!--![commit-activity](https://img.shields.io/github/commit-activity/w/prahladyeri/distroverify.svg)-->
[![follow](https://img.shields.io/twitter/follow/prahladyeri.svg?style=social)](https://twitter.com/prahladyeri)
# distroverify
Utility to verify any linux distro file (*.iso) for its integrity.

# Installation

	pip install distroverify

# Usage

	> python -m distroverify.main d:\iso\ubuntu-mate-19.04-desktop-amd64.iso
	Distro Verify version 1.0.8
	Utility to verify any linux distro file (*.iso) for its integrity

	match success:  ubuntu-mate
	verifyication url: http://cdimage.ubuntu.com/ubuntu-mate/releases/19.04/release/SHA1SUMS
	calculating file hash...
	done
	response hash: c691d223f9f3b56340a525686c72db37e7433b90
	calculated hash: c691d223f9f3b56340a525686c72db37e7433b90
	match:  True

# Note

You shouldn't change the name of the iso file (for example, `ubuntu-mate-19.04-desktop-amd64.iso`) because this tool uses regular expressions to match them and then look up its hash on the corresponding distro.