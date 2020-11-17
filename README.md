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

Then, click File-> Open -> "<vulnerable application>"



To Learn More
=============

* https://inst.eecs.berkeley.edu/~cs161/fa08/papers/stack_smashing.pdf 
- Why are we doing all of this? A very straightforward breakdown of memory, registers, assembly, C, and it's **FREE**!!!!!!

* https://en.wikipedia.org/wiki/Buffer_overflow 
- Actually quite informative

* https://www.amazon.com/Hacking-Art-Exploitation-Jon-Erickson/dp/1593271441 
- Again, to understand memory, registers, assembly, C, and how it all works
