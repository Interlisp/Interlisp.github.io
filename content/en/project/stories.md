---
title: Our Stories
weight: 40
type: docs
---

### Blake McBride
_Imagine finding an old car from the 1960s. It's been sitting in storage for decades, doesn't run, and looks like hell. You remember driving the car when you were young and how much fun you had with it. It had a number of features you enjoyed back then that don't exist anymore. You want to re-live the experience and be able to share it with future generations so that they can experience the same thing and learn from the lessons it taught._

_You decide to fix the car up. Make it run well again. Make it look good again. It'll be close to what it once was - a thing of beauty of that time._

_The thing you don't want to do to it is make it modern. You don't want to add air conditioning to it, and you don't want to add anti-lock brakes to it. You don't want to do that for several reasons as follows:_

_a. You lose the whole value of bringing the old experience into the present._

_b. You are trying to make the old car modern. Ultimately, you can't compete with modern cars and all of your "enhancements" are just tack-on garbage._

_I like InterLisp for what it was. It was a thing of beauty in its own right. I'm not looking to create another "modern" development environment out of it. Additionally, there are several top-notch Common Lisp systems available. Making yet another Common Lisp implementation is as utterly a waste of time as I can imagine. To this end, I think emphasizing and enhancing Common Lisp is doing more harm than good. Same for things like new fonts._

_What we should be doing is:_

_1. Make sure it runs really well and is as portable as possible._

_2. Emphasize InterLisp rather than Common Lisp._

_3. Fix bugs and make it run as close to some spec that we chose._

_4. Do not make enhancements that lie outside the spec._

_5. Focus on making it look and run as it originally did._

### John Cowan

_When I went to summer camp in the 1970s, the director owned a 1932 Packard that we sometimes got to take rides in. But we could only do that on the camp property because the car was completely unsafe under any other conditions (for one thing, the starter didn't work: you had to push the car). By now, riding in it at all would probably be either illegal or contrary to the camp's insurance policies._

_This isn't directly on point for Interlisp, but it illustrates why you might need anti-lock brakes even if not air conditioning._

_The Society for Creative Anachronism provides a medieval experience for its members and guests, but without the original filth and consequent disease. The simulation of Interlisp-D isn't going to be perfect._

_I'm not saying that it makes sense for the Medley development environment to support, say, Java programming. But Common Lisp is another matter._

_Common Lisp is \*part\* of Medley (and its predecessors Lyric and Koto). The Interlisp specs have always been a posteriori: they tell you what the existing implementations have in common. That's a good and valuable thing, but Medley is now the leading implementation (in the sense that OpenJVM is the leading Java implementation), and the spec is what Medley does (modulo OS interface bugs, of course. The Common Lisp standard is another matter. It is a priori: if you are writing or maintaining a Common Lisp implementation (at least one new implementation is currently underway) and it doesn't agree with the current (1994) spec, it is buggy and you should fix it. If it were a question of adding Common Lisp support to Medley, I'd say "Forget about it!" But it isn't. It's just bad luck that most of the work was done between the 1984 and the 1994 standards. (No further standards are contemplated, so when it's done, it's done.)_

_At the very least, someone should run the ANSI test suite and see at which points it fails to be conformant. It's known that some Common Lisp bugs and limitations were fixed since the Medley release, but nobody remembers which ones._

_Note that I am not an Interlisp insider and have no axe to grind, except that Larry has said the purpose of this effort is to create a new group of Medley users/maintainers), and I think what will matter to them most is the programming tools. If they can develop on Medley and either deploy on Medley or on SBCL, that will be a big incentive._

### Michele Denber

_Well, I guess I might as well toss in my $0.02. I am not an Interlisp insider, just a user. I came to Lisp at Xerox back in the early 80's. Coming from a Fortran/PL/I/APL/BCPL background, Interlisp-D was a revelation to me. The power of this environment was so amazing I couldn't imagine ever going back to anything else._

_IMNSHO, Interlisp-D needs just three things to be as good a development environment as anything around today: network connectivity, local device access (USB, printers, etc.), and color (just because everything is in color these days). All of these features were available back in the 80's on the D-machines but were lost with the move to X._

_The closest thing I've found to Interlisp-D in terms of quickly coding up some algorithm and getting it running is Matlab. But Interlisp-D as an IDE is far superior to Matlab._

### Ron Kaplan

_I was the one who was most interested in the resurrection, because of my desire to use it as a platform to explore new aspects of linguistic theory (LFG). Many years ago we (namely, John Maxwell in my group at Parc) translated the core algorithms from Interlisp to C, and that provided a high-speed commercial-grade implementation that became the basis for the Powerset spin-out company. But we took a 40-to-1 hit in coding productivity (with maybe a 1-to-40 efficiency gain), and it is virtually impossible for someone other than John to use the C implementation for experimental investigations._

_It was a real break when Nick had the time, about 3 years ago, to figure out what was causing it to crash on the Mac. I have probably been the only “user” for the last 3 years before this community effort got started. During that time I encountered a few bugs in the emulator that Nick was able to track down (I remember a fat/thin string bug, a bigending bug) and at least one that is still lurking (stack corruption with multiple-value returns). But it has been remarkably stable—I have run for weeks if not months in the same sysout without crashing._

_Along the way, I fixed a few other compatibility bugs to make it work better in the Mac environment, and I also did some modernization extensions (interface to the clipboard, moving and reshaping windows by dragging the title bar and corners instead of the silly pop-up menus)._

_Another important modernization that I have worked on and has been discussed is to replace the XCCS character encodings and fonts with Unicode, so that text files at least can move back and forth between Medley and the OS. Especially because the XCCS fonts that we have are so incomplete. And a few other things that make it easy to interoperate with modern interface conventions as they evolved away from our intuitions in the 80s and 90s._

_But none of this would change the core behavior of Interlisp, it would just reduce some of the barriers to entry and make it less confusing to move in and out._

_I am not particularly interested in Common Lisp per se, except insofar as Common Lisp has added a collection of often useful and sometimes elegant new functions that I call from time to time. In terms of capabilities, Common Lisp and Interlisp tend to generalize on different dimensions and so a mix can sometimes be helpful._

_However: the integration of Common Lisp into the Medley development environment is incomplete, and in some ways broken. Key attractive features of the environment simply don’t work on Common Lisp FUNCTIONS and MACROS that are contained in files. I would never actually do a DEFUN or DEFMACRO in my own code, although I certainly do call out to Common Lisp functions. Common Lisp feels basically like a reversion towards a non-residential system. (There are also some inconveniences in the way that BREAK works.)_

_My primary goal then would be to complete the Common Lisp/Medley integration so that the development experience is consistent for FNS and FUNCTIONS etc. Upgrading Common Lisp to this or that standard might also be an attractor (or less of a disincentive) for others to come into this particular implementation, but I would first want to ensure a consistent Medley development environment._

### Larry Masinter

_For me, the importance of Medley is as a development environment. People who used it (including myself) were much more productive. It spoiled me so much I've never been proficient in anything else._

_I didn't think people could get the sense of the development without a lengthy session, to use it "in anger" -- trying to get something else to work while using medley as a tool._

_I think showcasing "things people built in Interlisp" shows the power of the development style, especially for research prototypes._

_I think with a volunteer effort like this, it is to be expected that people have different things they want to get out of it, and the project goals are necessarily a synthesis of the individual goals. We have common subgoals. I don't think there are any serious conflicts except perhaps priorities._

_Getting the system stable is very important._

_Getting the envos tests to run is a subgoal_

_There is too much to do with available manpower, so getting people to join is necessary. The first hurdle of contributing is understanding how to get started_

### Paul McJones

_I’ve had the feeling that I don’t understand “the big picture”, and how the discussions fit in. For example, support for the Unicode character set and for modern scalable fonts would make it nicer to do work like Ron’s computational linguistics in Interlisp, but don’t seem too necessary to support people using Interlisp to understand its programming environment. Similarly, getting Interlisp to interoperate with git repositories seems like a distraction for someone who is trying to understand how Interlisp’s programming environment worked back in the 1970s and 1980s._

_Here is my attempt to think about a “stripped down” path to preserving Interlisp history in a fashion allowing it to be used and studied:_

_1. Create one or more snapshot releases of Interlisp (a suitable virtual machine, a file system with sysouts, sources, and compiled files, and a matching set of documents (reference manual plus getting started guide) that will run on one or more modern platforms and that are complete enough to use the standard Interlisp tools to edit, compile, debug, and run an application. The snapshots would be distributed as compressed tar files and could be downloaded and run without any use of git or GitHub. If one of these could be adapted to run in a web browser, it might become the dominant way for “outsiders” to sample Interlisp._

_2. Create a series of source snapshots corresponding to various interesting points in the Interlisp timeline for which complete or partial sources are available, for example:_

_Parc/BBN PDP-10_

_Parc D machines_

_Envos (D machines?)_

_Venue (Solaris)_

_Each snapshot would be a compressed tar file, and, where available, would include multiple versions of various source files, as maintained in the traditional Interlisp development environment. These snapshots would be archived (for example at CHM, and possibly software heritage.org). They would also be the starting point for creating the executable snapshot releases of #1._

_3. The one component of Interlisp that seems compatible with git file-based development is the maiko virtual machine, although pragmatically I think the main activity would just be fixing show-stopper bugs and adapting it to new platforms._

_But for the Lisp source files, it seems that informal mechanisms used in the 1980s to coordinate within a small group of developers are still the best way._

### Nick Briggs

_I’m mostly interested in getting the underlying emulator code working reliably. Unfortunately, there is little-to-no documentation available for the (C language) code itself, or description of the technical design and implementation details behind it. This makes it critically important to me to have the code history preserved, in its entirety, so that when I find something that appears to be a problem I can look at all the revisions that have been made to determine if there was an error introduced recently, or exposed by, for example, operating system or compiler changes, or is an endian dependency that was never resolved (for which we need to have both the original big-endian and newer little-endian versions). Since there is very tight integration with the lowest levels of the Lisp sources, I’m also interested in ensuring that we keep the history of the Lisp code available too -- preferably in a way that permits easy comparisons of previous versions, and such that we can track the source in a running sysout back to the Lisp source files that we are keeping._

### Arun Welch

_I started working part-time for XAIS when I complained to John that the TCP/IP code was broken and he responded with “yeah, but all the AR’s reporting problems are coming from you and all the patches to fix those AR’s come from you so why don’t I pay you to support it since I don’t have any resources available to do that anyway”..._

_From there I supported the networking code, maintained the PCL port, and assorted other applications layered on top of the basic system as the ownership transitioned from XAIS to Venue to Envos._

_I’m interested in getting some of the applications that were built on Interlisp/Medley working in the current environment, including:_

1. _ROOMS_
2. _NoteCards_
3. _PCL/CLOS_

### Bob Bane

_I would like to resurrect and extend the Common Lisp development part of Medley Making Common Lisp a fully supported part of Medley was an amazing achievement back in the day; I did a bunch of work in that environment and really liked the combination of Common Lisp and managed source files._

### William Maddox

_I saw the recording of your demo at the NYC Lisp group…. I figured I'd download it and give it a whirl over the weekend. I'm interested in seeing what a residential Smalltalk-80-like Lisp system feels like. I've used Allegro CL and various file-oriented Lisp and Scheme implementations over the years, but Interlisp-D was a bit different. I also have a "thing" for self-contained systems that can run on bare metal. I think Wirth's FPGA Oberon is really, really cool, but it's really a bit of an educational toy, and the language is a dead-end. A real Lisp system would be so much neater. My interest, if I got involved with any development, would be getting a bare-metal port of maiko running. Recently, a fellow combined a bare-metal support library with an ST80 virtual machine in C (both pre-existing open-source) and got an ST80 image running on bare-metal Raspberry Pi -- no Linux in sight. In reality, though, a stripped-down embedded Linux would do the same thing, more or less. I really think to experience a Lisp machine, however, it needs to boot directly into Lisp. Running any sort of emulator "in a box" on a modern desktop, with a web browser, Facebook, and all those other distractions is just cheating. ;)_

### Stephen Kaisler

Back in the 1980s, I had written a book on Interlisp: The Language and Its Usage, which was published by John Wiley & Sons. The book has been out of print for years.

One of Xerox Electrical Optical Systems salespersons had told me they had purchased some copies to give to customers of their early D machines.

I had used Interlisp in several variations: Interlisp/360 (an implementation from Israel), Interlisp-D on a Xerox 1100 that I had at CIA, Interlisp-D on a Xerox 1186 that I had as a DARPA Program Manager, and Interlisp-VAX.

I began a subsequent volume entitled Interlisp-D: The Interactive Programming Environment, which had the same structure, format, and approach as the first book. It was submitted to John Wiley & Sons, who had initially agreed to publish, but then demurred after Xerox apparently stopped selling D-machines and Common Lisp came to the fore. The volume currently has 13 chapters and about 500 pages with numerous examples that I had tested on both my Xerox 1186 and on Interlisp VAX (the ISI version). It was written using Microsoft Word.

So, it languished for many years as I had hoped to see Interlisp-D be revived. Now, it appears that is the case with the Medley Interlisp project.

I am interested in participating in the project, re-editing the book with its examples, adding to it as appropriate, and adding it as another source of documentation to the Interlisp-D revival.

I wonder if you are also going to include LOOPS as part of this revision. I took the LOOPS course at PARC in 1983 with Peter Fisher of XEOS as my partner.

I am looking at the possibility of converting the first volume from PDF to Word so it can be further edited. Not sure if this is possible depending on how the PDF was created. If I can do this, I may split that volume into IA and IB to make it more manageable.

As I got more into editing the second volume, I realized it was going to be very big. So, I have split it into Volumes II and III:

* Volume II: The Interactive Programming environment
* Volume III: Tools and utilities like TEdit, DEdi, etc.

Once I start working on LOOPS, it may become a fourth volume. Others may arise as we get further into the project, but that is a ways off.

### Guenther Goerz

I got familiar with Interlisp when I was working on an implementation of a parser for my PhD thesis work in the late 1970 and 1980s. It started with a little cooperation with Martin Kay (and also Ron Kaplan) from PARC at a computational linguistics summer school in Pisa. Although I had a tenured researcher position at my university, I did not have any means to acquire one of Xerox' LISP workstations, which were sold in Germany by Siemens for something like 90000 Euros (today's equivalent) - so I used Interlisp on a Siemens mainframe to which I had access. The Interlisp version was a descendant from the IBM implementation - both machines had basically the same hardware architecture but different operating systems (which was not a problem for the rather self-contained Interlisp environment). After spending some time with IBM's LILIOG project at IBM in Stuttgart and getting my first professorship at the University of Hamburg, I came back to Erlangen in 1991. So, in the 1990s I used the Fuji Xerox emulation of Medley on Sun workstations and later on Linux machines. Additionally, we also acquired a license for the DOS version of Medley 2.0 from envos/Venue. What I used for some time was the LFG implementation in Medley - which I got from Ron Kaplan in Linux - in Suse Linux, running on my Mac(s) with the Parallels Virtual machine, mainly for teaching purposes. But I was also interested in various features of the programming environment... Recently, just for fun, I tried to get Medley up and running under DOSbox on Mac OS X. I was also wondering whether there is a DOS emulator for the ipad - and there is one, iDOS, which works pretty well! So, despite the small screen, Medley 2.0 runs amazingly well on the ipad too.

I must add that we (our chair at FAU Computer Science) first acquired a Medley 2.0 license for the Sun workstations through Xerox France first and the DOS license later. We used it for our first steps in the Behaim Globe project (also trying out NoteCards and implementing our first ontology with CLOS) and the actual portal https://wisski.cs.fau.de/behaim has still some of the code deep inside and furthermore for NLP, in particular, the LFG grammar development environment. Since I was a simple user, my expertise is pretty small; I was never involved in anything close to system development. Later on, I switched to Scheme for teaching and research for reasons of clarity and simplicity and also for theoretical reasons - I never liked Common LISP very much. But of course, there was never such a comfortable programming environment for Scheme.

After my retirement in 2012, I focused on the development of our VRE Wisski in cooperation with two museums (https://wiss-ki.eu), which turned out to be quite successful - in the meantime, there are several hundred applications. Furthermore, I helped to get Digital Humanities at our university up and running - they are starting a new department quite now - and I was involved in some DH projects at the Max Planck Institute for the History of Science in Berlin and more recently at the Bibliotheca Hertziana (Max Planck Institute for Art History) in Rome in the field of "cosmography" (which was the correct term in the Renaissance), i.e. modelling and annotating historical texts and maps (https://wisski.biblhertz.it).

A while ago I tried - just for curiosity - whether the old DOS version of Medley 2.0 would also run in the DOSBox under Mac OS X. It worked really well, and so I became even more curious whether there would be something like DOSbox for iOS - and yes, there is iDOS, basically designed to run old computer games. Now Medley 2 runs on my ipad... Actually, I don't have any further plans, and I didn't realize what happened after Medley 2.0. So, from your presentation at lispNYC I learned that there seems to be something like a new version 3.0. Sounds tempting... So, I would be glad if we could keep our contact active.

### J Moore

  I checked out interlisp.org.  That's an interesting project.  I am glad you're doing it.  Too often the first implementations of good ideas are overshadowed by evolutionary improvements.  (In that spirit, a few years ago I reimplemented the first Boyer-Moore theorem prover -- the one we built in Edinburgh in POP-2.  But I implemented it in ACL2, i.e., applicative Common Lisp.  But it proves the same theorems the same way as we did in 1972-3.)

As for the VM, I don't have much context to add beyond what I wrote in the Acknowledgements of CSL-76-5, which I'm sure you've read if you're interested in that question.  I got my PhD from Edinburgh in November, 1973, and arrived at PARC in January, 1974.  Danny Bobrow had taken a sabbatical from PARC (BBN?) in '73 and spent it in Edinburgh, where he convinced me to join PARC.  The Acknowledgements says Warren Teitelman asked me to write the VM document in January, 1975.  But I actually suspect it was earlier than that, perhaps as early as January, 1974 (i.e., I got the year wrong!).  The reason is that the Acknowledgement says we spent 2 years writing it, but CSL-76-5 came out in September, 1976, so I suspect Warren approached me in the
a few months after I joined PARC.  For the record, I don't remember doing anything at PARC besides (a) re-coding the Edinburgh theorem prover in Interlisp as a warm up exercise and to continue my research on theorem proving, (b) helping Simonyi with the representation of text in Bravo by implementing the underlying data structures in Interlisp and responding to Charles' requests for new features, (c) writing the VM, (d) inventing the fast string searching algorithm with Boyer and fighting the lawyers at Xerox to publish it (ultimately by threatening to remove my name from the publication and let Boyer author it), and (e) fighting with Ben Wegbreit and Jerry Elkind over the ``right'' way to approach verification and ultimately leaving.  So I suspect that my VM work was my first and main official task at PARC.

Other than that, I think the Acknowledgements say it all, accurately.  The line there that says I think my friends in the formal verification community will be displeased was not speculation.  Tony Hoare wrote me a letter upon seeing the document in which he complimented me on the precision and urged me to get back to formal methods.  Oh well.
