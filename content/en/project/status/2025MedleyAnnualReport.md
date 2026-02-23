---
title: 2025 Medley Interlisp Annual Report
weight: 1
type: docs
aliases:
 - /news/2025medleyannualreport/
 - /project/news/2025medleyannualreport/
---

{{< figure src="/Resources/logo_red_no_border_568x385.png" width="284" height="194" >}}

## **Overview**

2025 marked the fifth year of the [Medley Interlisp Project](https://interlisp.org).

We began the project in 2020 by merging code fragments from different sources and versions which last ran two decades earlier on long-obsolete machines. Over the intervening five years we consolidated the code and ported it to run on all major operating systems, as well as online via web browsers.

Medley can now run most of its original applications and support the development of new ones, such as the tools and games we created over these years.

Part of preserving Interlisp is bringing to the 21st century its ecosystem of software and knowledge. Along with making most of the original applications run again we compiled an extensive bibliography of documentation and literature. Historians and users can now access a major portion of the same material Interlisp users worked with when the system was in current use.

In 2025 we closed 95 GitHub issues and merged 193 Medley pull requests and 17 Maiko pull requests.


## **Work on the Core Medley System**

In 2025 we continued to work on the Medley internals and environment to adapt it to current operating systems and hardware platforms, improve stability, fix bugs, and add new features.

We implemented a new architecture for action/character key-bindings which also provides support for arrow keys in the command line editor of Lisp executives, the TEdit WYSIWYG editor, and the Sketch line drawing tool; modified build scripts to provide better control over the system building process; and made the LOOP iteration construct conform better to the ANSI Common Lisp specification.

Medley inherited a problematic font and character-encoding architecture from prior Interlisp-D and Xerox Alto technologies, later mixed in with the Xerox Character Code Standard (XCCS), now frozen. The fundamental problem was that the meaning of a character code depended on the current font.  (For instance, to render the Greek letter 𝛂 (alpha) might require using the Latin character code “a” and a special Greek font.) We created the Medley Character Code System (MCCS), an update to XCCS that permits Medley to work better with both legacy fonts and new fonts from external sources. We also revamped the internal font machinery.

In a separate effort, we created an HTML stream in Medley’s device-independent graphics (DIG) framework, enabling Medley’s generic display operations to produce HTML files for display in desktop browser windows. TEdit streams, for example, can be “hardcopied” not only to Postscript and PDF files, but also now to HTML files. We also revised the printing architecture and introduced a “VIEWER” printer that allows sending files to desktop windows.

In other work in Medley and Maiko, we laid the foundations for supporting old Xerox network protocols in order to run historical Interlisp networked applications, including distributed collaboration tools.

## **Community Outreach**

To bridge the gap between the old Medley environment and modern users we published a new primer, [*Medley Interlisp for the Newcomer*](https://primer.interlisp.org) at https://primer.interlisp.org. The primer assumes no prior knowledge of Lisp and takes the reader from operating the user interface to developing simple programs.

As part of Medley Online, a version of the environment accessible from web browsers, we implemented “Museum Mode.” This allows a user to automatically run arbitrary Lisp programs specified as part of a Medley Online URL, complementing self-learning resources like the Primer with support for guided demonstrations in museums or other settings. The work was a result of a new collaboration on an Interlisp exhibit at the [Interim Computer Museum](https://icm.museum).

Educating users and sharing our experience with the software preservation and history of computing communities are important to make Medley more approachable.

To this end, in 2025 we opened social media accounts on Mastodon and Bluesky and created a LinkedIn group. We continued assisting users on the project infrastructure such as GitHub discussions and issues.

University of Alberta student Eleanor Young presented the paper *The Medley Interlisp Project: Reviving a Historical Software System* at the 2025 IEEE Canadian Conference on Electrical and Computer Engineering and Industry Summit (CCECE). Larry Masinter was a guest of the Lispy Gopher Climate radio show at aNONradio and the Netstack.FM podcast. Ryan Burnside entered the Autumn Lisp Game Jam 2025 with an Interlisp game, bringing the system to the attention of the gaming community.

The Interlisp bibliography at https://interlisp.org/bibliography continues to be a key learning and reference resource. This year we restructured and redesigned it, focusing on improving the browsing experience and making its contents more easily searchable. In addition, we improved access to citation information. We continue to focus on extending and validating bibliographical metadata.

The historical context of Interlisp is another aspect of the Medley ecosystem that can immerse modern users into the working and evolution of the system. In 2025 we began examining a major archive of unpublished Medley material, such as emails and documents, and building tools for research and presentation.

## **Credits**

The Medley Interlisp Project depends on enthusiasts and volunteers. While it is impractical to list every contribution, we want to acknowledge significant achievements within the project:

* [Medley Interlisp for the Newcomer](https://primer.interlisp.org): author [Abhik Hasnain](https://www.linkedin.com/in/abhik-hasnain-285667293/overlay/about-this-profile/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3BVE2CLjbPQNua94s7Lm4Msw%3D%3D), University of Alberta
* [Interlisp bibliography reorganization](https://interlisp.org/history/bibliography): Abhik Hasnain and [Eleanor Young](https://www.linkedin.com/in/eleanor-young/overlay/about-this-profile/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3B3D6WZ9beRaKbEixni9DkWg%3D%3D), both University of Alberta
* Designing and documenting the bibliography intake process: Eleanor Young
* Curating the Interlisp [YouTube channel](https://www.youtube.com/@Interlisp): Eleanor Young
* Creation of [tutorial videos](https://www.youtube.com/playlist?list=PLVdf9_UoHmPngEKSE7SDLoQiX9w-_pAJW): [Ryan Burnside](https://www.linkedin.com/in/ryan-burnside-84500a34/overlay/about-this-profile/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3BjaN8Uux1S0CUEWQqJEIZTw%3D%3D)
* [Hungarian Rings](https://itch.io/jam/autumn-lisp-game-jam-2025/rate/4015363), a submission to the Autumn Lisp Game Jam 2025: Ryan Burnside

## **Looking Ahead**

Our major long term goal is to make the Medley Interlisp Project reach “escape velocity,” i.e., enable it to proceed without the original developers.

In 2026, we plan to work on producing more material for Museum Mode and provide a wider selection of learning resources. In particular, we aim to update the sources of the Interlisp Reference Manual so we can produce new versions. We intend to make networking usable and demonstrate some of the original Interlisp applications that depend on it.

We thank our contributors, supporters, and the wider community for making this journey possible.
