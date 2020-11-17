################ 
Buffer-Overflows
################

References
==========
* https://bytesoverbombs.io/exploiting-a-64-bit-buffer-overflow-469e8b500f10
* https://www.abatchy.com/2017/05/jumping-to-shellcode.html
* http://www.voidcn.com/article/p-ulyzzbfx-z.html
* https://www.securitysift.com/windows-exploit-development-part-4-locating-shellcode-jumps/
* https://medium.com/@johntroony/a-practical-overview-of-stack-based-buffer-overflow-7572eaaa4982

Background
==========
I'm new to this.
A lot of people are prepping for OSCP but cannot find good scripts in Python3.

Have at them because here they are.  
I built them to work through Ti3rius's TryHackMe room 
https://tryhackme.com/room/bufferoverflowprep
Tib3rius goes through all of this stuff in the room and on their github repo
https://github.com/Tib3rius/Pentest-Cheatsheets/blob/master/exploits/buffer-overflows.rst

Like all things in cyber, things deprecate. 
As of Oct 2020, these Python3 scripts should work.
P.s. I'm not a Python developer. I'm a Jack of all trades. 
So my code is simple and straightforward. 
Make a pull request if you want to make it look prettier. Please make a branch.

I'll go through and clean this up a bit as I have time.

Setup Windows
=============


To Learn More
=============

https://inst.eecs.berkeley.edu/~cs161/fa08/papers/stack_smashing.pdf - Why are we doing all of this? A very straightforward breakdown of memory, registers, assembly, C, and it's **FREE**!!!!!!

https://en.wikipedia.org/wiki/Buffer_overflow - Actually quite informative

https://www.amazon.com/Hacking-Art-Exploitation-Jon-Erickson/dp/1593271441 - to understand memory, registers, assembly, C, and how it all works
