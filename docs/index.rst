.. toctree::
   :maxdepth: 2
   :caption: Contents:
   

Introduction
============================

``distroverify`` is a utility to verify any linux distro file (\*.iso) for its integrity and primarily intended towards distro hoppers and linux newbies. When you download a distro iso file from the internet (such as 	``ubuntu-mate-19.04-desktop-amd64.iso``), you may never know if it may have been tampered with en-route or even on the server itself.

To be sure, you have to download a checksum file (usually ``sha1`` or ``sha256``) to ensure that the checksum matches with the distro file's checksum calculated at your end. This tool does exactly that, it takes care of the hassle for scavenging for the checksum file's download link and run a checksum utility like sha1sum or sha256sum. It automates this whole process for you in a single program!

Supported Distros
====================

The following distros are supported so far and the list keeps growing. It all depends on whether or not the distros maintain a standard convention in naming their urls for hashes.

	* Supported distros:
		* Ubuntu - All family
		* Debian (Live & DVD)
		* Linux Mint
		* OpenSUSE LEAP
		* Fedora (Live & netinst)

Installation
===========================

``distroverify`` can be installed with python's standard package manager, ``pip``::

	pip install distroverify

Usage
===========================

Simply run ``distroverify`` with path to iso file as argument:

.. code-block:: bash

	prahlad@ubuntu:~$ distroverify ubuntu-14.04.6-server-i386.iso 
	distro detected:  ubuntu
	version: 14.04.6, type: server, arch: i386
	verification url(s): http://cdimage.ubuntu.com/ubuntu/releases/14.04.6/release/SHA256SUMS
	calculating hash...

	c3b0e016e77e6bcfc608ab3e3d2aa33367fc83e3bf645014ecf36689fe330b80
	fetching official hash...
	trying releases url http://releases.ubuntu.com/14.04.6/SHA256SUMS...

	calculated hash: c3b0e016e77e6bcfc608ab3e3d2aa33367fc83e3bf645014ecf36689fe330b80
	official hash: c3b0e016e77e6bcfc608ab3e3d2aa33367fc83e3bf645014ecf36689fe330b80
	match:  True
	looks like ubuntu-14.04.6-server-i386.iso is genuine

Notes
===========================

You shouldn't change the name of the iso file because this tool uses regular expressions to match them and then look up its hash on the corresponding distro's URL.

API Documentation
==================

.. automodule:: distroverify
.. automodule:: distroverify.distroverify
	:members:


Indices and tables
===========================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
