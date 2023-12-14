---
Title: Reviving Medley
weight: 80
type: docs
---
# Choices and Challenges 
Instead of starting with an earlier, finished and tested release, we started with a project that was valuable but incomplete: the files for a "Medley 3.5" release, as the latest available to us. Among other things, Medley 3.5 increase in address space -- from 64mb to 256mb.

Differences between Medley 1.0 and Medley Interlisp.

* CPU and operating system:
  * originally: 16 and 32 bit systems, big endian
  * medley 3.5: 32 bit little endian
  * now: 64 bit data paths, little endian

* File systems:
  * originally: case insensitive, versioned file system
  * now: varied case sensitivity, upper and lower case
* Mouse:
  * originally: three button mouse
  * now: two, one, or touchpad cursor movement; scroll wheel
* Keyboard:
  * Originally: limited number of keyboards; every app did decoding
  * now: impossibly many keyboards: users want uniform (and familiar)
* Character encoding:
  * originally: XCCS (Xerox Character Code Standard)
  * Now: Unicode
* Display
  * originally: 768x808 one bit per pixel
  * now: larger, color displays
* Available compilers
  * Originally:  "K&R" book of standard C
  * now: gcc, cmake and Posix standards
* Version Management
  * Originally: versioned file system based on emulating 
  * now: relative path names from "pseudo hosts"


We have also developed tools for managing the GitHub workflow, to integrate the Interlisp style development with git and GitHub, Docker and other modern components.
