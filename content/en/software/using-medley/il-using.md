---
title: Using Medley Interlisp Basics
weight: 20
type: docs
---
the [parent page](/software/using-medley/) has pointers to additional resources.
Medley Interlisp also includes an online reference:

* right-click on the desktop to get to the system menu
* select DInfo

_or_, at any prompt, the `man` command will look up a symbol or phrase in the Interlisp Reference Manual (IRM) and/or the Common Lisp HyperSpec.

## Writing a sample Interlisp program

In an (INTERLISP) Exec window, type the following:

```lisp
(PLUS 1 1)
```

When you complete typing the ending `)` the Interlisp interpreter will perform the calculation and return the result.

One thing you probably noticed, the function name `PLUS` is capitalized. This is traditional -- Interlisp programmers commonly ran with the caps-lock turned on.  It’s not that the developers of Interlisp were always shouting at each other. Rather, when Interlisp was developed computer programming was in its early days and all-caps type-in was common. (It's possible to change the Interlisp exec to automatically capitalize symbols at imput, as is the case with the Common Lisp exec, if that's your preference.)

