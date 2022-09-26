---
title: Running Medley Interlisp
weight: 30
type: docs
---

There are different ways of running Medley Interlisp on a wide variety of systems.  This section lays out the basics to help you choose:

* Interlisp Online
* In a Docker container
* Download and install from a release
* (re)build the virtual machine emulator (Maiko) from sources, run in a release.
* (Re) build your own Lisp image

A note about performance:  Modern systems are thousands of times faster than the D-machines of 1980s. The system was designed for limited memory machines, so 32 MB is quite roomy. The Medley VM is now quite portable to many different OS and CPU configurations.

## Interlisp Online

For a minimum amount of setup, the online version is a good starting place. [Interlisp Online](https://online.interlisp.org) provides access to a version of Medley running in the cloud. All that is needed to get started is a (recent) browser and a mouse. You can log in as a guest or -- if you want to save files or sessions -- create an account.

Sessions and files are preserved between sessions, but will be removed after 30 days of inactivity. While you are connected to your session, you can access your files using sftp. Online should be good for experimenting and introducing yourself to the environment.

Pros: Sandbox environment -- it's all done with Docker and VMs so just modify anything you want. 
Cons: Requires a good Internet connection to run. No access to files in your file system (also a pro). Anything you create in the online environment should be treated as transient. 

See [Running Online](online) for more.

2. Running with Docker Desktop

This is a little like running online except you're connecting to your own Medley service. If you are familiar with running Docker Desktop, this option may appeal. In addition to a running Docker Desktop, you will need either a VNC viewer (or a windows X server). The VNC Viewer allows you to interact with the Medley instance running in Docker (Interlisp Online uses a browser-based VNC viewer.)

Medley in Docker has a copy of the Medley system within the Docker container. Whenever you install a new version of the Medley Docker container you get a fresh system. 

Pro: You can mount parts or all of your local file system, for easy file sharing, but at the same time you can restrict system access. Your files are on your own system, no live Internet capability needed.
Con: We're only building X86_64 docker containers regularly.

The instructions for this configuration are located at [Running with Docker](running-with-docker).

## Running Installed

For users of Linux, BSD, MacOS and Windows (with WSL2), installing and running a local copy is a little more complicated but has the most flexibility. You need to know a bit more about how Medley Interlisp works. The system comes in two parts: a C program (code name maiko, binaries lde, ldex) that emulates the virtual Lisp machine, and the rest of the system written in Lisp.

Maiko currently requires having an X-server installed; which one to use depends on your platform.

We use GitHub Actions workflow automation to build Maiko for different platforms; if your platform isn't in the mix you may need to [download maiko sources and make and install those binaries](https://github.com/Interlisp/maiko/#readme).

## Developing Medley Interlisp itself

The scripts "scripts/loadup*" in the github/interlisp/medley/ repository are used. See README.md files in the GitHub repo. 

