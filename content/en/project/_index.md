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

Our aim is to allow Medley to "live again": to be useable enough on modern systems that someone could develop some code and experience what it was like to use this groundbreaking system. You could think of this as a kind of "*vintage software*" project, to try to capture the sense of fluidity in the development cycle. 

We also hope to provide a platform for revival of systems developed using Interlisp, including 1980's work in hypertext (Notecards), desktop management (Rooms), and object-oriented programming (LOOPS).

The lessons from the Interlisp interactive environment is likely more relevant in today's "devops" environment -- managing large networks of independent microservices, with no single serialization of the components quite comprehensible. Development in this model has been called "repl-driven development": you are working in the 'live' environment (or a copy) making changes without a separate, lengthy edit-compile-load-restart.

## What are our challenges?

"Reviving" old software requires some judgment of tradeoffs. There are often disagreements. Backward compatibility, fixing what seems to be a bug might cause other problems. For more on the work we're doing, see [Reviving Medley](reviving) and [Status](status).

We are trying to address this conflict by also making older versions of Interlisp available. There is an emulator for the Xerox 1108 (Dandelion) D-machine that will run the old software unchanged, it is slow and cumbersome; not something you would want to use for day-to-day work. 

## Who is involved?

We are [some of the original developers and users of Interlisp](/project/credits) 30 years ago, joined by newcomers interested in software history and preservation, along with members of the Lisp community. We work with [organizational partners](partners). And with you!

<div class="mx-auto">
 <a class="btn btn-lg btn-danger mr-3 mb-4" href="getinvolved/">
  How do I get involved?<i class="fas fa-arrow-alt-circle-right ml-2"></i>
</a>
</div>

## Why?

People have [different stories](stories) for why they are interested.


A presentation from the 2020 Remote Chaos Experience conference highlights some of the interesting aspects of Interlisp.  

[What have we lost?](https://www.youtube.com/watch?v=7RNbIEJvjUA&t=841s)  

The presentation synopsis states it this way:
> We have ended up in a world where UNIX and Windows have taken over, and most people have never experienced anything else. Over the years, though, many other system designs have come and gone, and some of those systems have had neat ideas that were nevertheless not enough to achieve commercial success. We will take you on a tour of a variety of those systems, talking about what makes them special.
