# nnfeedfix

## Rationale

I have noticed that the Atom feed for the Nerf Now webcomic no longer works in my feed readers.
It seems that the site changed from a self hosted feed to one hosted by feedburner after the 25/05/2023.

## Workaround

This Python module runs a simple webserver that responds to HTTP GET requests by fetching the Nerf Now "Atom" feed and editing it to make it compatible with readers.
