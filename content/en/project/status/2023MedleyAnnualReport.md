---
title: 2023 Annual Report
weight: 8
type: docs
aliases:
 - /news/2023medleyannualreport/
 - /project/news/2023medleyannualreport/
---

<img src="/Resources/logo_red_no_border_568x385.png" width="284" height="194"></img>

### **Overview**

The Medley Interlisp Project has made significant progress toward its goals of preserving, extending, and documenting the “experience” of Interlisp for now and for the future. This annual report highlights our achievements and ongoing efforts.

### **Key Accomplishments**

We’ve structured our work around project objectives: lower barriers to entry, adapt to modern environments and user expectations, complete “work in progress”, demonstrate applications built in and for the system.

#### **Lower Barriers to Entry**

We want to allow newcomers to experience the system and ease of use without complex setup and configuration, so that more individuals can participate.

* **Online.Interlisp.org:** The online.interlisp.org site provides a quick and easy way for interested users to try Medley without any installation or setup. It enables any user to run the full Medley experience within the context of their browser.

In 2023, we improved the initial version of online.interlisp.org and began to attract a user base. Between 11/15/2022 and one year later: 187 users registered on the site, leading to 1522 unique Medley sessions. Unregistered users (i.e., guest logins) accounted for an additional 1971 unique Medley sessions.

* **Historical Interlisp Online:** As an extension to online.interlisp.org, we have implemented a proof of concept that runs historical versions of Interlisp (Harmony, Intermezzo, Koto, etc.) in a manner similar to the Medley sessions. This proof of concept is based on the Xerox Dandelion emulator (named DarkStar) developed by the (now closed) Living Computer Museum in Seattle. Our intention is to move this project from proof of concept to full implementation in the next year.
* **Running in the browser:** Recently, we have been exploring the possibility of using recent advancements in the “Web Assembly” emulator to run Medley locally in a browser. There remain significant issues we will need to address, but this is a very promising direction.

**Platforms, Releases, Builds, Automation, Installers**

* **Support for SDL2:** We added to Medley support for SDL2 which can now be built from source. Further work is needed to provide appropriate binaries in the software releases. The SDL2 backend is useful for running Medley on operating systems where X-Windows is not directly available, such as Windows, or which, being based on Wayland, may degrade the performance of X-Windows applications like Medley. Examples of the latter are Raspberry Pi OS Bookworm and later and ChromeOS.
* **Support for running ‘natively’ on Windows:** Previously, the only way to run Medley on Windows was via the Medley Docker container or via Windows System for Linux. Both of these require significant setup and expertise that are not common for Windows users. This year, we developed ‘native’ Windows support for Medley (based on Cygwin and SDL2) that is much more compatible with the ordinary setup and practices of Windows users.
* **Better Support for AArch64:** We extended the build scripts of the Maiko virtual machine to compile and run Medley on the AArch64 platform under Raspberry Pi OS Bookworm and later. Now Maiko can generate loadups on this platform too.
* **Build and Release Automation**: We completed the task of automating in GitHub Actions the build and release process for all major components of Medley including Maiko, Medley, Notecards and Online. These automations were synchronized, to the extent possible with the corresponding manual build, loadup and release tasks. Automated releases were set to run Weekly.
* **Installers for Major Platforms:** Previously, installing Medley on most platforms was a multi-step task, often requiring some degree of experience with various of the platforms’ administrative tools. We developed ‘single step’ installers for MacOS, Windows (native), Windows running WSL, Debian-based Linux, and for other Linux distros. This makes the task of installing Medley straightforward for users who want to quickly and easily explore Medley.
* **New Startup Script**: We developed a new, more comprehensive script for starting up Medley on all platforms. The script includes embedded documentation. It makes the task of configuring, starting up and managing Medley instances clearer and more straightforward in most circumstances.
* **Revamp ‘Loadup’ Scripts:** Loadup is the process of building a new image/release of the Medley Lisp code. We revamped the scripts that run the loadup process to make them more internally consistent, easier to maintain and to synchronize them with the automated loadups in our GitHub Actions for building releases. The load process was not fundamentally changed.

#### **Medley Tool Enhancements**

While Medley had support for Common Lisp constructs, the extension of Interlisp tools to the use of what evolved as the standard for Lisp – “Common Lisp” – was incomplete. Our goal has been that Medley tools should work as well or better than they did for Interlisp alone. This was work “in progress” in the 1990s, but it wasn’t complete and somewhat buggy. Some notable additions were implemented.

* **HELPSYS extended:** HELPSYS is the Interlisp tool which looks up and displays the information about an Interlisp function in the Interlisp Reference Manual. To aid us in the upgrade of our Common Lisp implementation, HELPSYS was extended to look up in the Common Lisp HyperSpec, and also more internal Medley documentation.
* **TEdit Redone**: Enhancements to our existing text editor in preparation for better Unicode support and to improve system efficiency, reliability, and maintainability. This work included completing and debugging the subroutine-stubs for ingesting Xerox Alto’s Bravo-format files, so that legacy documents can now easily be converted to modern formats (PDF).
* **PDFStream**: Medley has a native imagestream implementation for producing PostScript®-format hardcopy files, but it does not (yet) include code for producing or displaying PDF files. As an interim solution, an imagestream was defined to create PDF files indirectly, by first producing a PostScript file within Medley and then executing a UnixUtils shell command to run an available PostScript-to-PDF Unix utility (e.g., Ghostscript’s ps2pdf). In a similar way, the Medley Filebrowser’s “See” option was extended so that PDF files are opened automatically in a separate window by a resident PDF viewer (Preview, Acrobat…). Filebrowser automatically converts PostScript files to PDF so that they can also be seen.
* **UnixUtils:** In the last year we enhanced the set of tools that enables Medley to reach into its surrounding platform to accomplish tasks that are not available (and too extensive to implement) in Medley. As an example, the ShellBrowse function will open the specified URL within a browser running on the host platform. Similarly, ShellOpen can be used to open a PDF file using whatever PDF viewer is resident on the host platform.
* **GITFNS (use of Git and GitHub) extended**: Considerable effort went into the integration of Interlisp File Manager and GitHub, including a menu-driven interface to comparing Lisp source files on a function-by-function basis. This facility is crucial to the way the system manages the “residential style” development tools of Interlisp with GitHub.

#### **Variety of Issues Closed and PRs Merged**

The project development is managed through use of GitHub. There were 216 issues since the beginning of 2023, 69 of which closed, although many of those were website issues. Some of the issues led to 141 Pull Requests over the same time span, 132 of which merged. We continue to smooth some of the rough edges of using the Interlisp programming tools with Common Lisp compatible functions.

#### **Community Engagement**

We’ve actively engaged with the Lisp and Software Preservation communities, fostering collaboration and knowledge sharing.

#### **Website Enhancements**

The [Interlisp.org ](https://interlisp.org/)website continues to evolve. Our primary goal over the last year has been to clarify our messaging and evolve the website to support it. We have focused on adding content and redeveloping the site making content easier to find. In parallel we have worked to ensure our website is indexed allowing web searches on subjects related to Interlisp and Medley to direct users to appropriate content. Work on search optimization has also enhanced the internal website search capabilities. Efforts to improve the Interlisp bibliography continue across both the Zotero site holding the bibliographic material and within the Interlisp website.

* **Content Organization and Accessibility:** In 2022, a first attempt at reorganizing the website was completed. Over the last year, we continued to revise and refine what and how to present material on our website. Changes are driven by new and improved content as well as improvements in our understanding of the story we need to tell. The result has been major improvements in website navigation. We continue to explore and work on new methods of enhancing our story telling. Work in progress includes a carousel on the landing page which will provide snapshots representing different facets of the Medley project.
* **Bibliography:** The website representation of the bibliography was reworked providing a cleaner interface and access to more details on each publication. In addition, GitHub’s automation tools were leveraged to ensure that the website’s presentation of the bibliography is synced with the master Zotero copy daily. Work continues on organizing the Zotero database. Efforts have focused on cleaning up individual entries and standardizing our representation of content. Going forward this effort will continue along with efforts to improve searching and filtering content.
* **Search Engine Optimization:** In the last year we tracked down and eliminated the majority of the inbound link errors. We attempted to ensure all previously published links were remapped to an appropriate page and 404 errors were minimized.
* **Custom Search:** We improved search within the Interlisp.org website extending it to beyond just website materials to include content published on our GitHub site. Searches now cover the majority of the artifacts created by the project.

#### **Presentations**

We are continuing to spread information about the availability of Medley through technical presentations. This year, our team presented three talks on Medley Interlisp.

* **BALISP:** In March 2023, we presented a discussion of the project’s efforts on restoring and modernizing Medley Interlisp to the Bay Area Lisp (BALISP) meetup group. [The slides are available](https://drive.google.com/file/d/1xpXSoEnc5PPnIa7BHcionBbc8v-Nxp7N/view?usp=sharing) and the talk was [recorded](https://www.youtube.com/watch?v=N1MobfEaoWY\&t=1s).
* **SPN Idea Workshop:** On November 2, Larry Masinter participated in the Software Preservation Network’s Idea Workshop; we continue to pursue some academic projects in the software preservation community.
* **Computer Conservation Society:** Steve Kaisler, a member of the Computer Conservation Society (CCS) in London, England, presented a talk entitled “Software Archeology: The Medley Interlisp Restoration Project” on November 16, 2023 in London, England. This talk discussed a brief history of Interlisp, some applications, and some issues and challenges in modernizing the Medley Interlisp software. The talk was recorded and will likely be posted soon.

#### **Project and Organization**

As the work proceeds we expand our resources and adjust our processes to better achieve the project goals. In 2023 our team grew and we devised ways of keeping track of the work on the GitHub repositories.

* Three new regular contributors joined the team, Matt Heffron, Paolo Amoroso and Andrew Sengul. Matt joined the team as a former Medley and Interlisp user and developer, and contributor to various projects. Paolo exercised Medley as a user, reporting any bugs and issues that needed attention, and reviewed the existing documentation. Andrew, who came to the project as a Lisp developer, undertook a major redesign of the project site, restructuring it according to the project goals and making it easier to find the information users need, as well as clarifying and expanding the content. He also investigated how the development of Interlisp and other Lisps can proceed. As part of this work, for example, he started checking out the Medley test harness in view of using it again for testing system builds.
* In our GitHub repositories we began tagging issues and pull requests with a set of projects that will help us track the progress of the work and ensure it fulfills the project goals.

### **Looking Ahead**

As we move into 2024, we remain committed to advancing the Medley Interlisp Project.

A long-term goal is “sustainability”: Get the system in a state where no prior knowledge is necessary for developers to make changes.

* Make sure it is possible to rebuild the system from sources (recompiling every Lisp module and LispUsers).
* Identify all of the documentation we have, catalog it and link it with the source code for the versions that we have.

Another goal is to extend our outreach activities to both the extent Lisp communities and to the broader Computer Science community.

We continue to extend and refine the documentation on Medley Interlisp, including volumes on the Lisp Object-Oriented Programming System (LOOPS).

We are evaluating a variety of Interlisp and Common Lisp applications with the goal of making them publicly available for download and use.

Thank you to our contributors, supporters, and the wider community for making this journey possible.

_Stay tuned for more exciting developments in the coming year!_
