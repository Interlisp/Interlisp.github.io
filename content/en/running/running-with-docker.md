---
title: Running with Docker
weight: 50
type: docs
---

As an experiment, we've set up a way to use Medley Interlisp via a pre-built Docker configuration. As part of the experiment,  we've set  up a docker container that contains Xvnc (a kind of protocol gateway) so you would just need a VNC client.

If this is your first time working with Docker, you'll want to [install it](https://docs.docker.com/get-docker/) before continuing.

You'll also need a modern VNC client; [TightVNC](https://www.tightvnc.com/) works well. Rumor has it that Macs and Linux use VNC normally for screen sharing.

```
docker run -p 5900:5900 -e DISPLAY=$DISPLAY --rm --name interlisp interlisp/medley
```
