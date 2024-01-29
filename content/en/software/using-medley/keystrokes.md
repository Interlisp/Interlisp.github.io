---
title: Keystrokes, Mouse menus and Gestures
url: /software/using-medley/keystrokes/
weight: 40
aliases:
 - /doc/info/Keystrokes.html
---

The handling of keyboard and mouse clicks and gestures is different and varied within the Medley environment. This chart shows common keystrokes.
[Table of Keystrokes](https://docs.google.com/spreadsheets/d/1FOkrr62TtEhhY49m9U0T_6bvqSGRQt9fBRtMDw0YKtY/edit?usp=sharing) more data.

We'd like to improve keyboard handling but haven't yet found a path.

## At an "exec" (i.e., the REPL). 

|character |action                          |
|----------|--------------------------------|
|backspace | delete the previous character  |
|ctrl-H    |   (same as backspace)          |
|enter     |if at end of line, terminate    |
|ctrl-M    |  (same as enter)               |
|ctrl-alt-J|move down                       |
|ctrl-alt-L|move to start of line           |
|ctrl-alt-Y|"get userexec" ????             |

## Interrupt characters

These are enabled per-process. Medley maintains, for each process, a "termtable" which enables different kinds of interrupts. In general, the process (sometimes known as the "TTY" process or the process that "has the keyboard". 

|character|action                                                |
|---------|-----------------------------------------             |
|ctrl-B   |stop the process and enter a break window             |
|ctrl-D   | reset the process, unwind the stack to the top level |
|ctrl-E   | unwind the stack as if an error occured without break|
|ctrl-P   | interrupt printing and reset the PRINTLEVEL          |




