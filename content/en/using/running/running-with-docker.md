---
title: Running with Docker Desktop
weight: 50
type: docs
---


### **Running on Windows with Docker Desktop**

When running with Docker, Medley runs in a Docker container using the Interlisp/medley image found on Docker Hub.  A VNC Viewer window is used to display the Medley desktop.  All of this is started up using the single `medley` command.

These instructions are for Windows 10 or 11 (x86_64) only.


#### To install and run Medley with Docker Desktop:

1.  *Install Docker Desktop:*&nbsp;&nbsp;Install Docker Desktop for Windows as described [here](https://docs.docker.com/desktop/install/windows-install/).

2.  *Install Medley*:&nbsp;&nbsp;To install Medley, download and run the the `medley-install_<version>.exe` that can be found [here](https://online.interlisp.org/downloads/medley_downloads.html) under the Windows 10/11 heading. 

     This will install Medley on your system, by default in the `%USERPROFILE%/AppData/Local/Medley/Scripts` folder.  This folder will be added to your %PATH%.  An uninstall will also be added so that you can remove Medley via the standard Add/Remove Programs control panel.

    Notes: 
    * To download `medley-install_<version>.exe`, you may have to bypass any security concerns your browser has about downloading an .exe file.
    * You will have to bypass the Windows Defender protection against executing an unsigned .exe.  To do so, click `More info` followed by `Run Anyway` when the Windows Defender window pops up.

3.  *Run Medley:*&nbsp;&nbsp;Run Medley by typing `medley <flags and options>` into either a Command or a Powershell window.

    Documentation for the `<flags and options>` to the `medley` command can be found [here](https://online.interlisp.org/downloads/man_medley.html)

   	For first-time users: `medley --apps --interlisp --noscroll` or, equivalently, `medley -a -e -n` is a good starting point.  This will give you a fully populated Medley system, including some applications built on Medley such as Notecards and Rooms.


#### Notes:

*  Docker needs to be installed and *running* in order to run Medley.  However, the Docker Dashboard window does not be open.  You can check the state and start/stop Docker by right clicking on the Docker icon <img alt="Docker icon" height=15 width=15 src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK8AAAB+CAMAAABlLrHNAAAAY1BMVEUAAAD///+wsLDQ0NC/v7/r6+uioqLx8fEkJCQaGhrh4eFGRkZVVVW8vLwYGBj8/PxbW1tycnKqqqra2toRERHKyso3Nzd+fn5hYWGXl5doaGhMTEw8PDxBQUGNjY2GhoYwMDDd4iByAAAE4UlEQVR4nO2c69aqIBCGIQ8UHdSoTK30/q9ya7b7lIOMhUJr+f6chfZEMMwMEMJmtYo5PSKj70dG34bJHfGiRj/ANO924e1p4V14u1p4F96uFt6Ft6uF97d4i9/ixX7CKTP7ftO8OOJk+PXGeScWiDcKOJHGSnirtKnhDgbxhod1X3ENTOINZ22GasYb4/nzN7ITJr2H8V4wnhzJ36C8B0f878Ir0cr7KV6G0CP4HV4S1y2r88/wZm3bUuv83OAlp1fjVAfsBm/6bn0nP8BL13/Nk+EedoI37ba/Os8brXsPHF3nXXFPDLk10/HOB7xRwj1x+5I3ugoQDGNPMBZ1U/GraVetoOIfGcihQPEvDTk9f7E9ZzxSZdNBnYWvWKm/owP50EPgRQ9lYwd4xSGE1spVg+cNPE7NkxFvfP5elLc2np5ImzJZ05c4b9ZqBeQNitOmp0NeW0veeKkp6I23pnXThDc2XcXWh7711JlRwUnCq1zlON6z+HAE9mdIlb8dBeP97yNFP9MMCNWM43i9wxe8yvVC5N3+faQv40WqbMNV3rApZVBWi/ZKGK7ybst4e6maAkZ1KfLsTCJXeKXjV3x3vgrc4KUy/yDTOiQu8JINkLdep5kDvFgscat1dIBXEj8odXOAV4zP1HKhf4MLGHfDHODFJZg3dWG+NbUzoKhRXmX+Nhjv1MqBuKXgf6ngDJukTHwflfXKtW4aC1Yim1Fpv5dgS8ZdXC9w4Pd1fsbrnNFv43W+6TNelzZlsqadDxUTWpnqJNeFfIhl4iCS6ZlzWOWNAnYuZemQTHv85j2vLCjM0ryAxjrvjA7hKAM/Y083hv/z/gJu8k7nkDy8d0pxp0aE+GKbc9ruu8UTBB/xFnTYPRjuyTaRWps42zOhLmWbSqYtIURZ33FQyuJZwwvP9ubSbajC7SBvOYCLUWUbT9Dghgcak03Pot0QLkbQ2H42DW94oFT/hlm1G95ARmOqFXNoyJk1vGIuaFWnYVzn4rNQxwsrv86lu243FDGnFgxd92IUwJLTebTRn9+RbGbbk7Z76/wNXm2bXBrf2/JK9v1sydfi1rzUNuVbw5HDf15nQvYT5AQlku7nW5H60EOf15WCiX6ytbxj9jsmFGCytbyBeAbAgnIQ7rM+6UIIfAKNhpaXP69mQ5qwt8dLbMPy+xkaXvseTX0eSspre0CsmQ6zz0sru7yDJ1IlvJY9BGhh6/FaXTJG3TB67WdZrPLcRl2IevHam3HVuPs6L17JvUsncd/7m5bKJmvYrSGRF99s4G7G4v7x2kjjDrAYUsprIa+vRvdud38efirFkG7wVVjGO3deFEOuuw3xzuvTcnBIpuKdtRIxIsRR8s7nhC8fzDQJ76ijjF/ow7Eg8gpXeabQJvziyjd33ohMv72Vf+LGVLyTA1+giTCQF5NJh0T6kdMd4sXRdJPu+tVQUPBOFrwXgOvQH/Fiar4gcYg/drl6XhyZXjkSM7Tq85PkAT3XqFcBusn/HW8dXxqad/n+89VsDG/dx6udeNx6lKp8ZRJWw9tcLCzhh/fFnj1+77/G8TZi4XU88yV/eKb/KgjIW/cy9bMRHq7KQ59OAgvkbRV4YXotKvV5y6qI84dv9u9VBI07Dx4Ryjx/H2ZlmibPv3NN0iQts+Pe9xhVHiI0qH+feF7zFV+3XAAAAABJRU5ErkJggg=="> in the System Tray.

*  The first time it runs, `medley` will automatically pull the latest Interlisp/medley docker image from Docker Hub.  It will use this docker image for all subsequent runs unless the '--update' flag is raised.  When --update is raised, `medley` will once again pull the latest Interlisp/medley docker image.

*  When running with Docker, the Medley file system is "within" the Docker container.  This means it is deleted whenever Medley stops and is recreated whenever Medley restarts.  The exception is the directory `/home/medley/il` (in the Medley file system) which is automatically mapped by `medley` to a directory in the host Windows file system, by default to `%USERPROFILE%/AppData/Local/Medley/il` folder.  You can change this mapping to a different windows folder using the `--logindir` option to `medley`.

