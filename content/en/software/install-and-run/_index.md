---
title: Install and Run
aliases:
 - /medley/using/build
 - /medley/using/running
 - /medley/using/build/building/
 - /developing
weight: 10
type: docs
---

You can install Medley on a variety of different computer systems. 


### Download and install from a release
  * [Running on Linux](./running-on-linux)
    * Packages for .deb distributions and source to build for others
  * [Running on Mac](./running-on-mac)
    * for MacOS
  * [Running on Windows](./running-on-win)
    * [Running on Windows with WSL](./running-on-wsl)


Medley has a virtual machine architecture: there's a virtual machine implementation (called Maiko) and Lisp software that is compiled into instructions for it. The compiled code and memory images can be moved from one architecture to another -- only Maiko needs to be ported. Maiko has been substantially revised and modernized, so you can to run Medley on many different OSes and machine architectures.

See the [Maiko README](https://github.com/Interlisp/maiko#readme) and [Medley README](https://github.com/Interlisp/medley#readme) in their respective GitHub repository pages for more details on how to build and run them.

The current systems we've tested or for which we have confirmed reports can be found [in the Maiko github repository](https://github.com/Interlisp/maiko/tree/master/bin), including:
* OS:  FreeBSD, Linux, MacOS, Solaris, Windows (using WSL or CygWin)
* CPU: arm7l, arm64, PowerPC, SPARC, i386, x86_64



