---
title: Building the Interlisp system
weight: 60
url: /doc/build.html
aliases:
- /_pages/doc/build.html
type: docs
---

Medley Interlisp is open-source and may be obtained from GitHub. It is portable to many different Linux and Apple MacOS systems, as well as Windows using WSL2.

The core is written in portable C. The system currently depends on an X11 system for its display.

### Obtaining The System

The system comes in two parts. The first is a C-based virtual machine [Maiko](https://github.com/interlisp/maiko).

The remainder of the system is OS / architecture-independent and can be found in the [Medley repository](https://github.com/interlisp/medley).

You can now download Medley Interlisp from a release without building anything; see the Medley [README](https://github.com/interlisp/medley/#readme)

See The Maiko [README](https://github.com/Interlisp/maiko/#readme) for build instructions for Maiko, for systems for which there is no pre-built release.

(See [Medley repo README](https://github.com/Interlisp/medley/#readme) for instructions on getting Medley.
Make sure you have an X-server running to manage the Medley Interlisp display, and the DISPLAY environment variable set to point to your X-server.

Running Medley can be done by typing:

```bash
$ cd medley
$ ./run-medley
```

Or, if you wish to start Medley up with a particular image file (SYSOUT):

```bash
$ cd medley
$ ./run-medley <SYSOUT-file-name>
```

The first time the system is run it loads the system image that comes
with the system.  When you exit the system (or "do a `SaveVM`" menu option)
the state of your machine is saved
in a file named `~/lisp.virtualmem`.  Subsequent system startups 
load the `~/lisp.virtualmem` image by default.

### Exiting The System

The system may be exited from an Interlisp prompt by typing:

```lisp
(LOGOUT)
```

Or from a Common Lisp prompt with:

```lisp
(IL:LOGOUT)
```

When you logout of the system, Medley automatically creates a binary
dump of your system located in your home directory named
``lisp.virtualmem''. The next time you run the system, if you don't
specify a specific image to run, Medley restores that image so that
you can continue right where you left off.
