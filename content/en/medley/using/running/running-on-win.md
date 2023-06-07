---
title: Running on Windows 10/11
weight: 40
type: docs
---
How is this different from the topic running on Docker Desktop?

Medley does not yet run as a native Windows application.  Besides [online](online), you can run Medley on Windows 10/11 using Windows System For Linux (WSL1 or WSL2).

This methods requires the installation (if not already installed) of one additional component to your Windows system - WSL.

On Windows, Medley requires a 64-bit machine.

### **Running on Windows with WSL**

Medley will run on either WSL1 or WSL2.  WSL2 is preferred, but for older machines that do not support virtualization (see [here](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements)) or Windows builds prior to Windows 10 Build 19041, WSL1 will work just fine although it will be limited to the VNC mode (see below).

When running under WSL2, Medley can display in one of two ways: in an X-Window (using the X_Windows server built-in to WSL2) or in a VNC-viewer Window.  Although the X-windows approach is simpler (i.e., behind the scenes) it does not scale well on high-DPI displays.  In VNC mode, the Medley window will scale according to the Windows Display Scale settings. The X vs Vnc mode is set on using the `--vnc` flag on the `medley` command line.  When running on WSL1, Vnc mode is always used.

#### To install an run Medley with WSL:

1.  *Install WSL:*&nbsp;&nbsp;See [here](https://learn.microsoft.com/en-us/windows/wsl/install) for instructions on installing WSL.

2.  *Install medley within WSL:*&nbsp;&nbsp;Once WSL is installed, open a terminal to WSL (e.g., by typing "wsl" in a command or powershell window) and follow the instructions for installing and running Medley on Linux that can be found [here](https://interlisp.org/running/running-on-linux/).

3.  *Run Medley:*&nbsp;&nbsp;Once Medley has been installed on WSL, you can run medley from either a WSL terminal as described in the Running Medley on Linux instructions ([here](https://interlisp.org/running/running-on-linux/)) or by typing `wsl medley <flags and options>` in a Command or Powershell window.

    Documentation for the `<flags and options>` to the `medley` command can be found [here](https://online.interlisp.org/downloads/man_medley.html)

   	For first-time users: `wsl medley --vnc --apps --interlisp --noscroll` or, equivalently, `wsl medley -v -a -e -n` is a good starting point.  This will give you a fully populated Medley system, including the applications built on Medley such as Notecards and Rooms.

#### Notes:

  *  If Medley for Docker (see below) is also installed on the system, you can also start Medley by typing `medley --wsl <distro> <flags and options>` in a Command or Powershell window.  This is equivalent to the `wsl medley <flags and options>` command described above.

### **Running on Windows with Docker Desktop**

When running with Docker, Medley runs in a Docker container using the Interlisp/medley image found on Docker Hub.  A VNC Viewer window is used to display the Medley desktop.  All of this is started up using the single `medley` command.

#### To install an run Medley with Docker Desktop:

1.  *Install Docker Desktop:*&nbsp;&nbsp;Install Docker Desktop for Windows as described [here](https://docs.docker.com/desktop/install/windows-install/).

2.  *Install Medley*:&nbsp;&nbsp;To install Medley, download and run the the `medley-install_<version>.exe` that can be found [here](https://online.interlisp.org/downloads/medley_downloads.html) under the Windows 10/11 heading. 

     This will install Medley on your system, by default in the `%USERPROFILE%/AppData/Local/Medley/Scripts` folder.  This folder will be added to your %PATH%.  An uninstall will also be added so that you can remove Medley via the standard Add/Remove Programs control panel.

    Note that to download `medley-install_<version>.exe`, you may have to bypass any security concerns your browser has about downloading an .exe file.  In addition, you will have to bypass the Windows Defender protection against executing an unsigned .exe.  To do so, click `More info` followed by `Run Anyway` when the Windows Defender window pops up.

3.  *Run Medley:*&nbsp;&nbsp;Once it is installed, you can run Medley by typing `medley <flags and options>` into either a Command or a Powershell window.

    Documentation for the `<flags and options>` to the `medley` command can be found [here](https://online.interlisp.org/downloads/man_medley.html)

   	For first-time users: `medley --apps --interlisp --noscroll` or, equivalently, `medley -a -e -n` is a good starting point.  This will give you a fully populated Medley system, including the applications built on Medley such as Notecards and Rooms.

#### Notes:

* Docker needs to be installed and *running* in order to run Medley.  However, the Docker Dashboard window does not be open.  You can check the state and start/stop Docker by right clicking on the Docker icon <img alt="Docker icon" height=15 width=15 src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK8AAAB+CAMAAABlLrHNAAAAY1BMVEUAAAD///+wsLDQ0NC/v7/r6+uioqLx8fEkJCQaGhrh4eFGRkZVVVW8vLwYGBj8/PxbW1tycnKqqqra2toRERHKyso3Nzd+fn5hYWGXl5doaGhMTEw8PDxBQUGNjY2GhoYwMDDd4iByAAAE4UlEQVR4nO2c69aqIBCGIQ8UHdSoTK30/q9ya7b7lIOMhUJr+f6chfZEMMwMEMJmtYo5PSKj70dG34bJHfGiRj/ANO924e1p4V14u1p4F96uFt6Ft6uF97d4i9/ixX7CKTP7ftO8OOJk+PXGeScWiDcKOJHGSnirtKnhDgbxhod1X3ENTOINZ22GasYb4/nzN7ITJr2H8V4wnhzJ36C8B0f878Ir0cr7KV6G0CP4HV4S1y2r88/wZm3bUuv83OAlp1fjVAfsBm/6bn0nP8BL13/Nk+EedoI37ba/Os8brXsPHF3nXXFPDLk10/HOB7xRwj1x+5I3ugoQDGNPMBZ1U/GraVetoOIfGcihQPEvDTk9f7E9ZzxSZdNBnYWvWKm/owP50EPgRQ9lYwd4xSGE1spVg+cNPE7NkxFvfP5elLc2np5ImzJZ05c4b9ZqBeQNitOmp0NeW0veeKkp6I23pnXThDc2XcXWh7711JlRwUnCq1zlON6z+HAE9mdIlb8dBeP97yNFP9MMCNWM43i9wxe8yvVC5N3+faQv40WqbMNV3rApZVBWi/ZKGK7ybst4e6maAkZ1KfLsTCJXeKXjV3x3vgrc4KUy/yDTOiQu8JINkLdep5kDvFgscat1dIBXEj8odXOAV4zP1HKhf4MLGHfDHODFJZg3dWG+NbUzoKhRXmX+Nhjv1MqBuKXgf6ngDJukTHwflfXKtW4aC1Yim1Fpv5dgS8ZdXC9w4Pd1fsbrnNFv43W+6TNelzZlsqadDxUTWpnqJNeFfIhl4iCS6ZlzWOWNAnYuZemQTHv85j2vLCjM0ryAxjrvjA7hKAM/Y083hv/z/gJu8k7nkDy8d0pxp0aE+GKbc9ruu8UTBB/xFnTYPRjuyTaRWps42zOhLmWbSqYtIURZ33FQyuJZwwvP9ubSbajC7SBvOYCLUWUbT9Dghgcak03Pot0QLkbQ2H42DW94oFT/hlm1G95ARmOqFXNoyJk1vGIuaFWnYVzn4rNQxwsrv86lu243FDGnFgxd92IUwJLTebTRn9+RbGbbk7Z76/wNXm2bXBrf2/JK9v1sydfi1rzUNuVbw5HDf15nQvYT5AQlku7nW5H60EOf15WCiX6ytbxj9jsmFGCytbyBeAbAgnIQ7rM+6UIIfAKNhpaXP69mQ5qwt8dLbMPy+xkaXvseTX0eSspre0CsmQ6zz0sru7yDJ1IlvJY9BGhh6/FaXTJG3TB67WdZrPLcRl2IevHam3HVuPs6L17JvUsncd/7m5bKJmvYrSGRF99s4G7G4v7x2kjjDrAYUsprIa+vRvdud38efirFkG7wVVjGO3deFEOuuw3xzuvTcnBIpuKdtRIxIsRR8s7nhC8fzDQJ76ijjF/ow7Eg8gpXeabQJvziyjd33ohMv72Vf+LGVLyTA1+giTCQF5NJh0T6kdMd4sXRdJPu+tVQUPBOFrwXgOvQH/Fiar4gcYg/drl6XhyZXjkSM7Tq85PkAT3XqFcBusn/HW8dXxqad/n+89VsDG/dx6udeNx6lKp8ZRJWw9tcLCzhh/fFnj1+77/G8TZi4XU88yV/eKb/KgjIW/cy9bMRHq7KQ59OAgvkbRV4YXotKvV5y6qI84dv9u9VBI07Dx4Ryjx/H2ZlmibPv3NN0iQts+Pe9xhVHiI0qH+feF7zFV+3XAAAAABJRU5ErkJggg=="> in the System Tray.

* The first time it runs, `medley` will automatically pull the latest Interlisp/medley docker image from Docker Hub.  It will use this docker image for all subsequent runs unless the '--update' flag is raised.  When --update is raised, `medley` will once again pull the latest Interlisp/medley docker image.

* When running with Docker, the Medley file system is for the most part "within" the Docker container.  This means that it is deleted whenever Medley stops and is recreated whenever Medley restarts.  The exception is the directory `/home/medley/il` (in the Medley file system) which is automatically mapped by `medley` to a directory in the host Windows file system, by default to `%USERPROFILE%/AppData/Local/Medley/il` folder.  You can change this mapping to a different windows folder using the `--logindir` option to `medley`.
