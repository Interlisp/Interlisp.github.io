---
title: Vocabulary
weight: 90
type: docs
---

The names “Medley” “Medley Interlisp” “Interlisp” “Interlisp.org” “Common Lisp” in ways that are confusing. We’re talking about a lot of different things. And these are mostly not terms that we’ve made up, they’re cemented in by the titles that have appeared in different publications.

## Vocabulary and relationships

Interlisp.org
: a “domain name”, used for some web sites and email addresses

- <https://interlisp.org>  – the address of the main web site
- <https://online.interlisp.org> – the address of a service that lets you run Medley
- <info@interlisp.org>             - an email address of a group that can respond to questions

InterlispOrg
: A California-registered non-profit organization  (DBA Interlisp.org) Established
        August 2021. 501c3  EIN 87xxxx  California registered charity NNNNN.
        President Larry Masinter, Treasurer Ron Kaplan, Secretary Herb Jellinek.

Interlisp
: A GitHub “organization” with ~20 repositories, see <https://github.com/Interlisp>
: Both a language and, in some cases, the implementation of that language. Usually used with some other wording or refinement

Interlisp: The Language and its usage
: A book by Steve Kaisler which describes Interlisp of the 1970s & 80s

Interlisp-10
: The first implementation of “Interlisp” for the DEC PDP-10 / Tenex

Interlisp-VAX, Interlisp-360
: Other implementations of Interlisp for other machines (sharing source code)

DLISP
: By Warren Teitelman: a first attempt at building a “Display” (GUI) with
           Interlisp running on Maxc (A PDP-10 clone a Xerox Alto as a
           graphics terminal connected to it via Ethernet).

Alto Lisp
:  An (unsuccessful) attempt to build a Lisp-based OS for running Interlisp on an Alto

Dorado Lisp
: The reimplementation of AltoLisp microcode for the Dorado – a research prototype

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

Carol, Fugue, Harmony, Intermezzo, Koto, Lyric, Medley
: Named releases of Interlisp-D.  All are obsolete except Medley.

Medley 1.0, Medley 2.01, Medley 3.5 numbered releases of Interlisp-D
: At some point the name Interlisp-D was retired and Medley used to name the software.

Maiko
: An implementation of the functions of the microcode D-machine, but written in C for the
      Sun Microsystems (RISC-like) SPARC processor workstation, initially developed by
       Fuji Xerox.  Subsequently ported to little-endian processors and other operating systems.

Common Lisp
: The subject of a 10-year standards process to converge multiple dialects of the

- Lisp language.
- Strong influences from many Lisp dialects, including Interlisp.

Common Lisp the Language
: Book by Guy Steele with two editions:

- CLtL1 – edition 1, 465 pages
- CLtL2  – second edition, 1029 pages

Common Lisp dpANS
: The ANSI Standard for Common Lisp

Starting with the Lyric release of Interlisp-D and then the Medley release, the implementation of Medley included implementations of Common Lisp (CLtL 1) as well as the Interlisp dialect in a single development environment; this was made possible by using the (Common Lisp) “package” feature to allow both dialects to be intermixed.

### Organizations

BBN
: Boston consultancy which (late 60s) implemented BBN Lisp and the Tenex operating system.

Xerox PARC or just PARC
: Palo Alto Research Center, which continued in collaboration with BBN on (renamed) Interlisp. PARC developed the Alto and Dorado.  Now part of SRI International.

SRI International
: non-profit scientific R & D institute

Xerox Electro-Optical Systems (XEOS)
: Xerox division supporting classified customers

Xerox Artificial Intelligence Systems (XAIS)
: The division working to commercialize Xerox Workstations running Interlisp-D.

Rank Xerox
: Xerox affiliate in charge of delivering Interlisp-D workstations in Europe

Fuji Xerox
: Xerox affiliate – joint project of Rank Xerox and Fuji Photo Film company.

Envos
: Company founded in 198x to take on the Lisp business from Xerox. Closed within 10 months and folded back to Xerox. 

Venue
: Smaller company, started by John Sybalsky; it had the license to create and distribute derivative works of Maiko and Medley   Venue ceased operations… … some history …. Software recovered from late 90s…. Fuji Xerox worked with John into the 90s with ports and addons and other software….

Medley Interlisp Project
: began late 2010’s with Nick Briggs getting Maiko to run on MacOS.
In earnest in 2020 with start of weekly Zoom meetings, getting it to run on Linux in a VM and getting the Interlisp and LispCore google groups and ….
