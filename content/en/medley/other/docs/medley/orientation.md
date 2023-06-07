---
title: Orientation to Medley
weight: 5
type: docs
---

Once the system has been started, you will see some windows with title bars. Navigation within the system is a little unusual.
To control a window, right-click on the window's title bar. To bring up a system menu, right-click anywhere outside a window.

Windows titled "Exec" work as read-eval-print loops with the addition of extensive "commands". There are four different
contexts, determined by the default "package" and "readtable". The "package" of a window determines which (Common Lisp)
package is the default while the "readtable" controls whether typing is treated as case sensitive or not.

The title bar will also tell you whether you are running LISP (for Common Lisp), XCL (for Xerox Common Lisp), INTERLISP (for current Interlisp), or
OLD-INTERLISP-T (for an older version of Interlisp).

When the system first comes up you will notice a window labeled "Exec (XCL)". This works as a Common Lisp read-eval-print loop.

(Hint: When the system has completed its initialization process, a fresh prompt will appear.)

## Different Lisp Environments

The system comes with four versions of "Exec":

* `Interlisp`:  Package: *Interlisp*, Readtable: a hybrid, case sensitive environment. Most Interlisp functions are all caps, so use of the SHIFT LOCK is recommended.
* `Old Interlisp`: The same *Interlisp* package, but an older readtable (where ":" isn't a package delimiter)
* `Common Lisp`: Package: *USER* (need to check)
* `XCL`: (eXtended Common Lisp) Common Lisp with a number of extensions.

Even though each of the possible Exec's gives a default environment, all of the various Lisp functions and variables are interchangeably available from any of the Exec windows via package specifications.  For example, an Interlisp function names `ABC` may be run from Common Lisp via `(IL:ABC ...)`. Likewise, a Common Lisp function `DEF` may be executed from Interlisp via `(CL:DEF ...)`.

## Images And Files

The Medley system includes a virtual machine (VM) that runs the Lisp programs.
Medley can run Lisp code interpreted or compiled into the byte-code for the
Medley VM.  This is a bit similar to the Java Virtual Machine or the .NET CLR
or Smalltalk.

In traditional systems, a developer edits source code files and then
compiles those files into something the machine can execute --- be it
a machine executable file or byte-code for a VM.  Medley does not work
that way.  Medley is an image-based system similar to Smalltalk or Squeak.

When Medley is started up, you are in the development and runtime
environment.  All of your development is done here and all of your
programs are run here.  You are essentially editing runnable programs
in memory.  When you exit the system, Medley creates a backup of this
memory onto what is called a SYSOUT (or `lisp.virtualmem`).  When the system is started
up again, this image is read into memory and the system picks up right
where it left off.  This is what is called an image-based development
environment.

In Medley, programs are developed, edited, debugged, and run all from
within Medley.  The state of this development is saved in your image file.
There is also a way to save your system to more traditional
disk files.  This is called the ``File Package''.

Medley utilizes the following file types:

* `lisp.virtualmem`: This is located in your home directory and is an image of the last time Medley was run.  If you start Medley without specifying an image to run, this image is used.
* `XXXX.SYSOUT`: This is an image that was explicitly saved by the developer.  This may be loaded by specifying its name when starting Medley.
* `XXXX` (no file name extension): Source files created with the ``File Package''.
* `XXXX.LCOM`: Compiled versions of the XXXX files
* `XXXX.DFASL`: Another compiled form of XXXX files
* `XXXX.TEDIT`: Text (like a word processor) in a Medley-specific format

## Project Directory

Medley has something called its "connected directory".  This is just
another way to say "working directory".  All file reads and writes
occur (if no path is specified) in the connected directory.  When Medley
first starts up, its connected directory is your home directory.  This
can be changed by executing one of the following commands:

```
cd MyProject
```

or

```
(CNDIR "MyProject")
```

You will see the connected directory displayed at the top of the Medley
window.  Once the connected directory has been changed, all future
image saves or file loads or saves will occur in this directory.  Additionally,
this directory will be saved in the image so when you re-load the image, you 
will already be in the desired directory.

One thing to note, however, is that the default image
`lisp.virtualmem` will still be saved in your home directory.  This
assures that if you start Medley up without specifying an image, you
will return to the last environment you were in.

## Saving And Running Images

You can also manually save an image to a specific file at any point by
typing the following from an Interlisp prompt:

```
(SYSOUT "my-file")
```

This will save your running image to a file named `my-file.SYSOUT` that can be loaded again by passing that file name to the
`run-medley` command.

### Creating And Editing Functions

Objects (function, variables, etc.) can be credited and edited
as follows:

```
ED(myfunc)
```

First, if it is a new object, the system will ask what type of object
it is.  After that, the user will be presented with a GUI structure editor
where the object may be defined or edited.

When the window is closed, via right-clicking on the title bar,
the object will be saved.

### Saving & Loading Source Code To/From Disk Files

When you edit or define a function, a variable, etc., Medley keeps
track of the fact that they have been created or edited.  These
functions and variables are grouped and ultimately get associated with
a file on your disk.  In places, Interlisp refers to these disk files
as "symbolic files".

* `FILELST` - list of user files the system is aware of
* `SYSFILES` - list of system files loaded
* `(FILES?)` - prompts user for which file to associate newly defined functions, variables, etc.
* `(MAKEFILE "myfile")` - writes out all of the functions, variables, etc. that have been associated with file "myfile"
* `(LOAD "myfile")` - loads a previously saved file
* `(LOAD "myfile.LCOM")`  - load a previously compiled file
* `(CLEANUP)` - interactively save and compile all changed files
