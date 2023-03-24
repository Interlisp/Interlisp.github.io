---
title: Interlisp Online
weight: 10
type: docs
---

[Interlisp Online](https://online.interlisp.org/user/login) provides access to a version of Medley running in the cloud. You can login as a guest, but if you want to save state from one session to the next, you should create an acccount. All that is needed is an email address and password. Once an account has been created you can log in and start a Medley Interlisp session.

Sessions are preserved for users that login but 
* are not saved for "guests"
* may be deleted after 30 days of inactivity

Running online should be good for experimenting and introducing yourself to the environment. Anything you create in the online environment should be treated as transient. If you're interested in developing and experimenting with Lisp programs then you will want to investigate other options. But, for a first foray, this is a good starting place. The Interlisp/online repository may have more details.

### Things to note when running online

* Browser compatibility
* Watch out for control-character conflicts (control-W always gets me)
* Security not guaranteed
* Need a solid net connection to our AWS server (currently in Ohio)
* Back to time-sharing: Maximum load ~24 simultaneous sessions
