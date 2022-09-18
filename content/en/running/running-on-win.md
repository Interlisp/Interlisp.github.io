---
title: Running on Windows
weight: 50
type: docs
---
## Running on Windows

* Interlisp Online works fine with Edge and Chrome; we've tested others but don't regularly use
* Docker Desktop is a great possibility, too.


## Running on Windows with WSL2 (Windows Subsystem for Linux)

We hope there will be a way of running Medley Interlisp with direct support of WIndows, but not so far.

However, if you have Windows 10 or Windows 11 pro, WSL2 is the way to go.

If you have Windows 11 Pro, WSL

https://x410.dev/cookbook/wsl/using-x410-with-wsl2#vsock

For users of Windows 10 or 11 (pro), running in WSL2 is a good choice. This requires installing both Maiko, the underlying engine, and Medley. This option requires some familiarity with Linux and running Linux within Microsoft's WSL environment. In addition, if you aren't running Windows 11, you may need to install an X11 server within your Windows environment: two free servers that are known to work are [Cygwin/X](https://x.cygwin.com) and [XMing](http://www.straightrunning.com/XmingNotes/) (the 6.9 release is old but usable).

## Requirements
 - Windows 10 *or* Windows 11
 - Windows Subsystem for Linux Enabled.  [Installing WSL](https://docs.microsoft.com/en-us/windows/wsl/install).
 - An installed Linux distribution.  The following distros have been tested:
   - [Pengwin Linux Distro](https://www.microsoft.com/store/apps/9NV1GV1PXZ6P)
   - [Ubuntu Linux Distro](https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6)
 - Windows 10 Additional Requirements
   - An X Server installed and running in Windows.  The following X Servers have been tested:
     - [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
     - GWSL from Microsoft store
     - install Xvnc and [TightVNC Version 2.8.63 or higher](https://www.tightvnc.com/download.php)

### Installing Medley via an Install script

*tbd*

### Manual Installation of Medley

The [medley repo README](https://github.com/Interlisp/medley#readme) has a guide for downloading or building your own maiko (for your OS / architecture) and for obtaining Medley
