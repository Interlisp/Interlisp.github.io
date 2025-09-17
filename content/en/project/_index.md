---
Title: The Medley Interlisp Project
weight: 2
type: docs
aliases:
 - /hugo/
 - /medley/project/
 - /medley/about/
 - /medley/other/
---
#  Reviving a Groundbreaking System

## What are we trying to accomplish?

Our aim is to allow Medley to "live again": to be usable enough on modern systems that someone could develop some code and experience what it was like to use this groundbreaking system. You could think of this as a kind of "*vintage software*" project, to try to capture the sense of fluidity in the development cycle.

As part of this effort we explore alternate system technologies such as SDL2/SDL3 as a graphics backend and [running Medley in the browser via WebAssembly](http://wasm.interlisp.org/medley.html) (experimental, doesn't save files).

We also hope to provide a platform for supporting the revival of systems developed using Interlisp, including 1980's work in hypertext (NoteCards), desktop management (Rooms), object-oriented programming (LOOPS), linguistics (LFG Grammar Writer’s Workbench), user interface design (Trillium), geopolitical simulation (STRADS), and intelligent database assistants (DADM).

The lessons from the Interlisp interactive environment are likely more relevant in today's "devops" environment -- managing large networks of independent microservices, with no single serialization of the components quite comprehensible. Development in this model has been called "repl-driven development": you are working in the 'live' environment (or a copy) making changes without a separate, lengthy edit-compile-load-restart.

For more on the work we're doing, see [Reviving Medley](reviving) and [News and Status Reports](status).

## What are our challenges?

"Reviving" old software requires some judgment of tradeoffs. There are often disagreements. Backward compatibility, fixing what seems to be a bug might cause other problems.

We are trying to address this conflict by also making older versions of Interlisp available. There is an emulator for the Xerox 1108 (Dandelion) D-machine that will run the old software unchanged, it is slow and cumbersome; not something you would want to use for day-to-day work. 

## Who is involved?

We are [some of the original developers and users of Interlisp](/project/credits) 30 years ago, joined by newcomers interested in software history and preservation, along with members of the Lisp community. We work with [organizational partners](partners). And with you!

[Get involved](getinvolved) by running Medley, testing and reporting bugs and anomalies, participate to our discussions, and other opportunities to contribute with or without coding skills.

## Why?

People involved with the project have [different stories](stories) for why they are interested. The [1992 ACM Software System Award](https://awards.acm.org/award-recipients/masinter_3814811), awarded to the Interlisp system for pioneering work in programming environments, recognizes an influence over computer science that is broader than these individual stories and funnels them.

The paper [The Medley Interlisp Project: Reviving a Historical Software System](https://interlisp.org/documentation/young-ccece2025.pdf) expresses our motivations for preserving Medley and traces the journey to making the system and its lessons widely accessible:

> [the project] aims to render Medley Interlisp, the final release of Interlisp, usable on modern operating systems and hardware environments, and to selectively add modern capabilities to Medley while conserving its value as a historically groundbreaking system.
