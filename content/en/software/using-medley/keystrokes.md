---
title: Keystrokes, Mouse menus and Gestures
url: /software/using-medley/keystrokes/
weight: 40
type: docs
aliases:
 - /doc/info/Keystrokes.html
---

The handling of keyboard and mouse clicks and gestures is different and varied within the Medley environment. This chart shows common keystrokes. On macOS the Option key is equivalent to Alt. See
[Table of Keystrokes](https://docs.google.com/spreadsheets/d/1FOkrr62TtEhhY49m9U0T_6bvqSGRQt9fBRtMDw0YKtY/edit?usp=sharing) for more data.

We'd like to improve keyboard handling but haven't yet found a path.

## At an "exec" (i.e., the REPL) 

|character |action                          |
|----------|--------------------------------|
|Backspace | delete the previous character  |
|Ctrl-H    |   (same as backspace)          |
|Enter     |if terminates a valid expression evaluate, otherwise newline    |
|Ctrl-M    |  (same as Enter)               |
|Ctrl-Alt-J|move down                       |
|Ctrl-Alt-L|move to start of line (some OSes capture this for system functions, e.g. screen lock on Linux)          |
|Ctrl-Alt-Y| invoke an old-style executive (REPL), but uses the package and readtable of its caller             |

## Interrupt characters

These are enabled per-process. Medley maintains, for each process, a "termtable" which enables different kinds of interrupts.

Usually, the user wants interrupts to occur in the TTY process, which is the one
currently receiving keyboard input. However, sometimes the user wants to interrupt
the mouse process, if it is currently busy executing a menu command or waiting
for the user to specify a region on the screen. Most of the interrupt characters
below take place in the mouse process if it is busy, otherwise the TTY process.

|character|action                                                |
|---------|-----------------------------------------             |
|Ctrl-B   |stop the process and enter a break window             |
|Ctrl-D   | reset the process, unwind the stack to the top level |
|Ctrl-E   | unwind the stack as if an error occured without break|
|Ctrl-G   | interrupt a non TTY process and open the debugger|
|Ctrl-P   | interrupt printing and reset the PRINTLEVEL          |
