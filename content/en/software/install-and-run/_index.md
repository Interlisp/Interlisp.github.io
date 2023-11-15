---
title: Install and Run
weight: 30
type: docs
---

You can install Medley on a variety of different computer systems:

* Download and install from a release
  * [Running on Mac](./running-on-mac)
  (Is this active or still in progress? If it is not ready, I do not think we should not have it listed.)
  * [Running on Windows](./running-on-win)
    * For Windows 10 or 11 with WSL1 or WSL2
  * [Running on Linux](./running-on-linux)
    * Packages for .deb distributions and source to build for others

It's important to understand that the Medley and the Interlisp software it's built on are the same for any computer it runs on. What's different is Maiko, the virtual machine emulator that hosts Interlisp on a given computer system. It works a bit like the Java Virtual Machine -- and in fact Herb Jellinek, a member of the Interlisp team, went on to contribute to the Java project at Sun.

If you'd like to run Medley on another OS or machine architecture like BSD or Android, you can (re)build Maiko from source and then run in a release or even build your own images (sysouts).

(Where does the link to the build topics fit into these pages?)

See README.md files in the GitHub repo.
