---
title: Interlisp Basics for Common Lisp users
url: /software/using-medley/cl-using/
type: docs
weight: 30
---

If you are familiar with Common Lisp, this guide helps with some unexpected features.

### Advice for newcomers

A coding project is a great learning experience. But porting existing Common Lisp software to Medley may be challenging as a first project.

Modern Common Lisps are similar and implement most of ANSI Common Lisp. Adapting software to these environments usually involves minor modifications you can carry out with familiar tools. But the Medley environment is very different and its Common Lisp farther from ANSI.

Porting to Medley is a substantial task for a newcomer who has to deal at the same time with an incomplete Common Lisp implementation, unfamiliar tools, and an unknown workflow.

It's like hustling the move to a new country you barely speak the language and know the culture of. Within hours of landing at the airport you attempt to open a bank account, apply for a loan, file for health care, register with the tax system, negotiate renting an apartment, and do the paperwork for requesting the services of utility companies. Doing all this immediately after your arrival is overwhelming at best.

For a more enjoyable stay take the time to settle, absorb the local language and culture, and live like a native.

Rather than porting Common Lisp programs, it's better to start with small Interlisp projects that rely only on Medley's features and resources with no external dependencies or interactions. Write Interlisp code from scratch instead of bringing in existing software.

We recommend to take Medley a little bit at a time. [Read the introductory material](/software/using-medley/#introductory-material), and write at least one or two small Interlisp programs of no more than a thousand lines of code.

## Interlisp

Interlisp is a dialect of Lisp and as such, it is based on the familiar syntax of left-parenthesis, function name, arguments, and right-parenthesis.  Besides many of the functions having different names and/or arguments compared to Common Lisp, Interlisp has many other, more fundamental, differences from Common Lisp.  While this section will not go into any of the functional differences between Interlisp and Common Lisp, it will attempt to detail the more fundamental differences between the two. 

### Upper- and Lower Case

Interlisp uses mixed case.  That is, upper-case letters and lower-case
letters are treated as different.  This means you can have a variable
name `my-var` and a variable named `MY-VAR` that are unique and
unrelated to each other. This is true for Common Lisp too, but
the READ function in Common Lisp translates (unescaped) lower-case to upper-case within symbols. Most Interlisp primitives are upper case. 

As a side note, the Medley system includes feature called DWIM (Do
What I Mean).  When code would ordinarily cause an error to occur,
DWIM first  attempts to correct the error, e.g., by spelling correction
on variables and function names. In many situations DWIM will ask the
user to approve the change, but in some situations (like evaluating
a typed in variable using the wrong case-shift). DWIM will just
make the change, printing out that what it did.
 It may appear that the case doesn't matter - but it does.

### Variables

Except for Special Variables, variables in Common Lisp are lexically
scoped.  This means that local variables are only visible within the
scope they are defined.  This means, among other things, that
variables defined in one function are not visible to other functions.

In functions that are running interpretively (as opposed to having
been compiled), variables in Interlisp are dynamically scoped.  This
means that variables are visible within the dynamic environment they
are in.  For example, let's say we create two functions `FUN1`
and `FUN2`.  If `FUN1` introduced a local variable and then
called `FUN2`, then `FUN2` would have access to the variable
since it is in the dynamic environment of being called by `FUN1`.
In other words, the variable was in existence when `FUN2` was
called.  However, the Interlisp compiler "hides" variables unless
they are "declared special", so that they are essentially lexically scoped,
as in Common Lisp.

Common Lisp also supports dynamic variables as well.  They are called
the Special Variables.

### LISP-2

Like Common Lisp but unlike Scheme, Interlisp is a LISP-2 language.
This means, in part, that the namespace for variables is separate from
the namespace for functions.  For example, in Interlisp and
Common Lisp, you can simultaneously have a variable named `ABC`
and a function named `ABC` that are unrelated.

### LAMBDA & NLAMBDA & CL:LAMBDA

Interlisp shares the notion of `LAMBDA` expressions with Common Lisp,
as a way of defining functions. Interlisp `LAMBDA` specifies a list
of parameters; Common Lisp parameter lists can be decorated with
`&OPTIONAL`, `&REST` and `&KEYWORD` parameters. Interlisp also
adds the notion of an `NLAMBDA` function that doesn't evaluate
its arguments --  arguments to 
`NLAMBDA` function are passed directly into a function without 
being evaluated.

Interlisp supports spread and no-spread lambda arguments similar to
Common Lisp.  However, Interlisp treats all arguments as
optional (if not provided they default to NIL) and ignores extra arguments
(no warning or error is raised).

### Macros

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

Medley handling of macros is different: from a Common Lisp point of view, Interlisp "macros" are treated as compiler-optimizers (if the symbol has a function definition) or as (Common Lisp) macros.

## Medley Common Lisp

The term "Common Lisp" covers a range of development stages, first
defined by the book "Common Lisp, the Language" editions 1 (aka CLtL1)
and 2 (aka CLtL2) and ultimately the ANSI Standard Common Lisp (aka ANSI).
The Common Lisp currently supported by Medley is somewhere between
CLtl1 and CLtl2.  We are hoping to complete the move to
CLtl2.

In Medley Common Lisp and Interlisp are fully
integrated.  From within Common Lisp, Interlisp functions may be
accessed through the Common Lisp package nicknamed ``IL''.

<div class="mx-auto">
 <a class="btn btn-lg btn-danger mr-3 mb-4" href="{{< relref "/software/using-medley" >}}">
  Guide to Using Medley <i class="fas fa-arrow-alt-circle-right ml-2"></i>
 </a>
</div>
