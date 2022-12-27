---
title: Running on Windows
weight: 50
type: docs
---
## Running on Windows

Medley currently does not run natively on Windows.  We provide two methods of running
Medley with Windows.  Both methods require familarity with installing and configuring
advanced Windows options.  If you are uncomfortable with running Linux on Windows
using WSL2 or installing and using Docker and running Docker Containers, you
may want to use the Online web-based version.

## Running Medley in the Linx Subsystem

This section will explain how to setup Medley within Linux on a Windows system
using WSL2.

### Prerequistes

- WSL2 installed.  [Install Linux on Windows with WSL](https://learn.microsoft.com/en-us/windows/wsl/install) by Microsoft provides directions on how to install or upgrade your WSL2 installation.
- An installed Linux distribution.  There are many different available Linux distributions, Ubuntu is a widely used distribution.  [Install Ubuntu on WSL2 and get started with graphical applications](https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-11-with-gui-support#1-overview) provides a good set of instructions for installing a distribution and valiating that the graphics display works properly for Windows.

Once you have a working Linux distribution installed and working you're ready to install
the Medley environment.

It however, can easily be run using WSL2
and Linux.





* Interlisp Online seems to works fine with recent Edge and Chrome; we've tested others but don't regularly use them.
WARNING: Window/Chrome and Edge use keystrokes (control-W for example) that conflict with Medley use.

* Docker Desktop is a great possibility, too, if your system can run it.
* Otherwise, to run installed, you either need
    * WSLg (available with Windows 11) OR
    * WsL2 A running X-server installed on your machine

WsL stands for "Windows Subsystem for Linux". It's like docker but a little more integrated (You can get at your linux files from windows and your windows files from linux).    

## Running on Windows with WSL2

For users of Windows 10 or 11 (pro), running in WSL2 is a good choice. This requires installing both Maiko, the underlying engine, and Medley. This option requires at least a little familiarity with Linux and running Linux within Microsoft's WSL environment.

### X Server selection

The X11 protocol was invented quite a while ago (inspired by Warren Teitelman and Bob Sproull's Alto Display protocol as part of early Interlisp window system work.)

With X11, the notion of "client" and "server" are reversed. The software you run to manage the display and windows is the "server", and the thing far away which is running with access to files and doing the work is the "client".

When you run WSL it's like you have two (or more) computers in one box, where one is running windows and the other(s) are running Linux. The linux side(s) have their own Internet Protocol address. 

The thing that hooks them together is the "DISPLAY" variable in the linux side has the address of the "client".

There have apparently been some (mainly unsuccessful) attempts to simplify this for windows 11 users.

If you're running Windows 10, you will also need to install an X11 server within your Windows environment. There are different servers with varying capabilities and problems.

* [Cygwin/X](https://x.cygwin.com)
* [XMing](http://www.straightrunning.com/XmingNotes/) (the 6.9 release is old but usable).
* X410 (in the Microsoft Store, $40) -- useful uses windows sockets.
   https://x410.dev/cookbook/wsl/using-x410-with-wsl2#vsock
     - [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
* GWSL from Microsoft store
* install Xvnc and [TightVNC Version 2.8.63 or higher](https://www.tightvnc.com/download.php)

### X Server and Windows and Monitor sleep

If your windows system or monitor don't sleep by the schedule, there is a [WSLg problem](https://github.com/microsoft/wslg/issues/380) that they didn't want your Windows machine to fall asleep when watching a Linux-side video. If this turns out to be a problem, set your IDLE.PROFILE to TIMEOUT (to run a "screen saver") and then LOGOUT later.

## Requirements
 - Windows 10 *or* Windows 11
 - Windows Subsystem for Linux Enabled.  [Installing WSL](https://docs.microsoft.com/en-us/windows/wsl/install).
 - An installed Linux distribution.  The following distros have been tested:
   - [Pengwin Linux Distro](https://www.microsoft.com/store/apps/9NV1GV1PXZ6P)
   - [Ubuntu Linux Distro](https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6)

### Installing Medley via an Install script

*tbd*

### Manual Installation of Medley

The [medley repo README](https://github.com/Interlisp/medley#readme) has a guide for downloading or building your own maiko (for your OS / architecture) and for obtaining Medley
