---
title: Glossary
aliases:
 - /glossary/
 - /medley/project/vocabulary/
weight: 90
type: docs
---

The names “Medley,” "Interlisp-D," “Interlisp.org,” “Common Lisp,” etc. are often used in confusing ways. We’re talking about a lot of different things that evolved over decades. These are cemented in by usage in different publications over time. We hope this glossary of terms will help.

For general computer terminology and lore see [The Hacker's Dictionary](https://www.dourish.com/goodies/jargon.html) aka Jargon File.

## Vocabulary and relationships

AltoLisp
: An experimental microcoded implementation of Interlisp on an Alto personal computer.

Break package
: The Interlisp subsystem that comprises the debugger (also known as break window) and other debugging facilities. Named after the `BREAK` function and breakpoints.

Briefing Blurb
: One of the several documents that introduced Xerox PARC newcomers to the computing and network environment of the Computer Science Laboratory. Written in an upbeat style, their titles followed a pattern that included the expression "Briefing Blurb" such as *The Alto-Dolphin-Dorado Briefing Blurb: Exploring the Ethernet with Mouse and Keyboard* and *The Briefing Blurb: Exploring the Ethernet with Mouse and Keyboard*.

Carol, Fugue, Harmony, Intermezzo, Koto, Lyric, Medley
: Named releases of Interlisp-D.  All are obsolete except Medley.

Common Lisp
: The subject of a 10-year standards process to converge multiple dialects of the
Lisp language. Strong influences from many Lisp dialects, including Interlisp.

Common Lisp the Language
: Book by Guy Steele with two editions:

- CLtL1 – edition 1, 465 pages
- CLtL2  – second edition, 1029 pages

Common Lisp dpANS
: The ANSI Standard for Common Lisp.

Starting with the Lyric release of Interlisp-D and then the Medley release, the implementation of Medley included implementations of Common Lisp (CLtL 1) as well as the Interlisp dialect in a single development environment; this was made possible by using the (Common Lisp) “package” feature to allow both dialects to be intermixed.

Dfasl
: A compiled form of Medley Interlisp files with the extension ".dfasl".

Display
: Denotes a program or system with a Graphical User Interface or a full screen character interface, as opposed to a line oriented interface like a teletype. In expressions like "display oriented editor" or "display editor".

DLISP
: By Warren Teitelman: a first attempt at building a “Display” (GUI) with Interlisp running on MAXC (a PDP-10 clone) connected by Ethernet to a Xerox Alto acting 
as a graphics terminal.

Dorado Lisp
: The reimplementation of the AltoLisp microcode on the Dorado – a research prototype.

Fugue
: An obsolete named release of Interlisp-D.

Harmony
: An obsolete named release of Interlisp-D.

Intermezzo
: An obsolete named release of Interlisp-D.

Interlisp
: A GitHub “organization” with ~20 repositories, see <https://github.com/Interlisp>
: Both a language and, in some cases, the implementation of that language. Usually used with some other wording or refinement.

Interlisp: The Language and its usage
: A book by Steve Kaisler which describes Interlisp of the 1970s & 80s.

Interlisp.org
: The project's Internet domain name, used for its websites and email addresses.

- <https://interlisp.org>  – the address of the main web site
- <https://online.interlisp.org> – the address of a service that lets you run Medley
- <info@interlisp.org>             - the project's general information email address

Interlisp-10
: The first implementation of Interlisp for the Digital Equipment Corporation (DEC) PDP-10 / Tenex.

Interlisp-360
: Implemention of Interlisp for the IBM-360.

Interlisp-D
: What Dorado Lisp became.  The D stood for both “Display” and “D-machine”.  An implementation of

- Interlisp the language
- The Interlisp programming tools
- A Graphical User interface to Interlisp programming development
- A large number of tools, utilities, games, screen-savers
- A Lisp-based operating system for D-machines which, when coupled with microcode
  implementation of a Virtual Machine, allowed the D-machines to operate as a
  personal workstation. Each D-machine had its own microcode with different
  configurations and micro-instructions.

Interlisp-VAX
: Implementation of Interlisp for Digital Equipment Corporation VAX systems.

Koto
: An obsolete named release of Interlisp-D.

Lcom
: Used as a file ending, xxx.lcom, for compiled Medley files.

Lyric
: An obsolete named release of Interlisp-D.

Medley
: The final named release of Interlisp-D.  

Medley 1.0, Medley 2.01, Medley 3.5 numbered releases of Interlisp-D
: At some point the name Interlisp-D was retired and Medley used to name the software.

Maiko
: An implementation of the functions of the D-machine microcode, but written in C for the
      Sun Microsystems SPARC processor workstation, initially developed by
       Fuji Xerox.  Subsequently ported to little-endian processors and other operating systems.

Package
: The term Package has several different meanings depending on the context:

- Informally, a collection of utilities or submodule in Interlisp (the "break package", q.v.; the "file package", a facility for managing code changes; the "record package", a record data type; and so on)
- A feature of Commmon Lisp symbol support; the package system allows the combining of Interlisp symbols (written with `IL:` prefix) and Common Lisp symbols (written with a `LISP:` prefix).

SDL
: Structured Design Language.

Sysout
: A file containing the saved state of Interlisp virtual memory.

X11
: The X Window System.

### Organizations

BBN
: [Bolt, Beranek, and Newman](https://en.wikipedia.org/wiki/Raytheon_BBN), a Cambridge, Mass. consulting firm which sponsored the
      creation of BBN Lisp, Interlisp's immediate ancestor, as well as the Tenex operating system.

Xerox PARC or just PARC
: Palo Alto Research Center, which continued in collaboration with BBN on (renamed) Interlisp. PARC developed the Alto and Dorado.  Now part of SRI International.

SRI International
: A non-profit scientific R & D institute, headquertered in Menlo Park, California.

Xerox Electro-Optical Systems (XEOS)
: A former Xerox division supporting government customers.

Xerox Artificial Intelligence Systems (XAIS)
: The former Xerox division working to commercialize Xerox workstations running Interlisp-D.

Rank Xerox
: Xerox's European subsidiary, a joint venture of Xerox Corp. and the Rank Organization, which sold Interlisp-D workstations in Europe.

Fuji Xerox
: Xerox's Japanese subsidiary, owned jointly by Rank Xerox and Fujifilm Corp., responsible for selling and supporting Interlisp-D systems in Japan.

Envos
: Company founded in 198x to take on the Lisp business from Xerox. Closed within 10 months and folded back into Xerox.

Venue
: Company founded by John Sybalsky, former Xerox and Envos employee, which obtained a license to create and distribute derivative works of Maiko and Medley.

Medley Interlisp Project
: Began late 2010’s with Nick Briggs getting Maiko to run on macOS.  The group expanded and began holding weekly online meetings in 2020.
Subsequently ported Maiko (and therefore Medley) to Linux, Windows, and other operating system.  Maintains a mailing list for developers and interested users,
sponsors the maintenance of an exhaustive bibliography and the very website where you're reading this.

InterlispOrg
: A [California-registered](https://rct.doj.ca.gov/Verification/Web/Details.aspx?result=c7aa8cb2-16ec-458a-be56-41f963365258) non-profit organization  (DBA Interlisp.org) Established
        August 2021. 501c3  EIN 87-2528093  California registered charity CT0278267.
        The Board of Directors consists of Larry Masinter, President; Ron Kaplan, Treasurer; and Herb Jellinek, Secretary.
