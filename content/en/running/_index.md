---
title: Running Medley Interlisp
weight: 30
type: docs
---

*DRAFT -- This page is currently being revised.*


There are different ways of running Medley Interlisp, depending on your platform (Mac, Windows, Linux, other) and related factors.

* Interlisp Online
* In a Docker container
* Download and install from a release
* (re)build the virtual machine emulator (Maiko) from sources
* (Re) build your own Lisp image

## Interlisp Online

For the minimum amount of setup, the online version is a good starting place. [Interlisp Online](https://online.interlisp.org) provides access to a version of Medley running in the cloud. All that is needed to get started is a (recent) browser and a mouse. You can log in as a guest or -- if you want to save files or sessions -- create an account.

Sessions are preserved between sessions, but will be removed after 30 days of inactivity). Online should be good for experimenting and introducing yourself to the environment. The online site also provides a way of copying files to and from your account's files.

HOWEVER: anything you create in the online environment should be treated as transient. If you're interested in developing and experimenting with Lisp programs then you will want to investigate other options. But, for a first foray, this is a good starting place. The [Interlisp/online](https://github.com/Interlisp/online#readme) repository may have more details.

2. Running with Docker Desktop

If you are already familiar with running Docker Desktop, this option may appeal. In addition to a running Docker Desktop, you will need either a VNC viewer (or a windows X server). The VNC Viewer allows you to interact with the Medley instance running in Docker (Interlisp Online uses a browser-based VNC viewer.)

The instructions for this configuration are located at [Running with Docker](running-with-docker).

Medley in Docker has a copy of the Medley system within the Docker container. Whenever you install a new version of the Medley Docker container you get a fresh system (any previous changes would be lost.) Docker lets you mount directories on your local file system.

## Running Installed

For users of Linux, BSD, MacOS and Windows (with WSL2), installing and running a local copy is a little more complicated but has the most flexibility.

Medley (maiko) currently requires having an X-server installed -- which one to use depends on your platform.

We use GitHub Actions workflow automation to build Maiko for different platforms; if your platform isn't in the mix you may need to [download maiko sources and make and install those binaries](https://github.com/Interlisp/maiko/#readme).

## Developing Medley Interlisp itself

This process isn't well documented yet.
The scripts "scripts/loadup*" in the github/interlisp/medley/ repository are used. See README.md files in the GitHub repo.

