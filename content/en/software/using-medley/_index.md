---
title: Using Medley
weight: 60
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

The following links lead to PDF files containing Interlisp documentation.
We are in the process of organizing this documentation.

### Advice for newcomers

A coding project is a great learning experience. But porting existing Common Lisp software to Medley may be challenging as a first project.

Modern Common Lisps are similar and implement most of ANSI. Adapting software to these environments usually involves minor modifications you can carry out with familiar tools. But the Medley environment is completely different and its Common Lisp farther from ANSI.

Porting to Medley is a substantial task for a newcomer who has to deal at the same time with an incomplete Common Lisp implementation, unfamiliar tools, and an unknown workflow.

It's like hustling the move to a new country you barely speak the language and know the culture of. Within hours of landing at the airport you attempt to open a bank account, apply for a loan, file for health care, register with the tax system, negotiate renting an apartment, and do the paperwork for requesting the services of utility companies. Doing all this immediately after your arrival is overwhelming at best.

For a more enjoyable stay take the time to settle, absorb the local language and culture, and live like a native.

Rather than porting Common Lisp programs, it's better to start with small Interlisp projects that rely only on Medley's features and resources with no external dependencies or interactions. Write Interlisp code from scratch instead of bringing in existing software.

We recommend to take Medley a little bit at a time. [Read the introductory material](#introductory-material), and write at least one or two small Interlisp programs of no more than a thousand lines of code.

### Getting started

To learn Medley we recommend that you go over the following reading lists and pursue the resources in the indicated order.

The introductory list gets you started using Medley. The advanced list builds from there and covers programming the system and mastering its tools.

Most of these resources were created decades ago when Medley was a research system and a commercial product, so they may be incomplete or out of date. We will eventually update them.

Note: locations of documents are likely to change. Best to bookmark this page, which we'll update as the documentation settles down.

#### Introductory material

1. [Interlisp Basics for Common Lisp](/software/using-medley/cl-using). 
If you are familiar with Common Lisp, this guide points out some differences.
1. [Medley for the Novice](/documentation/Medley-Primer.pdf) (also known as Medley Primer).  An introductory guide to the basics of Medley such as executing commands, using menus and files, manipulating windows, editing and saving Lisp code, using the development tools, and more. Read it in full. The code in chapter 20 "Free Menus" doesn't work and some illustrations are missing.
1. [SEdit — The Lisp Editor](https://drive.google.com/file/d/12LW5zCZauJvC63NRMJhjNv5qJkuuCflb/view?usp=sharing). The manual of SEdit, the default Lisp code editor.

1. [LispCourse notes](https://interlisp.org/documentation/lispcourse.pdf). The notes of a beginner course on the Interlisp environment that goes from the basics of interacting with the system to programming in Lisp. Highly recommended. Skip the sections on printing and the network as modern Medley doesn't fully implement the described functionality. The formatting of the text is partially broken and some sections are missing. 

#### Advanced material

1. [INTERLISP: The Language and Its Usage](/documentation/1986-interlisp-language-book-1.pdf). An extensive book on the Interlisp language, a prerequisite for accessing the full functionality of Interlisp. Some of the material prepared in 1986 about earlier Interlisp versions and differs from Medley. You may skip the chapters on the Interlisp TTY editor, DWIM, and Conversational Lisp (CLISP).
1. [Medley Language Reference](/documentation/IRM.pdf) (also known as Interlisp Reference Manual). The reference documentation on the Interlisp language, the application platform, and the development environment. The chapters on the Interlisp language are highly recommended. You may skip the chapters on DWIM and CLISP. Some chapters are duplicated, others are missing.
1. [Medley Interlisp: Interactive Programming Tools](/documentation/2021-interlisp-book-3.pdf). Using the development tools and applications. Skip the chapter on DEdit as the tool was replaced by SEdit, the current default Lisp code editor.
1. [Medley Interlisp: The Interactive Programming Environment](https://interlisp.org/documentation/20211225-interlisp-book-2.pdf). Accessing from Lisp the facilities and tools of the Medley environment such as windows, menus, fonts, and image streams.

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
   Now also available in [zipped DJVU format](/documentation/1986-Interlisp-Language-Usage.ocr.djvu.zip)
  - <a href="20211225-interlisp-book-2.pdf">Medley Interlisp: Interactive Programming Environment (derived from Interlisp-D)</a>
  - <a href="2021-interlisp-book-3.pdf">Medley Interlisp: Interactive Programming Tools (derived from Interlisp-D)</a>
- <a href="IRM.pdf">(1993) Interlisp Reference Manual</a>
