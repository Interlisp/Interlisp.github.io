---
title: Running Medley Interlisp
weight: 30
type: docs
---

There are several different ways of running Medley Interlisp. Which you choose depends a bit on your platform (Mac, Windows, Linux, other).

* Interlisp Online
* In a Docker container
* Download and install from a release
* Building the sources
 * Maiko
 * Building loadups

## Interlisp Online

For the minimum amount of setup, the online version is a good starting place. [Interlisp Online](https://online.interlisp.org) provides access to a version of Medley running in the cloud. All that is needed to get started is a (updated) browser and a mouse. You can log in as a guest or -- if you want to save files or sessions -- create an account.

Sessions are preserved for an indefinite time (we haven't worked out for how long -- after 30 days of inactivity?). But it should be good for experimenting and introducing yourself to the environment. Anything you create in the online environment should be treated as transient. If you're interested in developing and experimenting with Lisp programs then you will want to investigate other options. But, for a first foray, this is a good starting place. The [Interlisp/online](https://github.com/Interlisp/online#readme) repository may have more details.

## Running with Docker

If you are already familiar with running Docker Desktop, this option may appeal. In addition to a running Docker Desktop, you will need either a VNC viewer (or X server). The VNC Viewer allows Windows to interact with the Medley instance running in Docker. It supports the windowing system and communicates your input.

The instructions for this configuration are located at [Running with Docker](running-with-docker).

Medley in Docker has a copy of the Medley system within the Docker container. Whenever you install a new version of the Medley Docker container you get a fresh system, all previous work is replaced by a vanilla image. This provides way of experimenting. Docker lets you mount directories on your local file system.

## Running Installed

For users of Linux, BSD, MacOS and recent Windows (with WSL2), installing and running a local copy is a little more complicated but has the most flexibility.

## Running in WSL2 (Windows)

For users of Windows 10 or 11 (pro), running in WSL2 is a good choice. This requires installing both Maiko, the underlying engine, and Medley. This option requires some familiarity with Linux and running Linux within Microsoft's WSL environment. In addition, if you aren't running Windows 11, you may need to install an X11 server within your Windows environment: two free servers that are known to work are [Cygwin/X](https://x.cygwin.com) and [XMing](http://www.straightrunning.com/XmingNotes/) (the 6.9 release is old but usable).

The instructions for installing Maiko and Medley can be found at [Running on Win](running-on-win).
