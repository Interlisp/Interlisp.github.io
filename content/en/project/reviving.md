---
Title: Reviving Medley
weight: 80
type: docs
---
# Choices and Challenges 

The main work of the Medley Interlisp Project is managed through GitHub.
This outlines some of the areas of work.

## A Work in Progress

We started with the most recent working files from Venue sources. This was not a finished and tested release, but rather a work in progress, nearly complete, labeled Medley 3.5. (The last release by Venue was called Medley 2.01.)

Among other improvements, Medley 3.5 increased the address space by a factor of 16.  But the changes to the address space affects some highly optimized code which took advantage of short-cuts.

## Common Lisp and Interlisp file manager

While Medley 3.5 has a Common Lisp implementation, it is compatible with the Common Lisp of its time -- the first edition of Common Lisp the Language (aka CLtL1).  There are files that purport to implement CLtL2, but they have not yet been merged. 

In addition, the integration of Common Lisp and Interlisp is extensive, there are still some rough edges -- along the way of integrating the two, the result is not quite seamless.

While Interlisp and Medley implement international character processing and hardcopy through use of 16-bit characters, the character coding system used is XCCS (the Xerox Character Code Standard). 

### CPU and operating system
* originally: 32 bit systems, big endian
* medley 3.5: 32 bit little endian
* now: 64 bit data paths, little endian

Changing from a 32-bit to 64-bit CPU was addressed carefully by upgrading the code in the emulator from "K&R" C to modern C standard.

### File systems
* originally: case insensitive, versioned file system. 
* now: varied case sensitivity

More subtlely, the collaboration workflow has changed. The assumption for many at PARC was to have large file servers that everyone in a team would share, develop new versions, and then merge in by copying files to the file server.

In a Git-based workflow, the version numbers are mainly meaningless.

### Mouse
* originally: three button mouse
* now: two, one, or touchpad cursor movement; scroll wheel

Scroll wheel implementation, middle button menu commands are awkward.

### Keyboard
* Originally: limited number of keyboards; every app did decoding
* now: impossibly many keyboards: users want uniform (and familiar)

We have yet to gain mastery over the complex way that Medley handles the keyboard.

### Character encoding
* originally: XCCS (Xerox Character Code Standard)
* Now: Unicode

### Display
* originally: 768x808 one bit per pixel
* now: larger, color displays

Color support seems like it might have been a Medley feature that was taken out, for reasons that are unclear.  Running on a large 4K display at full-screen isn't possible. We have yet to integrate modern fonts.

### Available compilers
* Originally:  "K&R" book of standard C
* now: gcc, cmake and Posix standards

### Version Management
* Originally: versioned file system
* now: path names via "pseudo hosts"; GITFNS, structure comparison


