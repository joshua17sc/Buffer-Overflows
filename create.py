#!/usr/bin/env python3

from __future__ import print_function
#badchars 00 07 2e a0
bad = "00 07 2e a0".split()
for x in range(1, 256):
	if "{:02x}".format(x) not in bad:
		print("\\x" + "{:02x}".format(x), end='')
print()
for byte in bad:
	print("\\x{}".format(byte), end='')
print()

