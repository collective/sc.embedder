.. contents::

Introduction
============

This packages gives you the oportunity to create a multimedia content type
for systems based on Plone with just few clicks. Bring you multimedia content
from main multimedia providers to you site, intranet or whatever.

Usage
=====

Once the product is installed you will note that you are available to add
a *Multimedia* content type. Inside this add view you will see the fields:

- Multimedia URL
- Description
- Embed html code
- Width
- Height
- Player position
- Body text
- Alternative Content
- Image

In the URL field you must put the url of you content. Like:
    * http://vimeo.com/17914974

and then click the *load* button. This will bring automatically some data of
the element from the provider to the form. It depends on each provider what
data it going to add. But generally the fields title, description, width,
height and embed html fields are the one to be filled.

**Note**: *Some providers only support width, height and title. So the fields
like description or html embed code are necessarily to be filled manually.
This information is normally encountered in the page where the url is
pointing to*.

Layout
^^^^^^
With *player position* field you can set where the embed multimedia is going
to be render regarding the body text. You have the options *top, bottom, left
and right*.

Body text will be the main information that will describe the content type.

The *alternative content* is to give a description or transcription to an
individual that is no able to hear. In the layout this is hidden by default.
There is a link called **alternative content** that will show or hide again
the content of this field by clicking on it.

The *Image* will be the image that it will be showed in a search list that
someone will generate to give a quick visual description of the item.

Providers
=========

This product use `collective.oembed <http://pypi.python.org/pypi/collective.oembed>`_.
You can check his documentation to see a list of them.
