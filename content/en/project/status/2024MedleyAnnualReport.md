---
title: 2024 Medley Interlisp Annual Report
weight: 1
type: docs
aliases:
 - /news/2024medleyannualreport/
 - /project/news/2023medleyannualreport/
---

<img src="/Resources/logo_red_no_border_568x385.png" width="284" height="194"></img>

## **Overview**

Interlisp-D (and the Medley version of it) were originally developed at the Xerox Palo Alto Research Center (PARC) in the 1970’s and 80’s. It was a software environment for rapid prototyping, research and Artificial Intelligence, combining the power of the Lisp language and system elements with the now common PARC-born Windows/Icon/Mouse/Pointer graphical user interface.  

The Medley Interlisp project was started in 2020 by a few of the original developers, focusing on reviving the software, making it usable and useful on modern systems. With permission from the last licensee of the software, we are able to release the system as open source. This report highlights the accomplishments and continuing projects over 2024.

For more information, see [https://interlisp.org](https://interlisp.org). There you will find:

* [History](https://interlisp.org/history/): The timeline of Interlisp, Medley, and applications written in or for it.  
  * An extensive bibliography of citations, articles, videos and other online material with pointers to the literature ([https://interlisp.org/bibliography](https://interlisp.org/bibliography/))  
  * A Glossary of terms used in conjunction with the software.  
* [Project](https://interlisp.org/project/): The Medley Interlisp Project itself – how we work, how to get involved  
  * Get Involved  
  * Donate  
* [Software](https://interlisp.org/software/): How you can try Medley online, install it, and pointers to documentation of components and applications a modern day user can try.

## **Progress and Key Accomplishments**

### **Lowered Barriers to Entry**

We continue working to make it easier to try out and use Medley Interlisp.

* **Medley Online**: We support and enhance our Docker-based Web version, [online.interlisp.org](http://online.interlisp.org).  This allows anyone with a browser to connect to a server running (a unique instance of) Medley “in the cloud”. It provides the full experience of using Medley to develop applications.  
* **Emscripten/WASM:** Emscripten is a compiler toolchain that outputs “Web Assembly” (WASM) code. We have an experimental Emscripten/WASM build of the Maiko virtual machine that allows Medley to run entirely in the user’s Web browser, available to try at [http://wasm.interlisp.org/medley.html](http://wasm.interlisp.org/medley.html).  In the long-term, we’re considering it to replace the “in-cloud” Medley now found at [https://online.interlisp.org](https://online.interlisp.org).  
* **Improved Medley startup:** Added new features to the `medley` command line program for macOS, Windows, and Linux.  
* **Improve Cursor Visibility**: Added X11 [cursor foreground and background color options](https://github.com/Interlisp/medley/issues/1820) to Maiko, to aid legibility and accessibility.

### **Documentation improvements**

* Extended the `MAN` manual browser tool to cover LispUsers (contributed software) packages.  
* Added [Meta-D command to bring up documentation](https://github.com/Interlisp/medley/pull/1624) for selected items in SEdit and TEdit.  
* Added Truckin’ documentation to LOOPS sources.  
* Created [PDF files for viewing Lisp source code and documentation](https://files.interlisp.org/medley/) without running Medley.  
* Posted Volume I of Stephen Kaisler’s Medley LOOPS book series, [*LOOPS: The Basic System*](https://interlisp.org/documentation/2024-loops-book-1.pdf).

### **ANSI Common Lisp Compatibility**

ANSI Common Lisp was standardized 30 years ago, after much of the Medley Common Lisp implementation was completed.  We’re working to complete this project.

* We [identified discrepancies in Medley’s Common Lisp implementation](https://github.com/orgs/Interlisp/discussions?discussions_q=Evaluating+Medley+compatibility+with+practical+common+lisp) by testing against the examples in [*Practical Common Lisp*](https://gigamonkeys.com/book/) by Peter Seibel.  
* Among other things, we added an [initial implementation of the Common Lisp LOOP macro](https://github.com/Interlisp/medley/issues/1578) and began work on `SYMBOL-MACROLET`.

### **Medley System Infrastructure**

* **Modern font support**: Began BDF reader implementation to allow us to import additional fonts.  
* **Portability**: Initial work to support the SDL3 UI library.  
* **Networking**: We have done very early work on an updated Medley TCP/IP stack.  Interlisp predated the definition and widespread adoption of TCP/IP networking, using Xerox’s PUP and XNS protocol stacks instead.  Prior releases of Medley included TCP/IP support, but we found it to be unstable.  
* **Automated building new versions:** In 2024 we completed the automation of producing new versions of Medley Online and Medley installers for a variety of platforms.
* **Automated Medley Online build and deployment on GitHub:** We refined our use of GitHub’s CI (Continuous Integration) tools to prepare new Medley software releases.  (GitHub is a version/configuration management system used by many software developers, especially in open source.)

### **Medley Applications**

* **TEdit**: TEdit is Medley’s WYSIWYG rich text editor with programmatic support for images.  It has been a key component of many other Medley applications.  We simplified the code to ease maintenance and improve performance. We modularized the public API and extended some capabilities. We prepared the code to move TEdit into its own package namespace.  
* **HTML support**: Began work to add HTML support to Medley’s device-independent graphics suite.  
* **Lafite**: A multi-protocol, GUI email client written in Lisp using TEdit.  We [improved Lafite module loading](https://github.com/orgs/Interlisp/discussions/1551) to make it work better with Unix spool files and mail transport agents.  
* **Source code tools**: We continue to develop and extend tools that bridge the Medley residential programming model and contemporary source control tools (git, GitHub, etc.). In 2024,  we made improvements to COMPARESOURCES, GITFNS  
* **New tools**: We created a number of new tools, including INSPHEX, a tool for exploring binary data (similar to the Linux utility `hd)`, and Stringscope, which displays a list of text strings found in a binary file, akin to the Linux `strings` program.

### **Reviving Related Systems**

Our previous work has focused mostly on core Medley capabilities.  In 2024 we broadened our focus to include systems built in or on top of Medley.

* **Revive and debug LOOPS**:  [LOOPS](https://xeroxparcarchive.computerhistory.org/indigo/loops/doc/manual/.CHAPLOOPS.PRESS!2.pdf), the Lisp Object-Oriented Programming System, was a Xerox PARC project to add data, object, and rule oriented programming to Interlisp’s procedure-oriented programming paradigm.  It was a predecessor of CLOS, the object-oriented programming component of Common Lisp.  
* **NoteCards**: NoteCards is an desktop and networked hypertext system developed on Interlisp at PARC starting in the early 1980’s.  This year we continued to update and modernize NoteCards in conjunction with updates to TEdit and other aspects of the Interlisp system.  In addition, as an entry to an Internet contest in retro-computing, we developed the first new NoteCards type (the Web card) since the 1990’s using the NoteCards Programmer’s Interface.  
* **Grammar Writers’ Workbench for Lexical Functional Grammar**: The Grammar Writer’s Workbench was constructed in the 1980s as a comprehensive graphical platform for linguistic and algorithmic research within the LFG theoretical framework (*Lexical Functional Grammar: A formal system for grammatical representation*, Kaplan and Bresnan, 1982). LFG research and teaching can still benefit from the system’s flexible interface for grammar development and testing against phenomena in a wide variety of languages.
* **Older Medley systems:** The version of Medley we started with was Medley 3.5 – an enhancement from Medley 2.0 that was the last release from Venue. But we also have archives of older Medley 2.0 compatible memory images. We can use these for preservation, testing compatibility, debugging, and running older demos. We made some progress on running these with our current emulator sources, the Harmony release of Interlisp-D using DarkStar (an emulator of the Xerox Dandelion workstation), and Medley 2.0 on DOS. These older release implementations still need some finishing, but the experiments are encouraging.

### **Issues Closed and PRs Merged**

We closed 89 GitHub Issues and merged 150 Medley pull requests and 35 Maiko pull requests in 2024 (through December 26).

## **Community Engagement**

### **Meetings**

We hold two online meetings per week: a Monday meeting focused on implementation issues, and a Wednesday meeting to discuss everything else Medley-related.  The meetings are open to everyone who wishes to attend on request to [info@interlisp.org](mailto:info@interlisp.org).

### **Community Projects**

Alexander Shendi is working on porting Medley to [Haiku OS](https://www.haiku-os.org/), a modern operating system inspired by BeOS.

Douglas Lenat’s Eurisko, an early AI system of historical importance, is now running on Medley.

We interviewed Italian researchers who used Interlisp in the 1980s for their recollections.

Paolo Amoroso entered [RetroChallenge 2024](https://www.retrochallenge.org/) with a NoteCards project, WebCard.

### **Website Enhancements**

We added a user feedback widget to pages on the Interlisp.org website and commenced initial work on fetching Zotero collection names for a more useful, well-search-engine-optimized bibliography.

We continued to improve our website deployment processes, creating Production and Staged website deployments.  We also cleaned up the website generator configuration file, refactoring it to improve maintainability and support multiple deployment environments.

The website page navigation was restructured to make the documentation section more prominent, and made PDF/HTML versions of documentation, TEdit files, and Lisp sources accessible via interlisp.org. This work is still in progress.

### **Publications and Presentations**

Andrew Sengul submitted a paper, [*The Medley Interlisp Revival*](https://doi.org/10.5281/zenodo.11090093), to the European Lisp Symposium 2024\.  It was accepted and published in the proceedings.  Andrew gave an accompanying [talk at the symposium](https://www.youtube.com/watch?v=ZBAJukF5mPE).

Herb Jellinek contributed Interlisp expertise to assist in evaluating historical materials for the book [*Firesign: The Electromagnetic History of Everything as Told on Nine Comedy Albums*](https://www.ucpress.edu/books/firesign/paper) by Jeremy Braddock.

### **Awards**

We applied for the 2024 Tony Sale Award for Computer Conservation and Restoration, sponsored by the (UK) Computer Conservation Society. We were not selected this year, but the experience has encouraged us to consider reapplying when CCS runs the next competition.

### **Collaborations**

#### University of Alberta

We began a collaboration with Professor Eric Kaltman and graduate students Eleanor Young and Abhik Hasnain of the University of Alberta [Software History Futures and Technologies (SHFT) Group](https://www.shft.group/pages/team/eric-kaltman/).

Eleanor has worked on organizing the Interlisp Bibliography, tagging, researching and adding missing metadata to hundreds of bibliography entries.  She has also begun work on an academic paper outlining the Medley project’s history and processes, intended as a guide for other software revival projects.

Abhik has worked on reviewing incomplete bibliography entries, including tracking files and updating metadata and tags. Currently he is focused on proofreading, testing, and modernizing the text and code examples in the Medley Primer (a.k.a. *Medley for the Novice*) to serve as a quickstart guide.

#### Libraries and Archives

Worked with PARC/SRI, Stanford Library, UC Berkeley Library, the Internet Archive, and other institutions to preserve printed and recorded material relating to Interlisp and other Xerox PARC research projects.

#### Internal Processes

Defined a process for prioritizing and working on issues and pull requests and made responding to issues raised by more-casual users a priority.

## **Looking Ahead**

In the coming year we will emphasize removing obstacles to getting started using Medley.  Plans include publishing an updated Primer suited to online.interlisp.org as well as modern operating systems and their users, and producing “one-click” installers to make it simple to set up and run Medley on personal computers.  We also hope to create an online version of LFG for use by linguists around the world.

In the area of retrocomputing, we aim to see what if any changes are required to get [Bernie Cosell’s ELIZA, written in BBN Lisp ca. 1969](https://sites.google.com/view/elizagen-org/eliza-clones?authuser=0#h.zdqi9um6k4za), running in its descendent Medley.

We anticipate that we will be able to fund a Computer Science graduate student to work on some more-difficult projects.

In general, we will continue our work on Medley, emphasizing outreach, documentation, modernization, and education.

## **Acknowledgements**

We thank our contributors, supporters, and the wider community for making this journey possible.
