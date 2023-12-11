---
title: Install and Run on MacOS
weight: 30
type: docs
aliases:
  - /running/running-on-mac
---
<style>.td-content blockquote { border-left: none; color: inherit; padding-left: 2rem;}</style>

## **Prerequisite: Install XQuartz**

Before installing and running Medley on your Mac, you will need to download and install XQuartz - an open-source X11 Windows server for the Mac.  You can download the latest XQuartz .pkg from  [XQuartz.org](https://xquartz.org) and install it using the MacOS installer.

If you do not have a three-button mouse on your Mac, you will need to set `Emulate three button mouse` in the XQuartz preferences.        

>To do so, start XQuartz (e.g., by double clicking the XQuartz icon within Launchpad). Select XQuartz->Preferences from the menu bar. In the Preferences dialog, select the Input tab and then check the *Emulate three button mouse* option.

## **Install Medley**

Medley releases on MacOS are distributed as a .zip file.  The .zip file contains universal binaries so that the same file can be used for either Intel or Apple Silicon machines.

To install Medley:

1. Download the latest release .zip from the Medley latest releases page [(here)](https://online.interlisp.org/downloads/medley_downloads.html) , under the heading "MacOS ...".

	>You can also download the latest release .zip as well as any prior release .zips from the Medley GitHub site [(here)](https://github.com/Interlisp/medley/releases).  In the Assets for any given release, the MacOS .zip file will be entitled *medley-full-macos-universal...zip*

2.  Drag the downloaded *medley-full-macos-universal...zip* file (which MacOS treats as an unzipped folder) from the Downloads folder into any folder of your choosing.  For the purposes of these instructions, we will call this the *\<install_folder>*.  And the file/folder just dragged into the \<install_foler>, we will call the *\<medley_folder>*.
    >You may also want to rename the \<medley_folder> from *medley-full-macos-universal...* to something more manageable - e.g., *medley-latest*.

4. In a Terminal window, you will need to remove the quarantine attributes from the executable files by executing the following command:
`xattr -d com.apple.quarantine <install_folder>/<medley_folder>/maiko/darwin.universal/lde*`

    For example: 
```
ssd@Mac-mini ~ % xattr -d com.apple.quarantine ~/il/medley-latest/maiko/darwin.universal/lde*
```

	
## **Run Medley**

On MacOS, Medley must be started from a Terminal window.

At the Terminal prompt, you need to execute the  command `<install_folder>/<medley_folder>/medley/medley`.  
>Note: it is usually easiest to first `cd \<install_folder>/\<medley_folder>/medley` and then just execute `./medley`

For example: 
```
ssd@Mac-mini ~ % cd ~/il/medley-latest/medley
ssd@Mac-mini medley % ./medley -a -e -n
```

Note that the first time you run it, Medley may take 10-15 seconds to start up as it starts the XQuartz X Windows server (assuming that it is not already running).
>You can optionally start the XQuartz server manually before starting Medley.  It will take 10-15 seconds to start up and then display an Xterm window in the upper-left corner of the screen.  You can just close this Xterm window.

There are many options to the `medley` command.  For a brief overview, run `./medley --help`. For a more complete description, run `./medley --man` or click
        [here](https://online.interlisp.org/downloads/man_medley.html).

For first-time users: `./medley -a -e -n` is a good starting	point.  This will give you a fully populated Medley system, including the applications built on Medley such as Notecards and Rooms.  It will start with a Interlisp Exec window (instead of the Xerox Common Lisp Exec window).

#### Notes:

>By default, `medley` will create a directory in *$HOME/il*.  This will be used by the Medley system as its *LOGINDIR*.  Medley will start up with *LOGINDIR* as its current connected directory. 	It will load the personal init file (if any) from *LOGINDIR*/INIT or *LOGINDIR*/INIT.LCOM.  Finally,  Medley will use *LOGINDIR*/vmem/ to store its virtual memory file(s).  The location of *LOGINDIR* can be changed using the `--logindir` option to `medley`.	





