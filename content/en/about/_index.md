---
title: About
aliases:
  # We want to redirect from /About.php. We need ".php.html" else the
  # redirect page is downloaded to ~/Downloads/ rather than shown in browser. See:
  # https://github.com/jekyll/jekyll-redirect-from/issues/145#issuecomment-392277818
  - /About.php.html
  - /News.php.html
weight: 1
type: docs
---
         
The 1970s and 80s saw major advances in computing and Human-Computer interaction.  Interlisp was one of the many experimental systems developed during these heady times.  It represents and early example of a system with a GUI (Graphical User Interface), and IDE (Integrated Development Environment) and within the Xerox PARC environment, it was an early example of a network enabled machine supporting email, file sharing .  In essence it was a forerunner of today's computing systems.

## Medley

Medley Interlisp represents the last Xerox Interlisp release.  Medley continued Xerox PARC's experimentation with developing systems for [D-machines](http://www.bitsavers.org/pdf/xerox/parc/Exploring_the_Ethernet_with_Mouse_and_Keyboard_May81.pdf), a family of computers (Dorado, Dolphin, Dandelion, Daybreak) descended. The project was later spun out to a company called Envos, which then turned into Venue.

It was the first IDE with a window/mouse/menu GUI, launched as a product from Xerox in 1980. It was a base from which AI applications were built, as well as a research project in its own right.

{{< imgproc Interlisp_Screen Fill "2000x600" >}} Medley Interlisp User Interface. {{< /imgproc >}}



## Restoration

Our aim is to restore **Medley Interlisp** to usability on modern systems, sufficient to allow someone to develop some code and experience what it was like. You could think of this as a kind of "*vintage software*" project, to try to capture the sense of fluidity in the development cycle. 

We hope to provide a platform for demonstration of early experiments of hypertext (Notecards), Desktop management (Rooms), Object-oriented programming (LOOPS), as well as Interlisp itself.

## Process

Primarily this is a matter of testing and debugging.  Identified [issues](https://github.com/interlisp/medley/issues) are documented in the Interlisp/medley repo. 

We're also trying to "*modernize*" some things; for example, we're adding Unicode support for IO (Interlisp-D was built before Unicode, and supports an older Xerox encoding). As with most open source projects, what we're able to accomplish depends on volunteers

---

For example, Interlisp [SEDIT](https://www.youtube.com/watch?v=2qsmF8HHskg) is the canonical ancestral structure editor. Masterscope and the "file package" included system-management tools that combined features of version control and build systems, with comprehensive cross referencing support.

Medley was the last release of the Xerox Lisp environment, before the whole environment was renamed Medley. It was originally written in Interlisp (a dialect separate from the MACLISP/Common Lisp tradition, with its own ancestry), but later, Common Lisp also became part of the environment. Medley includes a WYSIWYG text editor (TEdit), email organizer (Lafite), performance tools (Spy) and many other libraries and user contributed code (from the 1980s).

The [1992 ACM Software System Award](https://awards.acm.org/award_winners?year=1992&award=149&region=&submit=Submit&isSpecialCategory=), to Daniel G. Bobrow, Richard R. Burton, L. Peter Deutsch, Ronald M. Kaplan, Larry Masinter, Warren Teitelman  

> ... for their pioneering work in programming environments that integrated

>> -- source-language debuggers,  
>> -- fully compatible integrated interpreter/compiler,  
>> -- automatic change management,  
>> -- structure-based editing,   
>> -- logging facilities,  
>> -- interactive graphics, and  
>> --  analysis/profiling tools  

> in the Interlisp system.