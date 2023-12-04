---
title: Building the Interlisp system
weight: 60
aliases:
 - /_pages/doc/build.html
 - /doc/build.html
 - /developing
type: docs
---

Medley Interlisp is open-source and may be obtained from GitHub. It is portable to many different systems: Linux, Windows (with or without WSL),  Apple MacOS and many more.

### Obtaining The System

The system comes in two parts. The first is a C-based virtual machine [Maiko](https://github.com/interlisp/maiko).

The remainder of the Medley is independent of OS and computer architecture. Instrucdtions can be found in the [Medley repository](https://github.com/interlisp/medley).

The Maiko [README](https://github.com/Interlisp/maiko/#readme) has build instructions for Maiko. You may need to do this for systems for which there is no pre-built release.

In the cases where you've built your own Maiko (producing binaries lde, ldex, ldsdl), the instructions are changing.



```bash
$ cd medley
$ ./run-medley
```

Or, if you wish to start Medley up with a particular image file (SYSOUT):

```bash
$ cd medley
$ ./run-medley <SYSOUT-file-name>
```

### Exiting The System

The system may be exited from an Interlisp prompt by typing:

```lisp
(LOGOUT)
```

Or from a Common Lisp prompt with:

```lisp
(IL:LOGOUT)
```
The first time the system is run it loads the system image that comes
with the system.  When you exit the system (or "do a `SaveVM`" menu option)
the state of your machine is saved
in a file named `~/lisp.virtualmem`.  Subsequent system startups 
load the `~/lisp.virtualmem` image by default.

`run-medley` is a script, documentation at the beginning.
