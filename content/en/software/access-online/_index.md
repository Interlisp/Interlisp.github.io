---
title: Access Medley Online
weight: 10
type: docs
aliases:
  - /medley/using/running/online/	
  - /medley/using/running/online
  - /running/online
  - /running/online/using/online
  - /software/access-online
---

Running Medley online is good for experimenting and introducing yourself to the environment. However, anything you create in the online environment should be treated as transient. If you're interested in developing and experimenting with Lisp programs, you will want to investigate other options. For a first foray, it is a good starting point.

### Things to note when running online

* **Browser compatibility:** Older browsers may not support the VNC software we use; it should give you a warning if this is detected.
* **Control-character conflicts:** Different browsers may intercept user typing control-characters; for example, control-W might close the entire Medley window, rather than backward-delete a word. There is no standard fix: Using Chrome in "full screen" mode; using a browser extension which captures the control-character for its own operations might help. 
* **No guarantees:** In general, Medley has NO WARRANTY, but in particular we make no guarantees that private information will not be revealed, or that your files uploaded to your account will be held securely.
* **Reliable Internet:** You need a solid net connection to our AWS server (currently in Ohio).

## Accessing Interlisp Online

1. Go to [Interlisp Online](https://online.interlisp.org/)
{{< imgproc Login_Screen Resize "400x450">}} Interlisp Online Login {{< /imgproc >}}
2. Login to Medley Interlisp Online:
   * You can login as a guest by clicking <img src="Guest_Login_button.png" alt="Guest Login button"> on the login screen. However, guest sessions are not saved.
   * We suggest you create your own account by clicking <img src="New_User_Register_here_button.png" alt="New User Register here button"> on the login screen. Having an account enables you to save your sessions. To create an account, you just need an email address and password. Click Register here on the login screen to create your own account.

   * If you are already registered (created an account), log in and start a Medley Interlisp session. Sessions are preserved for users that login with their own account. However, user account sessions may be deleted after 30 days of inactivity.

3. Select the Exec you want to start out with. For example, select `Interlisp`. 

4. Leave the `Fill browser window` option set. 

5. Select `Run Medley`.
Your browser will open a window that represents the Interlisp Desktop and looks much like this:

{{< imgproc Online_Initial_Medley Resize "800x450">}} Medley Interlisp{{< /imgproc >}}

<div class="mx-auto">
 <a class="btn btn-lg btn-danger mr-3 mb-4" href="{{< relref "../using-medley/" >}}">
  Guide to Using Medley<i class="fas fa-arrow-alt-circle-right ml-2"></i>
 </a>
</div>

