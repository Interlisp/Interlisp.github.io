---
title: Running on Windows 10/11
weight: 40
type: docs
aliases:
 - /hugo/running/running-on-win/
---

There are three ways to run Medley on Windows:
 1.  Use Medley Online within your browser 
 2.  Run Medley on Windows System for Linux (WSL)
 3.  Run the 'native' Medley Windows app (which uses cygwin behind the scenes)

These three ways result in (nearly) identical Medley experiences, but differ in the if and how Medley is installed and run.

Medley Online requires nothing to be installed on your local machine.  Instead, Medley is run in the cloud and accessed from a browser running on Windows.  Medley Online is best from users wanting to try Medley out without having to install anything on Windows.  It is not well-suited to significant software development using Medley. 

Medley on WSL involves installing and maintaining the WSL subsystem within Windows. And when installing and using Medley on WSL you are working within Linux. Some familiarity with Linux and the Linux command line is helpful.  Medley on WSL is best for users who are running WSL anyway and/or prefer working in a Linux environment.

Medley 'native' works within the ordinary Windows environment. Installation uses standard Windows installer and you start Medley from a standard Command (or Powershell) window.  Medley 'native' is best for users who prefer to stay (almost) exclusively in the Windows environment.
 
Medley on WSL and 'native' Medley both require 64-bit Windows 10/11.  Medley Online will run on any Windows, providing that the browser is up-to-date..


### **Running Medley Online**

Instructions on running Medley Online can be found [here](https://interlisp.org/medley/using/running/online/).


### **Running on Windows with WSL**

Medley will run on either WSL1 or WSL2.  WSL2 is preferred, but for older machines that do not support virtualization (see [here](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements)) or Windows builds prior to Windows 10 Build 19041, WSL1 will work just fine although it will be limited to the VNC mode (see below).

When running under WSL2, Medley can display in one of two ways: in an X-Window (using the X Windows server built-in to WSL2) or in a VNC-viewer Window.  Although the X-windows approach is simpler (i.e., behind the scenes), it does not scale well on high-DPI displays.  In VNC mode, the Medley window will scale according to the Windows Display Scale settings.  VNC mode is set using the `--vnc` flag on the `medley` command line.  In the absence of the --vnc flag,  X Windows mode will be used.  When running on WSL1, VNC mode is always used.

#### To install and run Medley with WSL

1. *Install WSL:* See [here](https://learn.microsoft.com/en-us/windows/wsl/install) for instructions on installing WSL.

2. *Install medley within WSL:* Once WSL is installed, open a terminal to WSL (e.g., by typing "wsl" in a command or powershell window) and follow the instructions for installing and running Medley on WSL and standard Linux that can be found [here](/medley/using/running/running-on-linux). 

3. *Run Medley:* Once Medley has been installed on WSL, you can run medley from either a WSL terminal as described in the Running Medley on Linux instructions ([here](/medley/using/running/running-on-linux)) or by typing `wsl medley <flags and options>` in a Command or Powershell window.

    Documentation for the `<flags and options>` to the `medley` command can be found [here](https://online.interlisp.org/downloads/man_medley.html)

    For first-time users: `wsl medley --vnc --apps --interlisp --noscroll` or, equivalently, `wsl medley -v -a -e -n` is a good starting point.  This will give you a fully populated Medley system, including the applications built on Medley such as Notecards and Rooms.


### **Running on Windows 'natively'**

When running on Windows 'natively', Medley will be installed into a directory (of your choice).  This directory will contain an isolated copy of the Cygwin environment and a version of Medley that runs within that specific Cygwin environment.  This complexity, however, is largely hidden from the user and Medley behaves as if it is a native Windows app.

#### To install and run Medley 'native'

1. Download the Medley Windows installer from under the Windows 10/11 heading [here](https://online.interlisp.org/downloads/medley_downloads.html).

2. Start the Medley installation app (e.g., by double clicking on the .exe just downloaded.

     The installation app will ask for the directory in which to install Medley.  Any directory that you have read/write access to will suffice.

    The installation app will then copy the Medley files into the specified directory. It will also run the Cygwin installer to install Cygwin into the specified directory as well.
    

     This will install Medley on your system, by default in the `%USERPROFILE%/AppData/Local/Medley/Scripts` folder.  This folder will be added to your %PATH%.  An uninstall will also be added so that you can remove Medley via the standard Add/Remove Programs control panel.

    Note that to download `medley-install_<version>.exe`, you may have to bypass any security concerns your browser has about downloading an .exe file.  In addition, you will have to bypass the Windows Defender protection against executing an unsigned .exe.  To do so, click `More info` followed by `Run Anyway` when the Windows Defender window pops up.

4. *Run Medley:* Once it is installed, you can run Medley by typing `medley <flags and options>` into either a Command or a Powershell window.

    Documentation for the `<flags and options>` to the `medley` command can be found [here](https://online.interlisp.org/downloads/man_medley.html)

    For first-time users: `medley --apps --interlisp --noscroll` or, equivalently, `medley -a -e -n` is a good starting point.  This will give you a fully populated Medley system, including the applications built on Medley such as Notecards and Rooms.

#### Notes


