---
title: Install and Run on Windows with WSL
weight: 20
type: docs
---

Medley on WSL involves installing and maintaining the WSL subsystem within Windows. When installing and using Medley on WSL, you are working within Linux. Some familiarity with Linux and the Linux command line is helpful.  

Medley on WSL is best for users who are running WSL anyway and/or prefer working in a Linux environment. Medley sees the WSL file system, and Windows files appear under `/mnt/c/`, e.g., Windows download will be in `/mnt/c/Users/yourname/Downloads`.

Medley will run on either WSL1 or WSL2.  WSL2 is preferred, but for older machines that do not support virtualization (see
[here](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements))
or Windows builds prior to Windows 10 Build 19041, WSL1 will work just fine although it will be limited to the VNC mode (see below).

For WSL installations, the browser(s) on the Windows side will suffice.

There are release configurations for Debian-based systems; i.e., systems that support dpkg), including Debian-based distros on WSL.

In the [Medley downloads site](https://online.interlisp.org/downloads/medley_downloads.html) get the release asset for WSL and your host machine type (X86_64, ARM64, ARMv7).

The WSL packages differ only in
that they include an additional functionality to have Medley display in a VNC Window
instead of a standard X Window.  This is useful on high resolution displays since
the VNC window will scale according to the Windows Settings->Display->Scale setting,
while the X Window on WSL will not so scale. The WSL packages also install the wslu
package, which is used by Medley to connect to external browsers as described above.
Aside from these two features, a non-WSL .deb package will install and run on WSL.

## Accessing Medley for WSL

1. Use a browser to download from the .deb package for your platform (i.e., "standard" WSL) and your machine architecture (X86_64, ARM64, or ARMv7) to `<deb_filepath>` from [the Medley downloads site](https://online.interlisp.org/downloads/medley_downloads.html)  
 `<deb_filepath>` will depend on whether the browser was started in Windows or in WSL:

* If downloading to the standard Downloads folder, using a WSL-based browser `<deb_filepath>` will be in `~/Downloads`.

  * If using a Windows-based browser, `<deb_filepath>` will be in `/mnt/c/Users/<username>/Downloads`.
