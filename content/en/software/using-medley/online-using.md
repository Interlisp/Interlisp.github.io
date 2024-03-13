---
title: Using Medley Online
weight: 40
type: docs
---


## Starting up

The Medley Desktop at startup contains 4 windows of interest:

* Prompt Window: The black window at the top of the screen. It is used to display system or application prompts
* Exec (INTERLISP or XCL) window: The main window where you run functions and develop programs.
* Medley logo window: A window containing the Interlisp Medley logo as a bit map.
* Status Bar window

Medley Online users get some additional buttons on the right-hand side of the screen.

### Managing memory images and sessions

Medley has a byte-coded virtual machine architecture with a VM designed for Lisp.  This is a common practice, used by Javascript, Flash and Java and other systems to aid in portability: to support a new architecture, you just port the "virtual machine emulator" rather than the whole system.

With Medley, there are two types of files relevant to managing memory images and updating them across sessions: `lisp.virtualmem` and `.sysout`.

The `lisp.virtualmem` file is a capture of the "current" state of the system (i.e., it is a copy of the virtual memory at a point in time). `lisp.virtualmem` is written whenever you execute `(IL:LOGOUT)` and also whenever executing `(IL:SAVEVM)`. You can restart Medley using a `lisp.virtualmem` and it will pick up essentially where it left off before the `LOGOUT` or `SAVEVM` (with the exception that the user can set `BEFORE`/`AFTER` and `LOGOUT`/`SAVEVM` code that runs before you get control of the restarted `lisp.virtualmem`).

A `.sysout` is a virtual memory image produced by `MAKESYS` (for writing an image for distribution) and `SYSOUT` (for saving a named checkpoint, e.g. to revert to a previous state if needed), which differ only in the way they process the startup options. You can (and most frequently do) start Medley from a sysout file. When Medley first starts from a sysout, it automatically runs initialization scripts — a site initialization script followed by a per-user initialization script (if available).

With Interlisp Online, every time you `Run Medley` you start up from one of the supplied sysout files (i.e., from a "clean image"), unless the `Resume previous session` box is checked. In that case, you will be starting up from the `lisp.virtualmem` stored for you online (if any) and that was created by the `(IL:LOGOUT)` at the end of your previous session.

As a registered Interlisp Online user you get the choice of resuming your previous image or starting from a clean image — with the default being starting from a clean image.

For guest logins, there is no `Resume previous session` because `lisp.virtualmem` is never preserved for guests. 

For registered users, any files that you create (e.g., with `IL:MAKEFILE`) will also be preserved across sessions online.These files will not be automatically loaded into the system when you re-start with a clean image, unless you `LOAD` them explicitly (or add a `LOAD` to your personal `INIT` file stored online at `{DSK}/home/medley/il/INIT`).



