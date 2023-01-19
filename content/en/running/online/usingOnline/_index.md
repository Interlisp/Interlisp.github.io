---
title: Using Interlisp Online
weight: 8
type: docs
---

### A Brief Introduction

### Running Interlisp Online

* Go to [Interlisp Online](https://online.interlisp.org/main)\
{{< imgproc Login_Screen Resize "400x450">}} Interlisp Online Login {{< /imgproc >}}
  You may either login as a Guest or create an account. If you plan to save and later retrieve files, [register](https://online.interlisp.org/user/register) and create an account. Guest logins are not guaranteed to perserve sessions and stored files.

However, if you just want to get a taste of Interlisp without the extra effort of creating an account, the guest login will suit your needs.

* Select the Exec you want to run. For this exercise, select `Interlisp`
* Leave the `Fill browser window` option set.

Select `Run Medley`. Your browser will open a window that represents the Interlisp Desktop and looks much like this:

{{< imgproc Online_Initial_Medley Resize "800x450">}} Medley Interlisp{{< /imgproc >}}

The Interlisp Desktop at startup contains 4 windows of interest:

* Prompt Window: The black window at the top of the screen. It is used to display system or application prompts
* Exec (INTERLISP) window: The main window where you run functions and develop programs.
* Medley logo window: A window containing the Interlisp Medley logo as a bit map.
* Status Bar window

### Writing Interlisp programs

In the Exec window, type the following:

```lisp
(PLUS 1 1)
```

When you complete typing the ending `)` the Interlisp interpreter will perform the calculation and return the result.

One thing you probably noticed, the command `PLUS` is capitalized. It’s not that the developers of Interlisp were always shouting at each other. Rather, when Interlisp was developed computer programming was in its infancy and standards for naming commands were still evolving.

### Managing memory images and sessions

In Interlisp, there are two types of files relevant to managing memory images and updating them across sessions: `lisp.virtualmem` and `.sysout`.

The `lisp.virtualmem` file is a capture of the "current" state of the system (i.e., it is a copy of the virtual memory at a point in time). `lisp.virtualmem` is written whenever you execute `(IL:LOGOUT)` and also whenever executing `(IL:SAVEVM)`. You can restart Medley using a `lisp.virtualmem` and it will pick up essentially where it left off before the `LOGOUT` or `SAVEVM` (with the exception that the user can set `BEFORE`/`AFTER` and `LOGOUT`/`SAVEVM` code that runs before you get control of the restarted `lisp.virtualmem`).

A `.sysout` is a virtual memory image produced by `MAKESYS` (for writing an image for distribution) and `SYSOUT` (for saving a named checkpoint, e.g. to revert to a previous state if needed), which differ in the way they process the startup options. You can (and most frequently do) start Medley from a sysout file. When Medley starts from a sysout, it automatically runs initialization scripts — a site initialization script followed by a per-user initialization script (if available). A sysout is what you might call "a clean image".

As for Interlisp Online: except as noted below, every time you `Run Medley` you are starting up from a sysout file (i.e., from a clean image). The exception is if you check the `Resume previous session` box. In that case, you will be starting up from the `lisp.virtualmem` stored for you online (if any) and that was created by the `(IL:LOGOUT)` at the end of your previous session.

As a registered Interlisp Online user you get the choice of resuming your previous image or starting from a clean image — with the default being starting from a clean image.

For guest logins, there is no `Resume previous session` because `lisp.virtualmem` is never preserved for guests.

For registered users, any files that you create (e.g., with `IL:MAKEFILE`) will also be preserved across sessions online. But these files will never be automatically loaded into the system when you re-start with a clean image — you need to `LOAD` them explicitly (or add a `LOAD` to your personal `INIT` file stored online at `{DSK}/home/medley/il/INIT`).

### Save your program as a file

### Opening a saved program

### What next?
