# **![][image1]**

# **2024 Medley Interlisp Project** **Annual Report**

## **Overview**

Interlisp-D (and the Medley version of it) were originally developed at the Xerox Palo Alto Research Center (PARC) in the 1970’s and 80’s. It was a software environment for rapid prototyping, research and Artificial Intelligence, combining the power of the Lisp language and system elements with the now common PARC-born Windows/Icon/Mouse/Pointer graphical user interface.  

The Medley Interlisp project was started in 2020 by a few of the original developers, focusing on reviving the software, making it usable and useful on modern systems. With permission from the last licensee of the software, we are able to release the system as open source. This report highlights the accomplishments and continuing projects over 2024\. 

For more information, see [https://interlisp.org](https://interlisp.org). There you will find:

* [History](https://interlisp.org/history): The timeline of Interlisp, Medley, and applications written in or for it.  
  * An extensive bibliography of citations, articles, videos and other online material with pointers to the literature ([https://interlisp.org/bibliography](https://interlisp.org/bibliography))  
  * A Glossary of terms used in conjunction with the software.  
* [Project](https://interlisp.org/project/): The Medley Interlisp Project itself – how we work, how to get involved  
  * Get Involved  
  * Donate  
* [Software](https://interlisp.org/software/): how you can try Medley online, install it, and pointers to.documentation of components and applications a modern day user can try.

## 

## **Progress and Key Accomplishments**

### **Lowered Barriers to Entry**

We continue working to make it easier to try out and use Medley Interlisp.

* **Medley Online**: We support and enhance our Docker-based Web version, [online.interlisp.org](http://online.interlisp.org).  This allows anyone with a browser to connect to a server running (a unique instance of) Medley “in the cloud”. It provides the full experience of using Medley to develop applications.  
* **Emscripten/WASM:** Emscripten is a compiler toolchain that outputs “Web Assembly” (WASM) code. We have an experimental Emscripten/WASM build of the Maiko virtual machine that allows Medley to run entirely in the user’s Web browser, available to try at [http://wasm.interlisp.org/medley.html](http://wasm.interlisp.org/medley.html).  In the long-term, we’re considering it to replace the “in-cloud” Medley now found at [https://online.interlisp.org](https://online.interlisp.org).  
* **Improved Medley startup:** Added new features to the “`medley`” command line program for macOS, Windows, and Linux.  
* **Improve Cursor Visibility**: Added X11 [cursor foreground and background color options](https://github.com/Interlisp/medley/issues/1820) to Maiko, to aid legibility and accessibility.

### **Documentation improvements**

* Extended the `MAN` manual browser tool to cover LispUsers (contributed software) packages.  
* Added [Meta-D command to bring up documentation](https://github.com/Interlisp/medley/pull/1624) for selected items in SEdit and TEdit.  
* Added Truckin’ documentation to LOOPS sources.  
* Created [PDF files for viewing Lisp source code and documentation](https://files.interlisp.org/medley/) without running Medley.  
* Posted Volume I of Stephen Kaisler’s Medley LOOPS book series, [*LOOPS: The Basic System*](https://interlisp.org/documentation/2024-loops-book-1.pdf)*.*

### **ANSI Common Lisp Compatibility**

ANSI Common Lisp was standardized 30 years ago, after much of the Medley Common Lisp implementation was completed.  We’re working to complete this project.

* We [identified discrepancies in Medley’s Common Lisp implementation](https://github.com/orgs/Interlisp/discussions?discussions_q=Evaluating+Medley+compatibility+with+practical+common+lisp) by testing against the examples in [*Practical Common Lisp*](https://gigamonkeys.com/book/) by Peter Seibel.  
* Among other things, we added an [initial implementation of the Common Lisp LOOP macro](https://github.com/Interlisp/medley/issues/1578) and began work on SYMBOL-MACROLET.

### **Medley System Infrastructure**

* **Modern font support**: Began BDF reader implementation to allow us to import additional fonts.  
* **Portability**: Initial work to support the SDL3 UI library.  
* **Networking**: We have done very early work on an updated Medley TCP/IP stack.  Interlisp predated the definition and widespread adoption of TCP/IP networking, using Xerox’s PUP and XNS protocol stacks instead.  Prior releases of Medley included TCP/IP support, but we found it to be unstable.  
* **Automated building new versions:** In 2024 we completed the automation of producing new versions of Medley Online and Medley installers for a variety of platforms.   
* **Automated Medley Online build and deployment on GitHub:** We refined our use of GitHub’s CI (Continuous Integration) tools to prepare new Medley software releases.  (GitHub is a version/configuration management system used by many software developers, especially in open source.)

### **Medley Applications**

* **TEdit**: TEdit is Medley’s WYSIWYG rich text editor with programmatic support for images.  It has been a key component of many other Medley applications.  We simplified the code for maintenance and performance, extended some capabilities, and modularized the public API as well as preparing for future packaging.  
* **HTML support**: Began work to add HTML support to Medley’s device-independent graphics suite.  
* **Lafite**: A multi-protocol, GUI email client writing in Lisp using TEdit.  We [improved Lafite module loading](https://github.com/orgs/Interlisp/discussions/1551) to make it work better with Unix spool files and mail transport agents.  
* **Source code tools**: We continue to develop and extend tools that bridge the Medley residential programming model and contemporary source control tools (git, GitHub, etc.). In 2024,  we made improvements to COMPARESOURCES, GITFNS  
* **New tools**: We created a number of new tools, including INSPHEX, a tool for exploring binary data (similar to the Linux utility `hd)`, and Stringscope, which displays a list of text strings found in a binary file, akin to the Linux `strings` program.

### **Reviving Related Systems**

Our previous work has focused mostly on core Medley capabilities.  In 2024 we broadened our focus to include systems built in or on top of Medley.

* **Revive and debug LOOPS**:  [LOOPS](https://xeroxparcarchive.computerhistory.org/indigo/loops/doc/manual/.CHAPLOOPS.PRESS!2.pdf), the Lisp Object-Oriented Programming System, was a Xerox PARC project to add data, object, and rule oriented programming to Interlisp’s procedure-oriented programming paradigm.  It was a predecessor of CLOS, the object-oriented programming component of Common Lisp.  
* **NoteCards**: Notecards is an desktop and networked hypertext system developed on Interlisp at PARC starting in the early 1980’s.  This year we continued to update and modernize Notecards in conjunction with updates to TEdit and other aspects of the Interlisp system.  In addition, as an entry to an Internet contest in retro-computing, we developed the first new Notecards type (the Web card) since the 1990’s using the Notecards Programmer’s Interface.  
* **Grammar Writers’ Workbench for Lexical Functional Grammar**: The Grammar Writer’s Workbench was constructed in the 1980s as a comprehensive graphical platform for linguistic and algorithmic research within the LFG theoretical framework (*Lexical Functional Grammar: A formal system for grammatical representation*, Kaplan and Bresnan, 1982). LFG research and teaching can still benefit from the system’s flexible interface for grammar development and testing against phenomena in a wide variety of languages..   
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

[image1]: <data:image/png;base64,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>