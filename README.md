Fork of django-oembed from googlecode by WebRiders
==================================================

Changes
-------------
Now you can specify fixed width and height for the media using preceding '!' symbol.
E.g.: {% oembed !640x!480 %}http://www.viddler.com/explore/SYSTM/videos/49/{% endoembed %}

Fixed provider rules for providers which supports https  (Flickr, Revision3,
Google Videos, Wikipedia, YouTube and Vimeo).

TODO
-------------
Update docs.

django-oembed
-------------

This is a collection of tools for Django to allow for replacing links in text
with OEmbed.  This application also provides utilities to make this process not
prohibitively expensive CPU-wise.

For installation instructions, read INSTALL.txt.

Visit the google code page at http://django-oembed.googlecode.com/
