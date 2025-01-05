![pypi](https://img.shields.io/pypi/v/distroverify.svg)
![python](https://img.shields.io/pypi/pyversions/distroverify.svg)
![license](https://img.shields.io/github/license/prahladyeri/distroverify.svg)
![docs](https://readthedocs.org/projects/distroverify/badge/?version=latest)
[![patreon](https://img.shields.io/badge/Patreon-brown.svg?logo=patreon)](https://www.patreon.com/prahladyeri)
[![paypal](https://img.shields.io/badge/PayPal-blue.svg?logo=paypal)](https://paypal.me/prahladyeri)
[![follow](https://img.shields.io/twitter/follow/prahladyeri.svg?style=social)](https://x.com/prahladyeri)

# distroverify

![project logo](https://raw.githubusercontent.com/prahladyeri/distroverify/master/logo.png)

Utility to verify any linux distro file (*.iso) for its integrity.

# Installation

	pip install distroverify

# Usage

Simply run `distroverify` with path to iso file as argument:

![distroverify usage](https://raw.githubusercontent.com/prahladyeri/distroverify/master/distroverify_usage.png)

	
# Notes

- Supported distros:
	* Ubuntu - All family
	* Debian (Live & DVD)
	* Linux Mint
	* OpenSUSE LEAP
	* Fedora (Live & netinst)

- You shouldn't change the name of the iso file (for example, `ubuntu-mate-19.04-desktop-amd64.iso`) because this tool uses regular expressions to match them and then look up its hash on the corresponding distro's URL.
