---
title: The Basics of Interlisp
url: /doc/info/Using.html
weight: 2
---

Some very basics -- enough to get you to find the Medley User's Guide of ~30 years ago.

# Interlisp

Interlisp is a dialect of Lisp and as such, it is based on the familiar
syntax of left-parenthesis, function name, arguments, and
right-parenthesis.  Besides many of the functions having different
names and arguments compared to Common Lisp, Interlisp has many other,
more fundamental, differences from Common Lisp.  While this section
will not go into any of the functional differences between Interlisp
and Common Lisp, it will attempt to detail the more fundamental
differences between the two.  The reference manual may be used for a
detailed description of the Interlisp functions.

## Upper- and Lower Case

Interlisp uses mixed case.  That is, upper-case letters and lower-case
letters are treated as different.  This means you can have a variable
name `my-var` and a variable named `MY-VAR` that are unique and
unrelated to each other. This is true for Common Lisp too, but
the READ function in Common Lisp translates.

Most Interlisp primitives are upper case.

As a side note, the Medley system includes a package called DWIM (Do
What I Mean).  This system reads in what you type and attempts to
automatically correct input errors.  At times, in an effort to correct
typing errors this system will auto-convert something you type in
lowercase into uppercase.  Thus it may appear that the case doesn't
matter - but it does.

## Variables

Except for Special Variables, variables in Common Lisp are lexically
scoped.  This means that local variables are only visible within the
scope they are defined.  This means, among other things, that
variables defined in one function are not visible to other functions.

In functions that are running interpretively (as opposed to having
been compiled), variables in Interlisp are dynamically scoped.  This
means that variables are visible within the dynamic environment they
are in.  For example, let's say we create two functions `FUN1`
and `FUN2`.  If `FUN1` introduced a local variable and then
called `FUN2`, then `FUN2} would have access to the variable
since it is in the dynamic environment of being called by `FUN1`.
In other words, the variable was in existence when `FUN2` was
called.  However, the Interlisp compiler "hides" variables unless
they are "declared special", so that they are essentially lexically scoped,
as in Common Lisp.

Common Lisp also supports dynamic variables as well.  They are called
the Special Variables.

## LISP-2

Like Common Lisp but unlike Scheme, Interlisp is a LISP-2 language.
This means, in part, that the namespace for variables is separate from
the namespace for functions.  For example, in Interlisp and
Common Lisp, you can simultaneously have a variable named `ABC`
and a function named `ABC` that are unrelated.

## LAMBDA & NLAMBDA & CL:LAMBDA

Interlisp shares the notion of `LAMBDA` expressions with Common Lisp,
as a way of defining functions. Interlisp `LAMBDA` specifies a list
of parameters; Common Lisp parameter lists can be decorated with
`:OPTIONAL`, `:REST` and `:KEYWORD` parameters. Interlisp also
adds the notion of an `NLAMBDA` function that doesn't evaluate
its arguments --  arguments to 
`NLAMBDA` function are passed directly into a function without 
being evaluated.

Interlisp supports spread and no-spread lambda arguments similar to
Common Lisp.  However, Interlisp treats all arguments as
optional (if not provided they default to NIL) and ignores extra arguments
(no warning or error is raised).

## Macros

Interlisp supports macros but unlike Common Lisp, Interlisp symbols
may simultaneously have a function definition and a macro definition.
If a symbol has both a function definition and a macro definition, the
function definition is used by the interpreter and the macro
is used by the compiler.  This allows for extra error checking during 
development and fast operation during production use.

Interlisp also has a backquote facility similar to Common Lisp's \`
and \, read macros.

Unlike Common Lisp, Interlisp does not have a special function for
defining macros.  Macros are defined by placing their definition on
the property list of the symbol.

# Medley Common Lisp

The term "Common Lisp" covers a range of development stages, first
defined by the book "Common Lisp, the Language" editions 1 (aka CLtL1)
and 2 (aka CLtL2) and ultimately the ANSI Standard Common Lisp (aka ANSI).
The Common Lisp currently supported by Medley is somewhere between
CLtl1 and CLtl2.  We are hoping to complete the move to
CLtl2.

In Medley Common Lisp and Interlisp are fully
integrated.  From within Common Lisp, Interlisp functions may be
accessed through the Common Lisp package nicknamed ``IL''.

# Continuing On

This introduction was designed to provide the most general of
information -- just enough to get you started.  Medley comes
with extensive documentation. 

In searchable PDF and (imperfect) HTML:


* (1991) [Sun User Guide](/documentation/SunUserGuide.pdf) ([HTML](https://interlisp.org/SunUserGuide.html))
* (1992) [Medley for the Novice](/documentation/Medley-Primer.pdf) ([HTML](https://interlisp.org/Primer.html))
* (1993) [Interlisp Reference Manual](/documentation/IRM.pdf)  ([HTML](https://Interlisp.org/IRM.html)) 

Medley Interlisp also includes an online reference:

* right-click on the desktop to get to the system menu
* select DInfo

_or_, at any prompt, the `man` command will look up an (Interlisp) symbol.

------------
_Many thanks to [Blake McBride](https://github.com/blakemcbride) and his [Medley Intro](https://github.com/blakemcbride/medley-intro) from which this was initially taken._