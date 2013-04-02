***********
sc.embedder
***********

.. contents::

Life, the Universe, and Everything
----------------------------------

This packages gives you the oportunity to create a Embedder content type for
systems based on Plone with just few clicks. Bring your multimedia content
from main multimedia providers to your site, intranet or whatever.

Don't Panic
-----------

Once the product is installed you will note that you are available to add a
Embedder content type. When you attempt to add an item you will see the
fields:

- Content URL
- Description
- Embed html code
- Width
- Height
- Player position
- Body text
- Alternate content
- Image

In the URL field you must put the url of you content. Like:
    * http://vimeo.com/17914974

and then click the *load* button. This will bring automatically some data of
the element from the provider to the form. It depends on each provider what
data it going to add. But generally the fields title, description, width,
height and embed html fields are the one to be filled.

**Note**: *Some providers only support width, height and title. So the fields
like description or html embed code are necessarily to be filled manually.
This information is normally encountered in the page where the url is pointing
to*.

Layout
^^^^^^
With *player position* field you can set where the embed multimedia is going
to be render regarding the body text. You have the options *top, bottom, left
and right*.

Body text will be the main information that will describe the content.

The *alternate content* is to give a description or transcription to an
individual that is no able to hear. In the layout this is hidden by default.
There is a link called **alternate content** that will show or hide again the
content of this field by clicking on it.

The *Image* field is just to assign an image to the object that will give a
quick visual description of the content. The idea is to show it in listing
views or covers.

Providers
^^^^^^^^^

This product use `collective.oembed`_. You can check its documentation to see
a list of them.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/simplesconsultoria/sc.embedder.png
    :target: http://travis-ci.org/simplesconsultoria/sc.embedder

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/simplesconsultoria/sc.embedder/issues
.. _`collective.oembed`: http://pypi.python.org/pypi/collective.oembed
