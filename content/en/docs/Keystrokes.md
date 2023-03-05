---
title: Keystrokes, Mouse menus and Gestures
url: /doc/info/Keystrokes.html
weight: 40
---
The handling of keyboard and mouse clicks and gestures is different and varied within the Medley Interlisp environment. This chart shows common keystrokes.
[Tabled of Keystrokes](https://docs.google.com/spreadsheets/d/1FOkrr62TtEhhY49m9U0T_6bvqSGRQt9fBRtMDw0YKtY/edit?usp=sharing) has the raw data.


## At an "exec" (i.e., the REPL)

|character |action                        |
|----------|------------------------------|
|back      |delete the previous character|
|ctrl-H    |  ""                         |
|ctrl-M    |insert End-of-Line           |
|ctrl-alt-J|move down                    |
|ctrl-alt-L|move to start of line        |
|ctrl-alt-Y|"get userexec" ????          |
|ctrl-P    |interrupt typeout,set printlevel|


## Interrupt characters

These are enabled per-process. Medley maintains, for each process, a "termtable" which enables different kinds of interrupts. In general, the process (sometimes known as the "TTY" process or the process that "has the keyboard". 

|character|action                                                |
|---------|-----------------------------------------             |
|ctrl-B   |stop the process and enter a break window             |
|ctrl-D   | reset the process, unwind the stack to the top level |
|ctrl-E   | unwind the stack as if an error occured without break|
|ctrl-G   | ?? |


