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

Our goal is to maintain compatibility with old code and not introduce breaking changes at the source level or introduce subtle semantic changes.

## Common Lisp and Interlisp file manager

While Medley 3.5 has a Common Lisp implementation, it is compatible with the Common Lisp of its time -- the first edition of Common Lisp the Language (aka CLtL1).  There are files that purport to implement CLtL2, but they have not yet been merged. 

In addition, the integration of Common Lisp and Interlisp is extensive, there are still some rough edges -- along the way of integrating the two, the result is not quite seamless.

While Interlisp and Medley implement international character processing and hardcopy through use of 16-bit characters, the character coding system initially used for the external format was XCCS (the Xerox Character Code Standard). The system can now read and write files in a number of formats, including UTF-8, and we are aspiring to use the UTF-8 encoding for Lisp source files.

### CPU and operating system
* Originally: 32 bit systems, big endian
* Medley 3.5: 32 bit little endian
* Now: 64 bit data paths, little endian

Changing from a 32-bit to 64-bit CPU was addressed carefully by upgrading the code in the emulator from "K&R" C to modern C standard.

### File systems
* Originally: case insensitive, versioned file system
* Now: varied case sensitivity

More subtlely, the collaboration workflow has changed. The assumption for many at PARC was to have large file servers that everyone in a team would share, develop new versions, and then merge in by copying files to the file server.

In a Git-based workflow, the version numbers are mainly meaningless.

### Mouse
* Originally: three button mouse
* Now: two, one, or touchpad cursor movement; scroll wheel

Scroll wheel implementation, middle button menu commands are awkward.

### Keyboard
* Originally: limited number of keyboards; every app did decoding
* Now: impossibly many keyboards: users want uniform (and familiar)

We have yet to gain mastery over the complex way that Medley handles the keyboard.

### Character encoding for external file representation
* Originally: XCCS (Xerox Character Code Standard)
* Transitioning to: UTF-8 and Unicode

### Display
* Originally: 768x808 one bit per pixel
* Now: larger displays

Medley supported color displays on certain platforms, but the underlying code has been removed.

### Available compilers
* Originally:  "K&R" book of standard C
* Now: Clang, gcc, Make, CMake and Posix standards

### Version Management
* Originally: versioned file system
* Now: path names via "pseudo hosts"; GITFNS, structure comparison

### Modernization
We are introducing new features to make the Medley environment more accessible and familiar to modern users. We have implemented scrolling with a mouse wheel, host system clipboard access, and click and drag mouse gestures to move or resize windows.
