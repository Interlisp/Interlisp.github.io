---
title: Project
weight: 2
type: docs
aliases:
 - /hugo/
 - /medley/project/
 - /medley/about/
 - /medley/other/
---
## What is the Medley Interlisp Project?

The Medley Interlisp Project was created to revive the "Interlisp experience" by creating an environment that could be used by (and might even be useful for) modern users. Starting from the 20-year-old sources for the not-quite-released Medley 3.5 version of Interlisp, we have made good progress adapting Medley to work in the current environment -- open source, GitHub integration, improving Common Lisp support, running on a wide variety of platforms -- but there is much more to be done.

Because of the long history of naming and renaming of groups, software, environments, machines, languages, we have created a [glossary of terms](glossary).

## What are the origins of Medley and Interlisp?

The 1970s and 80s saw major advances in computing and Human-Computer interaction.  At Xerox PARC there were four IDEs developed with different approaches: Smalltalk, with an object-oriented system; Interlisp, for researchers in AI and exploratory development; Cedar/Mesa, with a strongly typed language for software engineering. They each had a different model for source code management, development and versioning. In common they shared an infrastructure and vision computing and distributed systems, with support for Ethernet networking, printing, file servers and network protocols. Each environment had its own Virtual Machine instruction set tuned for the language "all the way down", in a single address space, in a way that opened the systems to customization.

There were several different [D-machines](http://www.bitsavers.org/pdf/xerox/parc/Exploring_the_Ethernet_with_Mouse_and_Keyboard_May81.pdf): Dorado, Dolphin, Dandelion, Daybreak, and others. Each environment had its own microcode to implement its instruction set; once loaded, each would take over the machine -- there was no OS. Each had large-screen black and white CRTs for a graphical user interface, mouse and cursor pointer, high quality fonts.

Xerox marketed the Interlisp-D enviornment primarily to the AI community world wide, starting in 1980, from XEOS to Xerox Artificial Intelligence Systems, then a spin-out company called Envos, and then further development and porting to other systems by a company called Venue, until development tapered off. Along the way, the name changed from Interlisp-D to Medley.

We started with sources from Venue for a not-quite-finished release of what was to be Medley 3.5.

## What are we trying to accomplish?

Our aim is to allow *Medley Interlisp* to "live again": usable on modern systems, sufficient to allow someone to develop some code and experience what it was like to use this groundbreaking system. You could think of this as a kind of "*vintage software*" project, to try to capture the sense of fluidity in the development cycle. 

We hope to provide a platform for demonstration of early experiments of hypertext (Notecards), Desktop management (Rooms), Object-oriented programming (LOOPS), as well as Interlisp itself.

## What are our challenges?

Since we aim to revive Medley Interlisp to support not just a demo or test drive, but actual use as a development and learning tool, we need to overcome a number of compatibility problems with current systems and interfaces.

We also want to restore and present earlier versions of Interlisp, for the student of computer history. For more information go to [Interlisp and Software Preservation Network](https://www.softwarepreservationnetwork.org/Interlisp/).

## What have we done so far?

We have done a lot of cleanup and adaptation to make Interlisp Medley usable again in the modern world. Among other developments, you can now run Medley Interlisp on many OS and hardware configurations, or in the cloud, using a web browser.

We've also been working on integration of the Interlisp style development with git and GitHub, Docker and other modern components.

<div class="mx-auto">
 <a class="btn btn-lg btn-danger mr-3 mb-4" href="">
  How do I access and use Medley?<i class="fas fa-arrow-alt-circle-right ml-2"></i>
 </a>
</div>

## Who is involved?

We are some of the original developers and users of the system 30 years ago, joined by newcomers interested in software history and preservation, along with members of the Lisp community. We work with [organizational partners](partners). And with you!

<div class="mx-auto">
 <a class="btn btn-lg btn-danger mr-3 mb-4" href="">
  How do I get involved?<i class="fas fa-arrow-alt-circle-right ml-2"></i>
 </a>
</div>

## Check out this presentation for more information

A presentation from the 2020 Remote Chaos Experience conference highlights some of the interesting aspects of Interlisp.  

[What have we lost?](https://www.youtube.com/watch?v=7RNbIEJvjUA&t=841s)  

The presentation synopsis states it this way:
> We have ended up in a world where UNIX and Windows have taken over, and most people have never experienced anything else. Over the years, though, many other system designs have come and gone, and some of those systems have had neat ideas that were nevertheless not enough to achieve commercial success. We will take you on a tour of a variety of those systems, talking about what makes them special.
