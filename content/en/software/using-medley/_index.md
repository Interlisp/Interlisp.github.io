---
title: Using Medley
weight: 10
type: docs
aliases:
 - /medley/using/docs/medley/orientation/
 - /docs/
 - /medley/using/docs/medley/the-medley-interlisp-dsk-file-system/
 - /doc/info/Using.html
 - /doc/info/Using
 - /hugo/documentation
 - /using-medley/
 - /medley/using/
 - /medley/using/docs/medley/orientation/
 - /medley/using/docs/medley/
 - /docs/medley/orientation/
 - /medley/using/docs/medley/tips/
 - /docs/medley/orientation/
 - /software/using-medley/medley/
 - /software/using-medley/IRM.pdf
---

Whether you're just getting started or refreshing your knowledge of Interlisp, we have a variety of documentation to help you along.

### Getting started

To learn Medley we recommend that you go over the following reading lists and pursue the resources in the indicated order.

The introductory list gets you started using Medley. The advanced list builds from there and covers programming the system and mastering its tools.

Many of these resources were created decades ago when Medley was a research system and a commercial product, so they may be incomplete or out of date. We will eventually update them.

Note: locations of documents are likely to change. Best to bookmark this page, which we'll update as the documentation settles down.

#### Introductory material

1. [Interlisp Basics](il-using)
2. [Medley Basics for Common Lisp users](cl-using). 
If you are familiar with Common Lisp, this guide points out some differences.
1. [Medley for the Novice](/documentation/Medley-Primer.pdf) (also known as Medley Primer).  An introductory guide to the basics of Medley such as executing commands, using menus and files, manipulating windows, editing and saving Lisp code, using the development tools, and more. Read it in full. The code in chapter 20 "Free Menus" doesn't work and some illustrations are missing.
1. [SEdit — The Lisp Editor](https://drive.google.com/file/d/12LW5zCZauJvC63NRMJhjNv5qJkuuCflb/view?usp=sharing). The manual of SEdit, the default Lisp code editor.

1. [LispCourse notes](https://interlisp.org/documentation/lispcourse.pdf). The notes of a beginner course on the Interlisp environment that goes from the basics of interacting with the system to programming in Lisp. Highly recommended. Skip the sections on printing and the network as modern Medley doesn't fully implement the described functionality. The formatting of the text is partially broken and some sections are missing. 

#### Advanced material

1. [INTERLISP: The Language and Its Usage](/documentation/1986-interlisp-language-book-1.pdf). An extensive book on the Interlisp language, a prerequisite for accessing the full functionality of Interlisp. Some of the material prepared in 1986 about earlier Interlisp versions and differs from Medley. You may skip the chapters on the Interlisp TTY editor, DWIM, and Conversational Lisp (CLISP).
1. [Medley Language Reference](/documentation/IRM.pdf) (also known as Interlisp Reference Manual). The reference documentation on the Interlisp language, the application platform, and the development environment. The chapters on the Interlisp language are highly recommended. You may skip the chapters on DWIM and CLISP. Some chapters are duplicated, others are missing.
1. [Medley Interlisp: Interactive Programming Tools](/documentation/2021-interlisp-book-3.pdf). Using the development tools and applications. Skip the chapter on DEdit as the tool was replaced by SEdit, the current default Lisp code editor.
1. [Medley Interlisp: The Interactive Programming Environment](/documentation/20211225-interlisp-book-2.pdf). Accessing from Lisp the facilities and tools of the Medley environment such as windows, menus, fonts, and image streams.

### Unsorted documentation content

Most Interlisp/Medley documentation was written using the Medley Text Editor, one of the first WYSIWYG graphical user interface text editors, called TEdit. Written in and for Interlisp users, it features muliple fonts, embedded graphics including line drawings and raster images.

TEdit files are scattered through the various Interlisp repositories. For the convenience of those who would rather read the files using more modern tools, see the files from different Medley Interlisp repositories, [converted to PDF](https://drive.google.com/drive/folders/10ZBQty5gEwdBnZHtEbXfe5f1dHGziGZG?usp=sharing).
 
For the searcher's conveneience, these have also been combined into searchable PDFs named All-*-PDFs.pdf.

### Medley References

- [Medley Primer](/documentation/Medley-Primer.pdf)
- [Medley for the Sun Workstation User's Guide](/documentation/SunUserGuide.pdf)

<!-- - <a href="1992-02-An_Introduction_to_Medley_Release_2.0.pdf">Introduction to Medley, Release 2.0</a> -->

#### Exported Medley Documentation
These documents were converted from Medley's internal format into PDFs. Watch out for weird formatting, but these are firsthand sources on Medley features and applications.

- [Medley Internal Documentation PDF](/documentation/All-Medley-PDFs.pdf)
- [Notecards Documentation PDF](/documentation/All-Notecards-PDFs.pdf)
- [LOOPS Documentation PDF](/documentation/All-Loops-PDFs.pdf)


### Interlisp Books

- [Interlisp - The Language and Its Usage](/documentation/1986-interlisp-language-book-1.pdf)
  Also available in [zipped DJVU format](/documentation/1986-Interlisp-Language-Usage.ocr.djvu.zip)
  - <a href="20211225-interlisp-book-2.pdf">Medley Interlisp: Interactive Programming Environment (derived from Interlisp-D)</a>
  - <a href="2021-interlisp-book-3.pdf">Medley Interlisp: Interactive Programming Tools (derived from Interlisp-D)</a>
- <a href="IRM.pdf">(1993) Interlisp Reference Manual</a>

# Another brief guideline for online users

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

