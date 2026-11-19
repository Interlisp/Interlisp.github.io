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

<span id="advising" data-tooltip="A way of modifying a function's behavior by wrapping it with code that runs before or after the function and can inspect or change its arguments or return value."></span>Advice (Advising)
: Advice (advising) is a way of modifying a function's behavior without editing its definition. The advice is code wrapped around the original function: it can run before or after the function body, or at a specified position in an existing advice list, and it can inspect or change the function's arguments, examine or replace its return value, or bypass the original definition entirely. Because the original definition is preserved, advice can be added and removed independently. Teitelman’s [*PILOT: A Step Toward Man-Computer Symbiosis*](/history/bibliography/rqwu8zw9/) (1966) describes advising in detail, presenting it as giving the system advice about how to modify its programs.

  In Interlisp, `ADVISE` can apply the same advice to one function or several, can restrict advice to calls made from a particular function, and works on compiled as well as interpreted functions. Each function's advice is recorded on its property list, so it can be edited, removed with `UNADVISE`, and restored with `READVISE`. Trace and the Break package are examples of this technique. For the introduction of advising in BBN-LISP, see the [1967 Timeline entry](/history/timeline/#1967).

<span id="altolisp"></span>AltoLisp
: An experimental microcoded implementation of Interlisp on an Alto personal computer.

<span id="briefing-blurb"></span>Briefing Blurb
: One of the several documents that introduced Xerox PARC newcomers to the computing and network environment of the Computer Science Laboratory. Written in an upbeat style, their titles followed a pattern that included the expression "Briefing Blurb" such as *The Alto-Dolphin-Dorado Briefing Blurb: Exploring the Ethernet with Mouse and Keyboard* and *The Briefing Blurb: Exploring the Ethernet with Mouse and Keyboard*.

<span id="named-releases"></span>Carol, Fugue, Harmony, Intermezzo, Koto, Lyric, Medley
: Named releases of Interlisp-D.  All are obsolete except Medley.

<span id="common-lisp"></span>Common Lisp
: The subject of a 10-year standards process to converge multiple dialects of the
Lisp language. Strong influences from many Lisp dialects, including Interlisp.

<span id="common-lisp-the-language"></span>Common Lisp the Language
: Book by Guy Steele with two editions:

- CLtL1 – edition 1, 465 pages
- CLtL2  – second edition, 1029 pages

<span id="dlisp"></span>DLISP
: By Warren Teitelman: a first attempt at building a “Display” (GUI) with Interlisp running on MAXC (a PDP-10 clone) connected by Ethernet to a Xerox Alto acting 
as a graphics terminal.

<span id="dorado-lisp"></span>Dorado Lisp
: The reimplementation of the AltoLisp microcode on the Dorado – a research prototype.

<span id="dwim" data-tooltip="An automatic error-correction facility that intercepts undefined functions, unset variables, and misspellings and uses context to suggest or apply corrections."></span>DWIM
: DWIM (Do-What-I-Mean) is Interlisp's automatic error-correction facility. When evaluation encounters an undefined function or an unbound variable, DWIM uses the context and a spelling list appropriate to that context to find a likely correction, such as a misspelling, a doubled character, a transposition, or a wrong-case letter. If the match is close enough, it makes the correction and continues; otherwise it reports the closest match and asks the user to approve it. The DWIM facility and its spelling correction are described in detail in Teitelman, [“Automated Programmering: The Programmer’s Assistant”](/history/bibliography/qwkix8dw/) (1972).

  DWIM operates in cautious or trusting mode. In cautious mode it asks before making corrections that would modify a user's function, while trusting mode proceeds automatically; if the user does not answer within a set interval, DWIM applies a default. It can also repair some structural errors, such as an 8 or 9 typed in place of a left or right parenthesis, where correcting the spelling alone would not restore the expression's structure. When DWIM cannot correct an error, normal error handling resumes with a break or unwind. For DWIM's introduction to BBN-LISP, see the [1970 Timeline entry](/history/timeline/#1970).

<span id="history-package" data-tooltip="The part of the Programmer's Assistant that records a session as a list of events, each storing the input, value, side effects, messages, and errors for later inspection."></span>History package
: The History package is the part of the Interlisp Programmer’s Assistant that records a session as a list of events. Each event stores the user's input, its value, side effects, messages, and errors, so the record can be inspected after the fact rather than discarded as soon as a command finishes. The list is a ring buffer: older events are forgotten as new ones arrive, and a NAME/RETRIEVE facility can preserve selected events. The history list and its use in the Programmer’s Assistant are described in Teitelman, [“Automated Programmering: The Programmer’s Assistant”](/history/bibliography/qwkix8dw/) (1972), and [“A Display Oriented Programmer’s Assistant”](/history/bibliography/3h5f6tba/) (1977).

  Using the history list, a user can refer to an earlier event by number, relative position, or a description of its input, then replay it, replay it with substitutions, or undo it. The History package is therefore the basis for the Programmer’s Assistant commands `REDO`, `USE`, and `UNDO`; the editor keeps its own history list for edit commands. For the introduction of the History package in BBN-LISP, see the [1970 Timeline entry](/history/timeline/#1970).

<span id="interlisp"></span>Interlisp
: Both a language and, in some cases, the implementation of that language. Usually used with some other wording or refinement.
: A GitHub “organization” with ~20 repositories, see <https://github.com/Interlisp>

<span id="interlisp-the-language-and-its-usage"></span>Interlisp: The Language and its usage
: A book by Steve Kaisler which describes Interlisp of the 1970s & 80s.

<span id="interlisp-org"></span>Interlisp.org
: The project's Internet domain name, used for its websites and email addresses.

- <https://interlisp.org>  – the address of the main web site
- <https://online.interlisp.org> – the address of a service that lets you run Medley
- <info@interlisp.org>             - the project's general information email address

<span id="interlisp-d" data-tooltip="What Dorado Lisp became. The D stood for both “Display” and “D-machine”; an implementation of Interlisp, its programming tools, and a Lisp-based operating system for D-machines."></span>Interlisp-D
: What Dorado Lisp became.  The D stood for both “Display” and “D-machine”.  An implementation of

- Interlisp the language
- The Interlisp programming tools
- A Graphical User interface to Interlisp programming development
- A large number of tools, utilities, games, screen-savers
- A Lisp-based operating system for D-machines which, when coupled with microcode
  implementation of a Virtual Machine, allowed the D-machines to operate as a
  personal workstation. Each D-machine had its own microcode with different
  configurations and micro-instructions.

<span id="medley"></span>Medley
: The final named release of Interlisp-D.  

<span id="maiko"></span>Maiko
: An implementation of the functions of the D-machine microcode, but written in C for the
      Sun Microsystems SPARC processor workstation, initially developed by
       Fuji Xerox.  Subsequently ported to little-endian processors and other operating systems.

<span id="package"></span>Package
: The term Package has several different meanings depending on the context:

- Informally, a collection of utilities or submodule in Interlisp (the "break package", q.v.; the "file package", a facility for managing code changes; the "record package", a record data type; and so on)
- A feature of Commmon Lisp symbol support; the package system allows the combining of Interlisp symbols (written with `IL:` prefix) and Common Lisp symbols (written with a `LISP:` prefix).

<span id="prettyprint" data-tooltip="A Lisp utility that formats programs with indentation and line breaks reflecting their list structure, making code easier to read and debug."></span>Prettyprint
: Prettyprint is a Lisp utility that formats programs for human reading. It uses indentation and line breaks to expose the nesting of list structure, so a definition whose subexpressions would otherwise run together is printed with its parts arranged by depth. The layout is generated from the program's list structure rather than preserved from a text file, because a Lisp program is list data. Barstow describes the prettyprinter used in the DED display editor in [“Overview of a Display-Oriented Editor for Interlisp”](/history/bibliography/w96jccyh/) (1981).

  In Interlisp, Prettyprint is more than a whitespace filter. It can print comments stored in a function definition, and global controls set the right margin, the column where comments begin, and how readily square brackets replace parentheses. It prints the saved original definition of a function that is currently broken, advised, or compiled, and tools such as `PRETTYDEF` use it to write definitions, variable values, and property lists to readable files. For the utility's origin and arrival at BBN-LISP, see the [1965](/history/timeline/#1965) and [1966](/history/timeline/#1966) entries in the Timeline.

<span id="spaghetti-stack" data-tooltip="An access and control stack represented as a tree of linked frames that remain addressable after a function returns, so programs can inspect or resume earlier environments."></span>Spaghetti stack
: The spaghetti stack is Interlisp's access and control stack, represented as a tree of linked frames rather than a contiguous pushdown stack. Each frame extension holds a function's variable bindings, return link, and temporaries, and is connected to other frames by access and control links. Because frames remain addressable after a function returns, a program can keep a stack pointer to an exited frame and later examine or resume the computation in that environment. Bobrow and Wegbreit describe the mechanism in detail in [“A Model and Stack Implementation of Multiple Environments”](/history/bibliography/em6wjf9a/) (1973).

  This structure lets programs and debugging tools search the stack for a named function or frame, inspect variable bindings in a caller's context, evaluate an expression in another access chain, and alter the flow of control with a non-local return. It also supports backtracking, coroutines, and generators, which are difficult to implement with a conventional call stack. For the introduction of the spaghetti stack to Interlisp, see the [1970 Timeline entry](/history/timeline/#1970).

<span id="structure-editor" data-tooltip="An editor that operates directly on a program's list structure, moving through subexpressions and inserting, deleting, or replacing elements in place."></span>Structure editor
: A structure editor is an editor that operates directly on a program's list structure instead of its printed text. The expression being edited is a Lisp data object, and the editor's commands move through it by descending into subexpressions, ascending to enclosing expressions, and inserting, deleting, or replacing elements. The edit changes the program itself, not a separate text file. Barstow describes the Interlisp structure editor and its display extension in [“Overview of a Display-Oriented Editor for Interlisp”](/history/bibliography/w96jccyh/) (1981).

  In Interlisp, the structure editor is used mainly to edit function definitions, but it can also edit variable values, property lists, and arbitrary expressions. Because it works on the live list structure, a function can be edited while it is running; a user can modify the definition, re-evaluate it, and continue execution. The editor also supports searching, marks for saving a location, macros, and undoable changes. For the editor's development and its extension at BBN, see the [1968 Timeline entry](/history/timeline/#1968).

<span id="trace" data-tooltip="A debugging facility that prints selected information when a function is entered and its value when it returns."></span>Trace
: Trace is a Lisp debugging facility that prints information about selected function calls as a program runs. It modifies a function's definition so that specified expressions are evaluated and printed when the function is entered, and its value is printed when the call returns; by default, the arguments and return value are shown. Several functions can be traced at once, and the user can choose particular forms to print rather than the full argument list. Bobrow et al. describe the system’s tracing and conditional breakpoint facilities in [*The BBN 940 LISP System*](/history/bibliography/lqaa78hi/) (1967).

  In Interlisp, Trace is implemented as a special case of the Break package: tracing a function installs a breakpoint that prints the requested information and then continues automatically. Because the function is still running normally, tracing gives a running account of calls and values without stopping the program or adding print statements by hand. The effect remains until the function is untraced; in Medley, `UNBREAK` restores functions modified by `BREAK`, `TRACE`, or `BREAKIN`. For the early availability of tracing in Lisp, see the [1965](/history/timeline/#1965) and [1967](/history/timeline/#1967) Timeline entries.

<span id="undo" data-tooltip="A Programmer's Assistant command that reverses the side effects of an operation recorded on the history list, including an earlier operation without undoing later ones."></span>UNDO
: UNDO is a command in the Interlisp Programmer’s Assistant that reverses the side effects of an operation recorded on the history list. Each undoable operation is responsible for saving the information needed to reverse it, so UNDO can restore edited structure, variable assignments, and other changes without requiring the system to anticipate them in advance. The command can undo an earlier event without undoing later ones, and an UNDO can itself be undone. Selective undo and the undoable-operation mechanism are described in detail in Teitelman, [“Automated Programmering: The Programmer’s Assistant”](/history/bibliography/qwkix8dw/) (1972).

  Selective undo is guaranteed for independent operations; undoing dependent operations out of order may not produce the expected result. Users can make their own functions undoable by using the undoable versions of destructive operations, which save the reversal information on the history list. Related history commands such as `REDO` and `USE` rerun recorded events or rerun them with substitutions. For the introduction of UNDO in BBN-LISP, see the [1970 Timeline entry](/history/timeline/#1970).

### Organizations

The following organizations shaped Interlisp's development, distribution, and continuing legacy.

<span id="bbn"></span>BBN
: [Bolt, Beranek, and Newman](https://en.wikipedia.org/wiki/Raytheon_BBN), a Cambridge, Mass. consulting firm which sponsored the
      creation of BBN Lisp, Interlisp's immediate ancestor, as well as the Tenex operating system.

<span id="envos"></span>Envos
: Company founded in 198x to take on the Lisp business from Xerox. Closed within 10 months and folded back into Xerox.

<span id="fuji-xerox"></span>Fuji Xerox
: Xerox's Japanese subsidiary, owned jointly by Rank Xerox and Fujifilm Corp., responsible for selling and supporting Interlisp-D systems in Japan.

<span id="interlisporg"></span>InterlispOrg
: A [California-registered](https://rct.doj.ca.gov/Verification/Web/Details.aspx?result=c7aa8cb2-16ec-458a-be56-41f963365258) non-profit organization  (DBA Interlisp.org) Established
        August 2021. 501c3  EIN 87-2528093  California registered charity CT0278267.
        The Board of Directors consists of Larry Masinter, President; Ron Kaplan, Treasurer; and Herb Jellinek, Secretary.

<span id="medley-interlisp-project"></span>Medley Interlisp Project
: Began late 2010’s with Nick Briggs getting Maiko to run on macOS.  The group expanded and began holding weekly online meetings in 2020.
Subsequently ported Maiko (and therefore Medley) to Linux, Windows, and other operating system.  Maintains a mailing list for developers and interested users,
sponsors the maintenance of an exhaustive bibliography and the very website where you're reading this.

<span id="rank-xerox"></span>Rank Xerox
: Xerox's European subsidiary, a joint venture of Xerox Corp. and the Rank Organization, which sold Interlisp-D workstations in Europe.

<span id="sri-international"></span>SRI International
: A non-profit scientific R & D institute, headquertered in Menlo Park, California.

<span id="venue"></span>Venue
: Company founded by John Sybalsky, former Xerox and Envos employee, which obtained a license to create and distribute derivative works of Maiko and Medley.

<span id="xais"></span>Xerox Artificial Intelligence Systems (XAIS)
: The former Xerox division working to commercialize Xerox workstations running Interlisp-D.

<span id="xeos"></span>Xerox Electro-Optical Systems (XEOS)
: A former Xerox division supporting government customers.

<span id="parc"></span>Xerox PARC or just PARC
: Palo Alto Research Center, which continued in collaboration with BBN on (renamed) Interlisp. PARC developed the Alto and Dorado.  Now part of SRI International.
