---
title: Install and Run on Linux
weight: 20
type: docs
---

Medley runs on most any Linux system that includes X Windows.

Note that for Windows users of System For Linux (WSL) on Windows 11 and Windows 10 Build 19044+, there are [separate instructions](./running-on-wsl).

We recommend the Linux system have a web browser installed. 
A browser is not strictly necessary to run Medley, but several features of the system (e.g., displaying some user documentation) will not work without an external browser installed.

Medley can be installed on your Linux system in one of two configurations: *standard* and *local*.

* Standard installation will install Medley into system directories and install any prerequisite packages.  
* Local installation will install Medley into any user directory but any prerequisite packages must be installed manually.

## **Standard Installation \(Debian-based systems only\)**

We are currently only building standard installations for Debian-based systems (i.e., systems that support dpkg).

In a standard Linux installation, Medley is installed in system directories
under /usr/local/interlisp. Man pages and (links to) the medley executable are also installed in standard system locations (e.g., /usr/local/man and /usr/local/bin).

Standard installations are ideal for users who want to explore Medley (including its system code) or to develop applications built on top of Medley.  Standard installations are not good for users who want to modify the Medley system code, since that code is installed in protected locations.

Standard installation uses `apt` to install a .deb package downloaded from
the [Medley downloads site](https://online.interlisp.org/downloads/medley_downloads.html).
The .deb package will install Medley as well as any other packages needed for Medley to run.

## Accessing Medley

1.  Use a browser to download from the .deb package for your platform (i.e., "standard" Linux or WSL) and your machine 	architecture (X86_64, ARM64, or ARMv7) to `<deb_filepath>` from [the Medley downloads site](https://online.interlisp.org/downloads/medley_downloads.html)
	
2.  Enter the following in a terminal to install the download:

	```bash
	ubuntu@oio:~$ sudo apt update
	ubuntu@oio:~$ sudo apt install -y <deb_filepath>
	```

3.  Enter the following in a terminal to run medley:
	
	```bash
	ubuntu@oio:~$ medley
	```

	There are many options to the `medley` command.  For a brief overview, run `medley --help`.
	For a more complete description, run `man medley` or `medley --man` or click
        [here](https://online.interlisp.org/downloads/man_medley.html).

	For first-time users: `medley --apps` or for WSL `medley --apps --vnc` is a good starting
	point.  This will give you a fully populated Medley system, including the applications built on Medley such as Notecards and Rooms.

#### Notes:

* By default, `medley` will create a directory in *$HOME/il*.  This will be used by the Medley
	system as its *LOGINDIR*.  Medley will start up with *LOGINDIR* as its current connected directory.
	It will load the personal init file (if any) from *LOGINDIR*/INIT or *LOGINDIR*/INIT.LCOM.  Finally,
	Medley will use *LOGINDIR*/vmem/ to store its virtual memory file(s).  The location of *LOGINDIR*
	can be changed using the `--logindir` option to `medley`.

### **Local Installation**

In a local installation, the Medley system is installed into any user directory from a .tar file.
Multiple "Medleys" can be installed in different directories on one machine without interference
(except see description of Medley *LOGINDIR* below).  Local installation makes it easy (from a file
management p.o.v.) to modify the Medley system code.

Local installation doesn't involve a package manager, so you are responsible for installing any
prerequisite packages onto your system before you install Medley.

Also note that with local installations, `man medley` will not work.  However, as indicated below,
`./medley --man` will show the medley man page.

#### To install and run Medley locally:

1.  Install prerequite packages

    * For non-WSL installations, use your distro's package manager to install `xdg-utils`.

    * For WSL all installations, use your distro's package manager to install `wslu`.

         Note that some distros do not include `wslu` in their standard repos. See
         [https://wslutiliti.es/wslu/install.html](https://wslutiliti.es/wslu/install.html)
         for installation instructions if this is the case.

         Also note that `wslu v4.0` does not work with Medley, so you will need to install
         either a version < v.40 or >= v4.1.


    * For WSL installations where the VNC feature will be used, install the `tigervnc-standalone-server` and `tigervnc-xorg-extension` packages.

      When using the VNC feature Medley will display in a VNC Window instead of a standard X Window.
      This is useful on high resolution displays since the VNC window will scale according to the
      Windows Settings->Display->Scale setting, while the X Window on WSL will not so scale.

      Note that Medley will install and run even if none of these prerequite packages are installed.
      However, some features (e.g., viewing documentation in an external browser) will be inoperable.

2.  Download

	Using a browser download from
	[the Medley downloads site](https://online.interlisp.org/downloads/medley_downloads.html)
	the tar (.tgz) file for your platform (i.e., "standard" Linux or WSL) and your machine
	architecture (X86_64, ARM64, or ARMv7) to `<tar_filepath>`.

    Note that on WSL, `<tar_filepath>` will depend on whether the browser was started in Windows or in WSL.  If downloading to the standard Downloads folder, using a WSL-based browser `<tar_filepath>` will be in `~/Downloads`.  If using a Windows-based browser, `<tar_filepath>` will be in `/mnt/c/Users/<username>/Downloads`.


3. Install Medley

	In a terminal:

	```
	ubuntu@oio:~$ mkdir <interlisp_directory>
	ubuntu@oio:~$ tar -C <interlisp_directory> -xzf <tar_filepath>
	```

4. Run Medley

	In a terminal:

	```
	ubuntu@oio:~$ cd <interlisp_directory>/medley
	ubuntu@oio:~$ ./medley
	```

	There are many options to the `medley` command.  For a brief overview, run `./medley --help`.
	For a more complete description, run `./medley --man` or click
        [here](https://online.interlisp.org/downloads/man_medley.html).

	For first-time users: `./medley --apps` or for WSL (and you have installed the VNC prerequisites)
	`./medley --apps --vnc` is a good starting point.  This will give you a fully populated Medley system,
	including the applications built on Medley such as Notecards and Rooms.

#### Notes:

* By default, `medley` will create a directory in *$HOME/il*.  This will be used by the Medley
	system as its *LOGINDIR*.  Medley will start up *LOGINDIR* as its current connected directory.
	It will load any personal init file from *LOGINDIR*/INIT or *LOGINDIR*/INIT.LCOM.  Finally,
	Medley will use *LOGINDIR*/vmem/ to store its virtual memory file(s).  The location of *LOGINDIR*
	can be changed using the `--logindir` option to `medley`.  In particular, if you have multiple
	installations of Medley that you would like to keep completely separate, then you can use the 
	`--logindir -` option, which will set *LOGINDIR* to \<medley_directory\>/logindir.
