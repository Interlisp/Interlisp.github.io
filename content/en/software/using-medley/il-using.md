---
title: Using Medley Interlisp Basics
weight: 20
type: docs
---
[exploratory programming]: https://en.wikipedia.org/wiki/Exploratory_programming

## Welcome to Medley!

Welcome to Medley. We hope you will come to be excited about this
retrofuturistic technology as we are.

Medley does things a little differently from other Lisp implementations you
might have seen before. It also treats user interfaces in a way that you've
likely not seen before. Let's get oriented.

## The Medley Mental Model

<details>
<summary>Medley embraces <em>exploratory programming</em> in a user interface
that is joined to your running program. Understanding the mental model may help
you navigate the documentation or development more easily.</summary>

The model of software development you are probably familiar with is inspired by
the ALGOL family of languages: C, Perl, Python, Java, etc. In this paradigm,
the development cycle looks something like:

1. Write/Update code
2. Run code
3. For an ephemeral moment, your code is "in" the OS  i.e. _the program_ is
   running
4. You decide to change behavior due to a bug or a new feature so you shut down
   _the program_. The OS releases that memory
5. Loop

Medley approaches things where differently. Like the ALGOL paradigm, Medley
seeks to generate a correct program. But it doesn't treat that program as an
ephemeral process. The program and the process _are the same thing_. The
program can be adjusted without having to do a "stop the world, read in updated
code, start a slightly-different world" iteration.

In the Medley model, through a suite of tools that _are part of the program_ --
Read-Eval-Print Loop (REPL), graphical explorers, documentation, version
control, debugger, built-in documentation, etc. -- you groom _the program_ to
correctness. Your portal into the program is the `EXEC` window which lets you
write Lisp to change the running state of _the program_. This development cycle
looks like:

1. There is a durable, long-running _program_ hosted by the OS + Medley that
   offers you tools, an editor, and a portal for updating the running program
2. Write code "in" _the program_ (`EXEC` window)
3. Run code "in" _the program_ (`EXEC` window)
4. _Optional_: Use visualizers, expression editors, bitmapped pictures to
   analyze the code
5. Judge correctness of behavior
6. Loop

Fascinating, no?

A different way of understanding these models of programming can be understood
by considering how you would share a program. In Medley, the memory state of
_the program_ can be written to disk (called a "SYSOUT") and given to a fellow
user/developer. They load it and they have your program. In the non-Medley
model, the goal is to be given a set of artifacts (files) that can be cajoled
(`make`, `clang`, `#ifdefs`) into recreating a system artifact that can be
loaded _into_ the OS.

### Exploratory Programming

All told, the design of Medley facilitates "[exploratory programming]." At the
time of Medley's birth, a lot of programming was encoding existing
processes/algorithms/behaviors into software. But Medley was/is a premier
environment for providing all the basic tools the developer needs to get
iterating on how _the program_ should work. No template repositories or code
generators, no packaging tarpit before writing your first line of code -- just
start exploring your way to _the program_. It is the ultimate agile
environment: a few commands and a full interactive mock-up is on the screen.

If you're feeling your brain stretching in a new way, excellent! You're in good
company here.  There's a lot more to discover about the coding experience in
Medley, but this is a primer, after all.
</details>

## 0. Launch and Two Windows

<figure>

![The Medley Interlisp programming environment as provided by interlisp.org is shown. Its a dithered black and white background with two windows for input shown. One is labeled 'Prompt Window', the other, 'EXEC'.  Inside the latter, a Lisp REPL is running. At the right are some buttons that link into documentation resources.](/images/software/using-medley/il-using/00-launch.png)

<caption>
<em>Medley with its two primary interfaces: 'EXEC' and 'Prompt Window'. Note
the documentation link-buttons at right.</em>
</caption>
</figure>

When you open/launch Medley, the first thing you'll notice are two windows:

_The program_ can be "spoken to" through a Lisp REPL in the `EXEC` window. The
REPL respects several dialects of Lisp: Interlisp, Common Lisp, and Xerox
Common Lisp. You can choose whichever you prefer, and we'll show you to launch
it below. Each of the Lisps respect packaging, so even if you're in (say)
Common Lisp, you can access an Interlisp command by adding the prefix `IL:`,
e.g. `(IL:FONTSIZE 'HUGE)` to get a large font.

The `Prompt Window` is where you interact with the development environment or
"as a user." Menu "tool tips" show up here as well as other interactive
activities.

## 1. Use the mouse and RIGHT-CLICK+HOLD

The mouse was invented not far from where Medley was created! At the time,
building pointer-based was still pretty rare. Medley's point-and-click feels
contemporary with systems like WindowMaker window manager, NeXSTSTEP, or the
CDE environment. Medley and these peers used button patterns that pre-dated the
paradigms that Windows or Mac OS brought to large audience

In Medley, the mouse's **third button** is used to summon/traverse menus. The
**first** button is used to confirm or finalize behavior.

On some hardware, the **third button** will be your _right_ button; on other
hardware: perhaps both left and right clicked together

Try clicking on the background of Medley. You'll be given the system menu.

<figure>

![The Medley Interlisp programming environment as provided by interlisp.org is shown. Its a dithered black and white background with two windows for input shown. One is labeled 'Prompt Window', the other, 'EXEC'.  Inside the latter, a Lisp REPL is running. At the right are some buttons that link into documentation resources. A system menu is active that contains a menu item called 'EXEC.'](/images/software/using-medley/il-using/01-system-menu.png)

<caption>
<em>Launching a system window</em>
</caption>
</figure>

_While holding the middle button_ mouse over `EXEC`; then mouse to the right
boundary of the system menu near the disclosure triangle and a submenu will
expand at right that allows you to choose a Lisp interpreter.

<figure>

![The Medley Interlisp programming environment as provided by interlisp.org is shown. Its a dithered black and white background with two windows for input shown. One is labeled 'Prompt Window', the other, 'EXEC'.  Inside the latter, a Lisp REPL is running. At the right are some buttons that link into documentation resources. A system menu is active that contains a menu item called 'EXEC.' That menu item is reverse colored indicating selection. Next to the system menu is a sub menu offering a variety of Lisp interpreters. The 'Interlisp' interpreter is highlighted by reverse color.  Together, these menus indicate an intention to launch an 'Exec' window that runs the Interlisp interpreter.](/images/software/using-medley/il-using/01-system-menu-with-submenu.png)

<caption>
<em>Medley with its system menu and a sub-menu at right</em>
</caption>
</figure>

Mouse over the interpreter of your choice and then release the button.  Medley
will then prompt you with an outline of a window whose dimensions you will
"sweep out." This will feel familiar to those who know the `twm` window
manager. 

<figure>

![The Medley Interlisp programming environment as provided by interlisp.org is shown. Its a dithered black and white background with two windows for input shown. One is labeled 'Prompt Window', the other, 'EXEC'.  Inside the latter, a Lisp REPL is running. At the right are some buttons that link into documentation resources. An outline of a window is being adjusted.  It will contain some function.](/images/software/using-medley/il-using/01-sweeping.png)

<caption>
<em>"Sweeping out" a window</em>
</caption>
</figure>

Click and drag the **left button** to create a window outline of a comfortable
size.  Release the button and you'll, as we say around here, "have a new EXEC"
running your chosen interpreter.

<figure>

![The Medley Interlisp programming environment as provided by interlisp.org is shown. Its a dithered black and white background with two windows for input shown. One is labeled 'Prompt Window', the other, 'EXEC'.  Inside the latter, a Lisp REPL is running. At the right are some buttons that link into documentation resources. A new window, called 'an EXEC' is seen at right.](/images/software/using-medley/il-using/01-new-exec.png)

<caption>
<em>A new <code>EXEC</code></em>
</caption>
</figure>

## 2. Working with the EXEC (a REPL)

If our goal is to create the right memory state that's shimmed with _just
enough_ of a development environment and _just enough_ user interface, then we
need a way to key that information in. The simplest way, and the way most
familiar to anyone who has read a chapter or two of a Lisp tutorial, is to use
the `EXEC`'s Lisp REPL.

In an (INTERLISP) Exec window, type the following:

```lisp
(PLUS 1 1)
```

When you complete typing the ending `)` the Interlisp interpreter will perform
the calculation and return the result.

One thing you probably noticed, the function name `PLUS` is capitalized. This
is traditional -- Interlisp programmers commonly ran with the caps-lock turned
on.  It’s not that the developers of Interlisp were always shouting at each
other. Rather, when Interlisp was developed computer programming was in its
early days and all-caps type-in was common. It's possible to change the
Interlisp exec to automatically capitalize symbols at input, as is the case
with the Common Lisp exec, if that's your preference.

## 3. Documentation

Our [parent page](/software/using-medley/) has pointers to additional
resources.  Medley Interlisp also includes an online reference:

* right-click on the desktop to get to the system menu
* select DInfo

_or_, at any prompt, the `man` command will look up a symbol or phrase in the Interlisp Reference Manual (IRM) and/or the Common Lisp HyperSpec.

> :caution: Sadly, font size changes are not respected in `DInfo`. Pull
> requests accepted and appreciated!

TODO Should probably cover how to use DInfo, the graph thing is pretty great,
but there are some steps like go forward, go back, how to traverse the stack of
help nodes, etc. that ought be covered.

## 4. Copy and Paste; History and Edits

TODO: needs more information;

Inside Medley Online, you can copy-and-paste with your host operating system's
key shortcuts. Medley developers are also given a rich history of redo,
history, and history but with an update option in a manner similar to history
expansion/replacement as provided by Unix shells. While you're getting started,
this can be a complication best avoided, though. When you're ready, consult the
specification for tools like `(redo)` and `(undo)`.

## 5. Tools for Authoring Lisp

If you're coming from SLIME / SWANK or some other Lisp editing tool, you're
going to recognize that keying things directly into the REPL is a consequence
of code you groom inside of an editor.

TODO cover base case here

When working with text, we launch `TEDIT`. You can write your expressions in
TEDIT and then copy/paste them into the REPL. Once you get comfortable using
history editing, you'll realize that writing, grooming, editing, replacing,
etc. are all well done inside the EXEC itself. But this _is_ a Basics document,
after all.

TODO: Needs expansion, I've not found a workflow here.

In Medley, we have multiple editors that work at the level of text as well as at
the level the symbolic express (sexp).

## 6. Handling Interrupts

A final magical part about working with Lisp is when something goes wrong we
fall back to "interrupts"

TODO: I've not figured out how to deal with interrupts. Nor have i figured a
good way to hit an interrupts debugger ( / 2 0) doesn't hit the interrupt
debugger (is there one? Huh?)

