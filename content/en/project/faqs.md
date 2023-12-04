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
* click with ouse the destination
* hold down the shift key, and, while holding, select the source (using left mouwse button to select a point, right button or repeated left button to extend the selection)
* let up the shift key. The system will copy from the selected content and paste it in the destination.

To do a cut/paste operation, hold down the control key as well as the shift key.

Modern Medley (in the CLUPBOARD software) adds an interface with the host OS's Clipboard.  Typing meta-C does copy to clipboard, and meta-V will paste from the clipboard into the destination. The 'meta' key is the one labeled 'cmd' on a Macintosh and 'alt' on most windows keyboards.

## How to ask for help about a specific function?

There is a graphical browser of the Interlisp Reference Manual -- right click any area of the screen not in a window (i.e., the background) and select DInfo.

The `MAN` command can be used:
```
MAN HELP
```
In addition,  typein of a list structure a question mark followed by a 'enter' will look up in the symbol entered in the enclosing list:
```
(list ?
```
Modern Medley extends this to look up Commonn Lisp functioins in the Common Lisp HyperSpec.

Interlisp EXEC commands are case and package insensitive, although the rest of the input line depends on the context.

## When to pop up a debugger or just report an error and unwind?

The command `retry` will redo a typein but invoke the debugger.

For example typing (+ 1 A) will only show the error message:
A is an unbound variable.
```
 RETRY
```
  and a debugger window will pop up. let's give A a value while in the debugger:
```
(SETQ A 9)
```
now middle click in the debugger then choose Ok and it will continue the execution as if the fault never happened. It will return the value 10.