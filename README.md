#Buffer-Overflows


References
==========
* https://bytesoverbombs.io/exploiting-a-64-bit-buffer-overflow-469e8b500f10
* https://www.abatchy.com/2017/05/jumping-to-shellcode.html
* http://www.voidcn.com/article/p-ulyzzbfx-z.html
* https://www.securitysift.com/windows-exploit-development-part-4-locating-shellcode-jumps/
* https://medium.com/@johntroony/a-practical-overview-of-stack-based-buffer-overflow-7572eaaa4982

Background
==========
A lot of people are prepping for OSCP but cannot find good scripts in Python3.

I built these scripts to work through Ti3rius's TryHackMe room 

https://tryhackme.com/room/bufferoverflowprep

Tib3rius goes through all of this stuff in the room and on their github repo

https://github.com/Tib3rius/Pentest-Cheatsheets/blob/master/exploits/buffer-overflows.rst

Like all things in cyber, things deprecate. 

As of Oct 2020, these Python3 scripts should work.

P.s. I'm not a Python developer. I'm a Jack of all trades. 
So my code is simple and straightforward. 

Let's walkthrough how it all works.


Setup Windows
=============
Your Windows VM will have Immunity Debugger and a vulnerable application.

Right click on Immunity Debugger and "open as Administrator"

Then, click File-> Open -> "vulnerable application"

Use the green start arrow at the top to start your process (check the bottom right corner of Immunity to see if it's still paused) - or use F9 to start

run CMD as Administrator
	:code: `netstat -anbo | find "Listening"`

Look for your process and its listening port.
	

Enumerate
=========

You can scan your windows machine with nmap.

Or, since you just ran netstat, netcat to your Windows machine on that port.

Look at what input it takes.

Probably need to run :code: `HELP`

Most of these commands are case-sensitive.

Play around and see what the service does.


Mona
====

Mona makes this process easier, as will Metasploit later.

| The latest version can be downloaded here: https://github.com/corelan/mona
| The manual can be found here: https://www.corelan.be/index.php/2011/07/14/mona-py-the-manual/


If your Windows machine doesn't have it already, copy the mona.py file into the PyCommands directory of Immunity Debugger (usually located at C:\\Program Files\\Immunity Inc\\Immunity Debugger\\PyCommands).

In Immunity Debugger, type the following to set a working directory for mona.

.. code-block:: none

    !mona config -set workingfolder c:\mona\%p

Spike
=====

We're going to use Spike to test which commands are vulnerable to buffer overflows.

* https://resources.infosecinstitute.com/topic/intro-to-fuzzing/

Spike is accessed with :code:`$ generic_send_tcp`

Usage: ./generic_send_tcp host port spike_script SKIPVAR SKIPSTR
./generic_send_tcp 192.168.1.100 701 something.spk 0 0

check out the spike.spk file to see the syntax
.. code-block:: none

	s_readline(); #to read the banner
	s_string("OVERFLOW1 "); #our command to test, don't forget the space afterwards
	s_string_variable("0"); #any additional strings to add each time

This is going to make a ton of connections, passing the string with fuzzed information. 

Immunity should crash, if the command is vulnerable.

Look at your register values. See if it was able to overwrite the EIP.

Fuzz
====

Congrats, you crashed it! (feels weird to say after years as a pilot).

Restart Immunity by using the Rewind button next to the red play arrow at the top. (Or Ctrl+F2)

Then hit play. (or F9)

Now, let's control that crash (we call that a landing).

We're going to use *fuzz.py* to send our vulnerable command and additional data, increasing by 100 bytes (A's) with each attempt.

Did you overwrite EIP? How many bytes were required?

This should give you a starting point for your next step.

Finding Offset
==============

Reset Immunity (Ctrl+F2 and then F9)

We really need to pinpoint EIP in order to control it, and control the service.

Metasploit Framework has a nifty couple tools for us :code:`msf-pattern_create` .

It will give us a non-repeating pattern that we can send with our command. If we make it the right size, then we can copy whatever ends up in EIP after the crash and use :code:`msf-pattern_offset` to find the exact offset.

With that offset, we will own the EIP.

.. code-block:: none
	
	msf-pattern_create -l 2300 #bytes from fuzzing plus 300

Double click the output to highlight, then Ctrl+Shift+C to copy it all.

Paste it in offset.py .

Run offset.py, copy the value from the EIP.

.. code-block:: none
	
	msf-pattern_offset -l 2300 #same as above -q 


To Learn More
=============

* https://inst.eecs.berkeley.edu/~cs161/fa08/papers/stack_smashing.pdf 
	- Why are we doing all of this? A very straightforward breakdown of memory, registers, assembly, C, and it's **FREE**!!!!!!

* https://en.wikipedia.org/wiki/Buffer_overflow 
	- Actually quite informative

* https://www.amazon.com/Hacking-Art-Exploitation-Jon-Erickson/dp/1593271441 
	- Again, to understand memory, registers, assembly, C, and how it all works
