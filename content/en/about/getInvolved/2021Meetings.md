---
title: 2021 Meeting Agendas and Notes
weight: 2
type: docs
---

### Agenda 13 Dec 2021

* online.interlisp.org -- getting to a (0.9) release
* InterlispOrg Inc -- 501c3 approval

### Agenda 6 Dec 2021

* online.interlisp.org
* Github projects?

### Agenda 29 Nov 2021

Other Topics?

* mkvdate.c (was on agenda pushed to issue)
* SDL
* Releases (medley, maiko, docker)
* online.interlisp.org
* Using GitHub projects?
* Documentation: Book 3, release notes

### Agenda 22 Nov 2021

* Deployment
  * SDL status (Peter)
  * Docker build (Bill)
  * online.interlisp.org (Frank)
* git/GitHub Medley branch commi push workflow (Ron)
  * Masterscope issue
* Annual Report feedback (Larry)

### Agendas 8 & 15 November 2021

We spent both meetings reviewing the Annual Report and Round Table

### Agenda 1 November 2021 NOTE NEW MEETING TIME

We should put out a progress report of what we've done, new things or soon anticipated. First annual report. In the meeting let's try [Google Docs](https://docs.google.com/document/d/1cGBDNMO5yt6ymi7YiCcf6uNn6RBe5PVS7mW4kFnlzNY/edit?usp=sharing).

### Agenda 25 October 2021

Too much to talk about – lots is happening all at once.

* Steve has published Interlisp book 2: https://interlisp.org/docs/2021-interlisp-book-2.pdf
*   Peter has added support for SDL, a multi-platform (Windows, Mac OS X, Linux, iOS, and Android) X11 replacement, to maiko. SDL can be used instead of X11 as the shim to the native window system, and provides a more native feel.\
    [Add prototypical SDL support. by ecraven · Pull Request #403 · Interlisp/maiko](https://github.oom/Interlisp/maiko/pr/403/)

    Open points to discuss and/or implement:

    * Mouse button emulation (for systems that have less than three mouse buttons)
    * Scroll bars for the entire lisp window
    * CMake vs. makeright
    * Make `lde` support dynamically choosing a backend
    * Mouse cursors
    * Warping the mouse cursor
* Frank has released http://notecards.online using XVnc with saving of your lisp.virtualmem, sources [notecards repo](https://github.com/Interlisp/notecards/)
* Bill has released new loadup / docker / release automations [Medley actions](https://github.com/Interlisp/medley/actions/)
* Ron (wants to) give up on GitHub (maybe); integrating Git with a [lisp-based git desktop](https://github.com/Interlisp/medley/issues/536/)?

### Agenda 18 Oct 2021

* round table: Status & plans
* README's and release notes
* Distributions

### Agenda 11 Oct 2021

* Documentation (reader's guide, SK books)
* Releases and automation
* Help wanted bugs (#55 eval, MV return stack)

### Agenda 27 September 2021

Lots of things to talk about, that might require some preparation

Let's start with (5 min each max) round-table. Then 15 minutes each on plan for review

* Documentation:
  * what we have (Wiki list, PDFs, Interlisp.org site)
  * what we're working on (SK)
  * What we need (Documentation issues, bibliography)
* Subrs and opcode survey
* Unicode plans (internal and external encodings)
* Releases and distributions

### Agenda 20 September 2021

Round-table. Save for last:

* BACKGROUND-YIELD -> liapusers (for now)
* Releases
* no commit of loadups => need loadups-only release
* (dribble files? need copyall?)
* Interlisp/DOS

### Agenda 13 September 21

* Interlisp Org Inc status, Q\&A
* Zotero (Herb?)
* Releases (Bill?)
* welcome Peter
* Envos files
* Fonts progress
* LispUsers

### Agenda 6 September 2021

Labor Day (US Holiday); attendance uncertain. Let's do a "round table" of brief status reports.

* Interlisp.Org Inc -- progress
* Zotero bibliography
* Releases
* Documentation - FAQ?
* Fonts (sigh)

### Agenda 30 August 2021

* loadups, releases, GitHub automation, Notecards configuration

### Agenda 23 August 2021

* Review of [Ongoing Projects](../ongoing-projects/)

before we dive into other topics, including:

* \*.TEDIT to PDF for all medley / envos repos
* envos repo reorg / undo cr/lf transform
* tests and benchmarks

### Agenda 16 August 2021

* Round table news
* Tracking down [bug 407](https://github.com/Interlisp/medley/issues/407/)

### Agenda 9 August 2021

* Notecards in the Cloud with Docker (@fhalasz)
* Recent merges
  * Unicode external format changes
  * Bye-bye old versions in repo (not entirely)
  * Docker and actions
* [Reviewing open Issues](https://github.com/Interlisp/medley/issues/)
* [Testing strategy](https://github.com/Interlisp/medley/issues/373/)
* [Organizational partners](../partners)

### Agenda 2 August 2021

* Testing -- how to make test cases for changes
* Git commit quality and separability
* Recent PR merges
* maintenance workflow
* Simplify process of obtaining new releases (mjd)

### Agenda 26 July 2021

* DOSBox / uploads
* Ron’s IO changes /Interlisp/medley/pull/348
* Project goals & bylaws (TBA)

### Agenda 19 July 2021

• 30 minutes topics important for filing for 501c3 articles of incorporation

1. brainstorming a list of possible organizational goals. I imagine this as a “brainstorming” session where we collect ideas. It’s important to have a broad purpose statement to allow flexibility but specific enough to attract volunteers and donations. Consolidation, evaluation, and pruning will come later. The ideas should be expressed in terms suitable for filing for non-profit status. See [Medley Interlisp Goals](https://docs.google.com/document/d/1q15mKHJt1fiFToamUacDWvw2UnUDJIaWLuuaeEUQS8k/edit#heading=h.8pdelledleut) and [Ongoing Projects](../ongoing-projects/) for inspiration.
2. Av list of ideas for the organization name.

I will record the session but it would be wonderful if someone could take notes (setting up a google document we all could connect to)

• 30 minutes round table: status, plans, blockers

### Agenda 12 July 2021

I'd like to talk about overall project goals in relationship to [Ongoing Projects](../ongoing-projects/)

### Agenda 5 July 2021

[Ongoing Projects](../ongoing-projects/) in reverse order

### Agenda 28 Jun 2021

I'd like some feedback on [Project Organization](../going-projects/). My hope is to use this organization to drive the agenda.

### Agenda 21 Jun 2021

Usual round-table status and plans

### Agenda 14 Jun 2021

some topics to touch base on

* Docker (Herb)
* Notecards demo (Frank?)
* Medley 2.0 on DOSBox (Arun?)
* Space and versions and file name case (Bill? Larry)
* EOL convention problems with DFASLs? (Ron?)
* Meeting recordings available to LispCore for 2 weeks

### Agenda 7 June 2021

* Introductions (if invitees can make it)
* Docker (Herb)
* Topic "Notecards Demo"

1. running old sysouts with DarkStar
2. running old sysouls with Medley 2.0 on DosBox
3. recompiling and loadup with modern medley

* "International Keyboard Support"
* "Zotero Interlisp bibliography"
*
  * Working with Fiverr
* git-versions
* GitHub space plan

### Agenda 24 May 2021

Usual round table, hoping to include topics:

* Docker plans (Herb)
* Filter GitHub for big files; use GitHub LFS; or both (? Bill)
* Running in Windows? (Steve)
* Starting an Interlisp non-profit (Larry)
* Stack overflow bug?

### Notes 17 May 2021

These are rough notes from the meeting. I regularly record the meetings for private consumption.

* Let me ask each of the attendees, your decision on the question of what to do: stop recording, available to LispCore members, available public, available on request. I want to respect everyone's conditions, and would like an explicit ack. I'll summarize before acting.
* [Reducing git repo size](https://github.com/Interlisp/medley/discussions/102/#discussioncomment-736844) (Bill Stumbo) We decided "one change at a time" even if it causes multiple force push, and invalidates forked repos (There were a small number.) If the forkers can cope once, they can prepare for the second time). Bill will test his filter on a fork/copy and make sure it has the desired effect.
* Steve was still having problems running WSL2 on Windows. Windows 10 Home vs. Windows 10 pro. We should resurrect the original instructions for running on Oracle Virtualbox or VmWare. Making progress on INTERLISP volume 2.
* [Bibliography progress](https://interlisp.org/bibliography/) (Abe) Abe showed off the Bibliography and advanced features on Zotero.org. There's a search feature but it's buggy. (The implementation is in the GitHub Interlisp/interlisp.github.io repository. I think Issues with the website and bibliography could just use Medley issues with tag "Documentation".
* Herb talked about the Docker and automation issues he was going to reverse inherit from Abe.
* [Character IO changes](https://github.com/Interlisp/medley/tree/Cleanup-character-IO-interfaces/) (Ron) Ron described his progress.
* [Versions from git](https://github.com/Interlisp/medley/pull/333/) (Larry) I demoed a 'proof of concept' for pulling old versions from git. I'll keep you posted
* [Notecards Demo](https://github.com/Interlisp/medley/issues/4/) (Arun, Frank Halasz(?))
* [stack overflow multiple value return bug](https://github.com/Interlisp/medley/issues/19/)\
  Nick and I talked over the fine details of who does what to the stack and why. The conjecture is this isn't a new bug, just a fault that was rare.

John Vittal, Arun Welch, Abe Jellinek, Herb Jellinek, Larry Masinter, Bill Stumbo, Nick Briggs, Ron Kaplan, John Cowan, Steve Kaisler, Michele Denber

***

#### **Agenda 10 May 2021**

* Round Table
* Changing character encoding default (Ron)
* The [stack overflow](https://github.com/Interlisp/medley/issues/19/) debugging techniques (as a "case study")

#### **Agenda 3 May 2021**

After trying other alternatives, I'm coming back to using the Wiki for agendas

* it's easy to find (not getting lost)
* Anyone can update easily

This week, we will (hopefully) see John Vittal and Steve Kaisler (who joined us last Monday)

* Introductions & usual 'round table'. Topic suggestions
  * John Vittal welcome
  * Steve Kaisler's Interlisp book and Volume II plans (Any success loading release?)
  * Bibliography (Abe)
  * EOL change in sources (Ron)
  * Lispusers (Herb?)
* Other topics if there's time
  * Loadups, releases
  * defaults for printing

#### Agenda 8 March 2021

* As usual, what have you been up to? (Status and Plans)
* Making releases:
* Visibility
* workflow on duplicate function removal (how to make each a PR)

### Agemda 22 Feb 2021

Topics I have for tomorrow

* Experimenting with loading all of sysfiles
* Cleaning out "dead wood" in the Lisp code

regular features:

* recent bug reports
* round table

#### Agenda 15 Feb 21

* Round table news & plans
* Configuration vs. Documentation (Masterscope & DInfo, Match, fonts)
* making the init and loadup review
*
  * reviewing the PR #187
*
  * debugging and analysis techniques

meeting recorded but available for 1 week on request

#### **Agenda 25 Jan 2021**

* Recent documentation updates (READMEs, Wiki) and plans
* Pinning CPU experiments
* MEDLEY-UTILS
* Common Lisp / Interlisp priorities
