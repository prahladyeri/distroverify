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
		* Ubuntu - All family (except ``ubuntu-server`` because they no longer provide checksums for older versions)
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

To use ``distroverify``, simply run the command with the iso filename as argument:

.. code-block:: bash

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

Notes
===========================

You shouldn't change the name of the iso file because this tool uses regular expressions to match them and then look up its hash on the corresponding distro's URL.

Indices and tables
===========================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
