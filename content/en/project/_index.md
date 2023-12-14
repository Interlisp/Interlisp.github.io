---
title: The Medley Interlisp Project: Reviving a Groundbreaking System
weight: 2
type: docs
aliases:
 - /hugo/
 - /medley/project/
 - /medley/about/
 - /medley/other/
---

## What are we trying to accomplish?

Our aim is to allow Medley to "live again": to be useable enough on modern systema that someone could develop some code and experience what it was like to use this groundbreaking system. You could think of this as a kind of "*vintage software*" project, to try to capture the sense of fluidity in the development cycle. 

We also hope to provide a platform for revival of systems developed using Interlisp., including 1980's work in hypertext (Notecards), desktop management (Rooms), and object-oriented programming (LOOPS).

## What are our challenges?

Being compatible with modern systems requires compensating for changes input and output channels.  Mouse, cursor, scroll wheels need to function in the expected way. Support for the plethora of different keyboard layouts available today requires rearchitecting some of the lowest levels of stream handling. The replacement of the "XCCS" (Xerox Character Code Standard) with Unicode isn't complete. Today's screens are bigger. CPUs are multi-threading, Big-endian 64-bit character codes. Three-button mouse vs. one button. Subtle bugs because of change of address space.

We also want to restore and present earlier versions of Interlisp, for the student of computer history. 

We have done a lot of cleanup and adaptation, to make Medley usable again in the modern world. Among other developments, you can now run Medley Interlisp on many OS and hardware configurations, or in the cloud, using a web browser. 

We have also developed tools for managing the GitHub workflow, to integrate the Interlisp style development with git and GitHub, Docker and other modern components.

## Who is involved?

We are [some of the original developers and users of Interlisp](/project/credits) 30 years ago, joined by newcomers interested in software history and preservation, along with members of the Lisp community. We work with [organizational partners](partners). And with you!

<div class="mx-auto">
 <a class="btn btn-lg btn-danger mr-3 mb-4" href="">
  How do I get involved?<i class="fas fa-arrow-alt-circle-right ml-2"></i>
a </a>
</div>

## Why?

People have [different stories](stories) for why they are interested.


A presentation from the 2020 Remote Chaos Experience conference highlights some of the interesting aspects of Interlisp.  

[What have we lost?](https://www.youtube.com/watch?v=7RNbIEJvjUA&t=841s)  

The presentation synopsis states it this way:
> We have ended up in a world where UNIX and Windows have taken over, and most people have never experienced anything else. Over the years, though, many other system designs have come and gone, and some of those systems have had neat ideas that were nevertheless not enough to achieve commercial success. We will take you on a tour of a variety of those systems, talking about what makes them special.
