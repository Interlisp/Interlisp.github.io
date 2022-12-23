---
title: Using Interlisp Online
weight: 8
type: docs
---

### A Brief Introduction

### Running Interlisp Online

* Go to [Interlisp Online](https://online.interlisp.org/main)\
{{< imgproc Login_Screen Resize "400x450">}} Interlisp Online Login {{< /imgproc >}}
  You may either login as a Guest or create an account. If you plan to save and later retrieve files, [register](https://online.interlisp.org/user/register) and create an account. Guest logins are not guaranteed to perserve sessions and stored files.

However, if you just want to get a taste of Interlisp without the extra effort of creating an account, the guest login will suit your needs.

* Select the Exec you want to run. For this exercise, select `Interlisp`
* Leave the `Fill browser window` option set.

Select `Run Medley`. Your browser will open a window that represents the Interlisp Desktop and looks much like this:

{{< imgproc Online_Initial_Medley Resize "800x450">}} Medley Interlisp{{< /imgproc >}}

The Interlisp Desktop at startup contains 4 windows of interest:

* Prompt Window: The black window at the top of the screen. It is used to display system or application prompts
* Exec (INTERLISP) window: The main window where you run functions and develop programs.
* Medley logo window: A window containing the Interlisp Medley logo as a bit map.
* Status Bar window

### Writing Interlisp programs

In the Exec window, type the following:

```lisp
(PLUS 1 1)
```

When you complete typing the ending `)` the Interlisp interpreter will perform the calculation and return the result.

One thing you probably noticed, the command `PLUS` is capitalized. It’s not that the developers of Interlisp were always shouting at each other. Rather, when Interlisp was developed computer programming was in its infancy and standards for naming commands were still evolving.

### Save your program as a file

### Opening a saved program

### What next?
