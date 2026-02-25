---
title:  Interlisp Timeline
type: docs
weight: 50
aliases:
 - /medley/history/timeline/
---

This timeline started with Teitelman’s [History of Interlisp](/documentation/History_of_Interlisp.pdf). The [Bibliography](/bibliography/) has a wealth of additional historical information. 

## 1960s

Through the 1960s, the languages of programming were primarily Fortran and assembly. Lisp enabled expressing recursion simply. Lisp also provided the ability to modify a program as it was running, since Lisp programs were themselves data—the same as other list structures used to represent program data. This made Lisp an ideal language for writing programs that themselves constructed programs or proved things about programs. As an area of Artificial Intelligence, programs writing programs was something of great interest to those working on applying AI to programming.  

Lisp was at that time just a language. Programming in Lisp consisted of submitting a job, usually as a deck of punched cards to run in batch mode on a mainframe. You could then pick up your output a few hours later, if lucky, otherwise the next day, and hope that it did not consist of a lengthy sequence of left parentheses or NILs, as would be the case if the program had certain kinds of bugs.
1964  

L. Peter Deutsch (high school student) developed PDP-1 Lisp at MIT.  

- L. Peter Deutsch, quoted in [lisp_doc.txt](/documentation/lisp_doc.txt) accompanying Bob Supnik's Software Kit
- L. Peter Deutsch and Edmund C. Berkeley. The LISP Implementation for the PDP-1 Computer. March 1964, pages 326-375 in Berkeley and Bobrow. [PDF](https://www.softwarepreservation.org/projects/LISP/book/III_LispBook_Apr66.pdf#page=336): Describes Basic PDP-1 LISP in detail, including full PDP-1 assembly language source code.

The introduction of time-sharing in the mid-60s changed the paradigm of software development. Instead of the developer doing their debugging offline, users could now interact directly with their program online. Time-sharing was originally developed as a way of making more efficient and economic use of a very expensive computer, but it also had the surprising side-effect of drastically reducing the amount of time it took to get a program working. Users experiencing this phenomenon reported that it was because they did not have to lose and then reestablish context so frequently, but could get very deep into their programs and the problems they presented, and stay there. The situation is analogous to trying to resolve an issue between two people via a conversation rather than sending letters back and forth. Regardless of how short the cycle of iteration is, e.g., if email is used instead of letters, if the process involves discovery and a lot of back-and-forth, it is much easier to do via a conversation. You could establish a context and stay focused until the problem was solved.

### 1965

Teitelman’s experience with his Ph.D. work led him to the notion of building a system where the computer took an active role in helping make changes to a program. At the time, this was a very novel idea.  

The term “programming environment” was meant to suggest not only the usual specifics of both a programming system and language but also more elusive and subjective considerations such as ease of use and level of interaction, “forgiveness” of errors, human engineering, and system “initiative.” The programmer’s environment influences and to a large extent determines, what sort of problems they can (and will want to) tackle, how far they can go, and how fast. If the environment is “cooperative” and “helpful”, then the programmer can be more ambitious and productive. If not, they will spend most of their time and energy “fighting” the system, which at times seems bent on frustrating one’s best efforts.  

In 1965, there were very few tools for developing Lisp programs, and those that were available were very primitive.

### 1966

- MIT EE Dept PDP-36 [LISP manual](http://bitsavers.org/pdf/mit/rle_pdp1/memos/pdp36_lisp_may66.pdf)

Teitelman started at Bolt, Beranek and Newman in Cambridge. At the time, BBN’s computer was a DEC PDP-1, and Daniel Murphy had written a version of Lisp 1.5 for it using ideas from Deutch’s work. This Lisp was really just a toy – single user, slow, small address space, but Teitelman started with Break and Prettyprint from MIT on his pursuit of a Lisp programming environment.  

- http://www.softwarepreservation.org/projects/LISP/bbnlisp/BBN-LISP-System_Feb1966.pdf#page=49 

### 1967

In 1967, BBN purchased an SDS 940 computer from Scientific Data Systems and began work building a time-sharing system on it. The SDS 940 had a larger address space and the ability to support a paging system. BBN was awarded an ARPA contract to provide a LISP system that could be distributed to other ARPA sites for doing A.I. research. (ARPA = Advanced Research Projects Administration of the Department of Defense.)  

- [Improvements to the 940 LISP Library](http://www.bitsavers.org/pdf/sds/9xx/940/ucbProjectGenie/940_LISP_Memo_2_Apr67.pdf)  

Advising was a means of allowing the user to treat a particular function as a black box without knowing what was inside the box, wrap “advice” around it that could operate before the function ran, potentially changing its input parameters, after it ran, possibly changing its value, or { PrettyPrint which printed out a nicely formatted representation of Lisp programs, using indentation to indicate depth of structure. A Trace facility was also available which modified specified functions to print on the terminal their input parameters on entry and their value on exit. You could think of this as a special case of Advising. There was also a Break package which enabled the user to cause program execution to halt at the entry point to specific functions. The user could then examine the value of the function’s input parameters, and even change them, then cause the function to run, and again gain control so as to examine the value that the function returned or side effects of the function’s operation. The user could change input parameters and re-execute the function, or manually specify the desired value and have it be returned to the caller as though it had been the value produced by that function.  

Teitelman memo to [SDS 940 LISP Users](http://www.bitsavers.org/pdf/sds/9xx/940/ucbProjectGenie/940_LISP_Memo_2_Apr67.pdf).

### 1968

Work on Demand Paging software virtual memory was focused on supporting Lisp.  

Peter Deutsch wrote a **structure editor** in Lisp for editing Lisp programs. Prior to this, Lisp source was prepared and edited offline in textual form and read into the Lisp system. Peter’s editor enabled the user to edit Lisp programs without ever leaving Lisp. The editor provided operations for moving up, down, left or right in the list structure definition of a Lisp function, and to make insertions, deletions, or replacements, e.g. (-3 X) to insert X in front of the 3rd item in the current list, 2 to descend into the second item in the current list, 0 to ascend one level, etc. Other more sophisticated commands were soon added, such as a find command to search through all levels of the function being edited looking for a specified string or pattern, a mark command to mark, i.e. save, the current location, and a command to restore the context to one that had previously been marked, an ability to define macros, etc.  

The ability to edit a Lisp program in situ meant that a user could modify a running program and continue execution. For example, the user might be at a Break, evaluate the current function, identify a problem, edit the definition using the structure editor, and reevaluate the current, now modified function and go on.

### 1969

Alice K. Hartley took over Dan Murphy’s role in BBN-LISP. A number of new data types were added to augment lists and numbers: arrays, strings, large numbers, floating-point numbers.

## 1970s

### 1970

As Lisp users began to write larger and larger programs, performance began to be an issue. A compiler had been available for Lisp programs since the early sixties.  

In 1970, Danny Bobrow and Alice Hartley designed and implemented the “spaghetti stack”. This enabled running programs to search the current execution stack, e.g., find the second occurrence up the stack of the function FOO, and return the name of the function that called FOO, to alter the normal flow of control, e.g., return from a specified stack pointer a specified value (very useful when debugging programs in order to manually bypass a known problem), and to evaluate an expression or variable in a specified context, e.g., what is the value of x as of six function calls back up the stack.  

**DWIM**, the most well known, and in some cases reviled, feature of BBN-LISP was introduced in 1970. DWIM stands for Do-What-I-Mean and embodies Teitelman’s view that people's time was more valuable/expensive than computer time. (This was a radical idea at the time.) When Teitelman first started programming in FORTRAN in 1960, he was appalled at receiving the error message, “on line 70, DIMENSION is misspelled”. If the FORTRAN compiler knew this to be the case, why didn’t it accept this and go on and compile his program?  

The BBN-LISP interpreter was modified so that rather than signal an error when an undefined function or unset variable was encountered, DWIM would use various heuristics to identify and attempt to correct the error. Spelling correction was the most common scenario. An algorithm was implemented that took advantage of the most common types of errors made by a touch typist, e.g., doubled characters, transpositions, case error, etc.  

A spelling list appropriate for the context of the error was searched, and a metric computed for each item on the list that measured the difference between that item and the unknown word. If the match was sufficiently close, e.g., the only difference being a doubled character or a transposition, the correction was performed without the user having to approve. Otherwise, the user was offered the closest match and asked to approve the correction.  

If the user approved or the correction was automatically done, a message was printed on the terminal and computation would continue as though the error had not occurred. If the user was not at the terminal, after an appropriate interval, DWIM would default to Yes or No depending on how close the match was. It was not uncommon for a user to perform some editing, then start a computation, go get some coffee, and come back to find the computation complete with several corrections having been made.  

DWIM could also handle the case where the user typed a number instead of ‘(‘ or ‘)’ because of failure to hit the shift key, e.g. 8COND instead of COND. This kind of error was particularly difficult to fix, because not only did it cause a misspelled function or variable, but totally altered the structure of the expression being evaluated. For the user to manually fix such an error using the structure editor required not only removing the 8 or 9, but rearranging the list structure. Having DWIM handle such errors was quite helpful.  

Spelling correction was also used in contexts besides evaluating Lisp expressions. For example, there was a spelling list of edit commands that was used to correct a mistyped editor command. When loading a file where the file name was not found, a spelling list of previously encountered file names would be used.  

Another innovation introduced to BBN-LISP in 1970 was the History package. The idea was rather than simply performing the operations requested by the user, call functions, edit expressions, perform break commands, etc., and discarding that information, to have an agent that would record what the user entered so that the user could examine the history, and replay portions of it, possibly with substitutions. (The history feature of the UNIX C-shell introduced in the late 70’s was patterned after the Interlisp history package.) The history also contained any messages displayed to the user during the execution of the corresponding event, e.g., any DWIM corrections, or messages about global variables being reset or functions being redefined, etc.  As with DWIM, the History package grew out of the desire to offload manual tasks to the computer.  

Perhaps the most important piece of information stored in each history event was the information required to UNDO that operation. This was especially valuable in the context of editing. UNDO is functionality that every user now expects in an editor, but it was first introduced in BBN-LISP in 1970. The UNDO functionality provided in BBN-LISP still surpasses that available in today’s editors in that the user could UNDO operations out of order. For example, after performing a series of four or five editing operations, the user could realize that the information deleted in the first operation is needed, and would be able to UNDO just that operation by explicitly referring to that operation using the history package, without affecting the intervening operations.  

In addition to being able to UNDO edit operations, the user could also UNDO operations that were typed in at the top level or in a Break. This was most frequently used to undo assignments. It could also be used to undo an entire edit session, rather than undoing one command at a time, sort of a revert operation for S-expressions. The user could also arrange to have functions that they defined to be undoable by storing information on the history list.

### 1971

The **File Package** was added in 1971. This was essentially a “make” for Lisp. The user could specify the set of functions, global variables, property lists, etc., to be contained in a specified file, and then “make” that file. When the file was loaded in a subsequent session, this information would be recorded and available. Whenever a component known to be in a specified file was modified, the system would know that the corresponding file needed to be rewritten. A cleanup function was provided that would write out all files that contained components that had been changed. The user would be informed about any items created or modified during the course of their session that did not appear in any of the user’s files, and therefore might be lost if the user abandoned their session without saving them somewhere. The only thing missing from the File Package that would be provided in UNIX Make was the notion of dependencies.

### 1972

In 1972, Danny Bobrow and Warren Teitelman left BBN and went to the newly formed Xerox Palo Alto Research Center – PARC. BBN continued to provide the low-level support for the Lisp system, i.e., compiler, garbage collector, and all of the operating system interface, while the Lisp-based center of activity for the various packages and utilities moved to PARC. Both sites continued to be supported by ARPA, and to indicate this partnership and shared responsibility, BBN-LISP was renamed to be **Interlisp**.  

Around the ARPAnet, Interlisp continued to use the DEC PDP-10 as its principal platform.

### 1973

- "[Interlisp Reference Manual, Acknowledgements and Background](http://bitsavers.trailing-edge.com/pdf/xerox/interlisp/Interlisp_Reference_Manual_1974.pdf)" (PDF). 1973.

### 1974

By 1974 a number of impressive extensions to Interlisp had been developed by Larry Masinter. These included a much more sophisticated version of Interlisp’s **iterative statement**, as well as a **Record** package that enabled a user to label various components of a list structure and refer to them by name, thereby eliminating the CADADRs and CDADDRs that made Lisp programs so difficult to read. The Record package also had the advantage that the user could change a record definition, and the program would automatically adopt the new structure. For example, if PERSON were defined as (RECORD PERSON (FIRSTNAME LASTNAME TITLE)), the expression (X:TITLE) would translate to (CADDR X). If the user later changed the definition of PERSON to (RECORD PERSON (FIRSTNAME INITIAL LASTNAME TITLE)), all expressions involving TITLE would automatically be retranslated to use CADDDR.  

- [Interlisp-10 sources from 1974](https://github.com/Interlisp/history/tree/master/1970s/1974-sources)

**Masterscope** would analyze a large program and build a database of relationships between the various components that could then be queried using a natural language front end. For example, WHO CALLS FOO AND USES MUMBLE, EDIT WHERE X IS USED FREELY AND Y IS BOUND, etc. As LISP programs became larger and more complex and were being built by teams of programmers, rather than a single programmer, functionality such as that provided by Masterscope was invaluable in understanding, maintaining, and extending programs.

### 1975

{{< imgproc IM_Cover Resize "128x166" >}} {{< /imgproc >}}

By 1975, Interlisp had become so rich in functionality that it was clear that word of mouth was no longer sufficient and in depth documentation was needed, especially since there was a large and growing community of users at the various ARPA sites that had little or no direct contact with the developers of Interlisp at PARC and BBN. Work on the first **Interlisp manual**, which turned out to be a year long project. When completed, the manual was over 500 pages and heavily indexed. It was written using PUB, a text formatting program developed at Stanford by Dan Swinehart and Larry Tesler. (This was back in the days when the only WYSIWYG editor was PARC’s Bravo which ran only on the Alto.)  

The fact that the manual was machine readable, and heavily indexed, meant Interlisp could use it to provide online help and documentation. The user could type in something like TELL ME ABOUT FILE PACKAGE and see on the terminal/screen the relevant text. In a break, the user could simply type ‘?’ and see an explanation of the input parameters for the current function.

### 1976

In 1976, Dan Ingalls gave a presentation at PARC in which he demonstrated the first window system. Written in and for Smalltalk, the user interface and paradigm it provided for enabling the user to manage and work with multiple contexts was very compelling, and immediately inspired work to provide such a mechanism for Interlisp. At the time, although Peter Deutsch had developed a byte-coded instruction set for the Alto, it was under-powered for Lisp development.  

Bob Sproull came up with the idea for what would turn out to be the first client-server window system: use the Alto as the window server and Interlisp running on the time-shared PDP-10 clone as the client. and develop a protocol for having Interlisp tell the Alto what to display, and for the Alto to tell Interlisp about mouse clicks. Bob developed the **ADIS** (for Alto Display) package and Teitelman wrote **DLISP** in Interlisp. DLISP included a window manager and windowing system that enabled overlapping windows, cut and paste, etc. J Moore implemented a text package that would support display and editing of text in windows. Teitelman demonstrated this functionality at IJCAI in 1977, and presented a paper, a Display Oriented Programmer’s Assistant.

### 1979

In 1979, PARC began the design of the Dorado, a high performance personal workstation. The availability of the Dorado also made possible building a Lisp with a native display capability, which led to the Interlisp-D project.

## 1980s

- Teitelman & Masinter, IEEE Computer, “[The Interlisp Programming Environment](https://larrymasinter.net/interlisp-ieee.pdf)” April 1981.
- [1983 Stanford University Medical Experiment Computer](https://github.com/Interlisp/history/tree/master/1980s/1983-sumex-lisp)

### 1982

- AAAI launch of 1108 (Dandelion) and 1132 (Dorado)

{{< image-gallery gallery_dir="photos/AAAI82" >}}

### 1983

- Chorus and Fugue Releases of Interlisp-D

### 1984

- Carol Release?

### 1985

- Harmony and Intermezzo releases
- Koto release (for Xerox 1186), some bits of Common Lisp

### 1987

- Lyric release

### 1988

- Medley 1.0 release. Medley supported all Sun's running on SunOS, plus IRIX, AIX, HPUX, Ultrix, (i.e., BSD Unix)

### 1989

- Envos formed from XAIS
- April 10, Envos closes

## 1990s

### 1991

- August: Venue moves to new offices [Arun Welch email]
- 3-byte atoms

### 1992

- Medley 2.0 with CLOS, MOP, for Dos 4.0 and Xerox 1186
- ACM Software Systems award was given to the Interlisp team: “For their pioneering work in programming environments that integrated source-language debuggers, fully compatible integrated interpreter/compiler, automatic change management, structure-based editing, logging facilities, interactive graphics, and analysis/profiling tools in the Interlisp system.”

### 1993

## 2000s

The ADVISE/advice idea and names carried through to the Aspect/J system, and on into contemporary, mainstream Java frameworks.

- e.g. Spring: [Chapter 6. Aspect Oriented Programming with Spring](https://docs.spring.io/spring-framework/docs/2.5.5/reference/aop.html)

### 2009

[John Sybalsky obituary](https://www.legacy.com/us/obituaries/mercurynews/name/john-sybalsky-obituary?id=22720418)

### 2010

[Web Archive of Medley](https://web.archive.org/web/20100304002925/http://top2bottom.net:80/medley.html)

**MEDLEY**  
Medley provides a rich software development environment, including a debugger, a list structure editor, a file package, a compiler, text-editing facilities, and other useful tools. With any interactive computer language, the user interacts with the system through an "executive," which interprets and executes commands. Medley includes three such executives: Common Lisp, Xerox Common Lisp, and Interlisp. Medley is a programming system, containing not only a programming language but also many predefined programs and specialized programming tools.  

Medley's interactive window-based *debugger* automatically appears when an error occurs. You can enter the debugger through a program execution error, a user-entered keyboard interrupt, or a programmer-specified break. When execution is halted for one of these reasons, the user can reset the system and unwind the stack, or enter the debugger. The break window is an executive window; you can perform any activity here that you can in other executive windows, including looking at the program's current state, changing data structures, evaluating expressions changing a function, and calling the editor. These break facilities, familiar to Interlisp users, are now in the common Lisp executive as well.  

The *programmer's assistant*. This tracks the user's actions during a session, allowing them to be replayed, undone, or altered. The most common interaction with the programmer's assistant occurs at the top level read-evaluate-print loop or in a break, where the user types in expressions for evaluation and sees the value printed out.  

The *file package and compiler*. The file browser provides a convenient user interface for manipulating files stored on a workstation or file server. The makefile option in the file package lets you compile an entire file. You can compile individual functions using the compile command for functions in memory, the Tcompl command for definitions stored in files, or the Recompile command for a combination of in-memory and file definitions. Medley also supports block compiling. The Spy tool lets you identify program bottlenecks.
Structure and text editors. Medley offers a choice of structure (list) editors. Dedit and Sedit. When loaded, the Dedit library utility becomes the default structure editor. Sedit does not have the type-in buffer of Dedit; it automatically places Lisp structures that the user fills in by selecting a character or a structure. Sedit recognizes Lisp functions such as single quotes, back quotes, and commas. It automatically adds spaces to maintain legal structures. Medleys Tedit supports multiple fonts, embedded graphics, and document formatting. Figures created with the drawing program, Sketch, can also take screen snapshots.  

**NOTECARDS**  
Notecards tool collects, organizes, and presents hypermedia information. Many cards can be displayed at once, and each can contain text, sketches, or scanned graphics. Cards are connected by typed links and stored in "file boxes."  

**LOOPS**  
**L**isp **O**bject-**O**riented **P**rogramming **S**ystem  

Objects give you a lot of power, but they're not the whole answer. Sometimes, other ways of looking at a problem will work better. At times, plain procedural programming is best. Other times, you'll want to trigger actions in response to changes in variables' values. Yet other times, you'll want to use rules to capture domain specific knowledge. LOOPS gives you all of these in one coherent package. LOOPS also gives you development tools that really help you while you work. You'll want to keep track of the classes and objects you've created. LOOPS' browsers let you do that. You'll want to watch your rules in operation to find out where they're going awry. LOOPS' rule auditing facility lets you do that.  

Big systems often have many objects that start out the same, and slowly diverge as the system runs. Normally, you'd have to start off with completely separate objects, at a tremendous cost in memory. LOOPS lets you start with only a single real object. All the others are tiny "virtual copies" of that one. Each copy grows only as you change the values of its instance variables. The effect is the same as having many independent objects, without the memory cost.  

The classes and objects you create are the same blocks LOOPS is built out of. So the classes you create can be combined with LOOPS itself to extend its power. You wind up with a system that speaks your language and has tools to fit your needs-and your specialized tools have become part of LOOPS, so its power is brought to bear to solve your problem.  

> "Medley is and has been a system before its time. Through the debuggers, the graphics and window systems, and the organized structure of the underlying Lisp systems, Medley provides a marvelous tool that creates enthusiasm and motivation for programmers, applications builders, application users, teachers, and students alike."  
> Patrick Goddi and Anne M. Keuneke

### 2019

[Jill Marci Sybalsky obituary](https://www.dignitymemorial.com/obituaries/san-jose-ca/jill-sybalsky-8186140)

### 2020

[Medley Interlisp project](https://interlisp.org/) begins
