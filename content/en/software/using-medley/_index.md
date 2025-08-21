---
title: Documentation
weight: 20
type: docs
aliases:
 - /docs/
 - /medley/using/docs/medley/the-medley-interlisp-dsk-file-system/
 - /doc/info/Using
 - /using-medley/
 - /medley/using/
 - /medley/using/docs/medley/orientation/
 - /medley/using/docs/medley/
 - /docs/medley/orientation/
 - /medley/using/docs/medley/tips/
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
3. [Using Medley Online](online-using) -- additional introduction primarily for online users
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

The site [files.interlisp.org/medley/](https://files.interlisp.org/medley/) is a mirror of the Medley source tree with most text files, such as Lisp sources and TEdit documents, also available in PDF format with HTML forthcoming. It holds many useful documentation files we recommend checking out.

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
  - [Medley Interlisp: Interactive Programming Environment (derived from Interlisp-D)](/documentation/20211225-interlisp-book-2.pdf)
  - [Medley Interlisp: Interactive Programming Tools (derived from Interlisp-D)](/documentation/2021-interlisp-book-3.pdf)
- [Interlisp Reference Manual (1993)](/documentation/IRM.pdf)
- Medley LOOPS Books (LOOPS, the Lisp Object-Oriented Programming System, was an object extension of Interlisp):
  - [Volume I: Medley LOOPS: The Basic System](/documentation/2024-loops-book-1.pdf)
  - Volume II: Medley LOOPS: Tools and Utilities (forthcoming)
  - Volume III: Medley LOOPS: Rule-based Systems and the Truckin Game (coming in the fall of 2025)

