---
title: FAQs
weight: 20
type: docs
---

## Is copy and paste available?

In Medley, there are three main editors used commonly:

* TEdit (full WYSIWYG styled text editor)
* SEdit (structure editor for Lisp code, package aware)
* TTYIN (Type-in using keyboard)

The original method for copy/paste is different from most modern systems:
* click with mouse the destination
* hold down the shift key, and, while holding, select the source (using left mouse button to select a point, right button or repeated left button to extend the selection)
* let up the shift key. The system will copy from the selected content and paste it in the destination.

To do a cut/paste operation, hold down the control key as well as the shift key.

Modern Medley (in the CLIPBOARD software) adds an interface with the host OS's Clipboard.  Typing meta-C does copy to clipboard, and meta-V will paste from the clipboard into the destination. The 'meta' key is the one labeled 'cmd' on a Macintosh, and the left side 'Alt' key on most windows keyboards.

## How to ask for help about a specific function?

There is a graphical browser of the Interlisp Reference Manual -- right click any area of the screen not in a window (i.e., the background) and select DInfo.

The `MAN` command can be used in an EXEC:
```
MAN HELP
```
In addition, typein of a list structure followed by a question mark followed by an 'enter' will look up (using DInfo) the symbol entered in the enclosing list:
```
(CONS ?
```
Modern Medley extends this to look up Common Lisp functions in the Common Lisp HyperSpec. 

Further, typein of a expression form followed by a question mark and equals sign followed by an 'enter' will look up the _closest_ function name (for any defined function) entered in the form and display that function's invocation form:
```
(SETQ FOO (LOAD ?=
```
shows
```
(LOAD FILE LDFLG PRINTFLG)
```
Interlisp EXEC commands are case and package insensitive, although the rest of the input line depends on the context.

## When to pop up a debugger or just report an error and unwind?

Interlisp uses a heuristic to decide when to simply print an error message and when to open a "break" window for the error; the decision is based on compute-time-since-last-user-input and stack depth. We've adjusted these parameters but modern machines are 1000 times faster, and the clock resolution is too coarse.

The `retry` command is handy in this situation.

For example typing `(+ 1 Z)` may only show the error message:  
`Z is an unbound variable.`  
without a break window opening. If you 
```
 RETRY
```
then a debugger window will pop up. Let's give Z a value while in the debugger:
```
(SETQ Z 9)
```
now type `OK` and _enter_ (or middle click in the debugger then choose Ok). It will continue the execution as if the fault never happened. It will return the value 10.
