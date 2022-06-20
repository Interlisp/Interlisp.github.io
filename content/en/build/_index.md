---
title: Building the Interlisp system
url: /doc/build.html
aliases:
- /_pages/doc/build.html
type: docs
---

Medley Interlisp is open-source and may be obtained from GitHub. It is portable to many different Linux and Apple MacOS systems, as well as Windows using WSL2.

The core is written in portable C. The system currently depends on an X11 system for its display.
Obtaining The System

The system comes in two parts. The first is a C-based virtual machine [Maiko](https://github.com/interlisp/maiko).

The remainder of the system is OS / architecture-independent and can be found in the [Medley repository](https://github.com/interlisp/medley).

You can now download Medley Interlisp from a release without building anything; see the Medley [README](https://github.com/interlisp/medley/#readme)

See The Maiko [README](https://github.com/Interlisp/maiko/#readme) for build instructions for Maiko, for systems for which there is no pre-built release.
