***********
sc.embedder
***********

.. contents::

Life, the Universe, and Everything
----------------------------------

This packages contains a Dexterity-based content type that allows you to
embedded content (such as photos or videos) from third parties into your Plone
site.

You can easily embed content from Flickr, SlideShare, SoundCloud, Vimeo,
Wikipedia, YouTube, and many other supporting the `oEmbed`_ format
especification.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/simplesconsultoria/sc.embedder.png?branch=master
    :target: http://travis-ci.org/simplesconsultoria/sc.embedder

.. image:: https://coveralls.io/repos/simplesconsultoria/sc.embedder/badge.png
    :target: https://coveralls.io/r/simplesconsultoria/sc.embedder?branch=master

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

1. Edit your buildout.cfg and add ``sc.embedder`` to the list of eggs to
   install ::

    [buildout]
    ...
    eggs =
        sc.embedder

2. If you are using Plone 4.1 you may need to extend a Dexterity known good
   set (KGS) to make sure that you get the right versions of the packages that
   make up Dexterity::

    [buildout]
    ...
    extends =
        http://good-py.appspot.com/release/dexterity/1.2.1

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to `sc.embedder`` and click the 'Activate' button.

.. Note::

	You may have to empty your browser cache and save your resource registries
	in order to see the effects of the product installation.

Use
^^^

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

In the URL field you must put the url of you content. For example:

    http://vimeo.com/17914974

and then click the *load* button. This will automatically populate the form 
with some data from the third party content. Which fields are populated depends 
on the individual provider. But in most cases the fields: title, description, width,
height and embed html fields will be filled.

**Note**: *Some providers only support width, height and title. So the fields
like description or html embed code will need to be filled manually.
This information is normally found in the page where the url points to*.

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

This product uses `collective.oembed`_. You can check its documentation to see
a list of supported providers.

.. _`oEmbed`: http://www.oembed.com/
.. _`opening a support ticket`: https://github.com/simplesconsultoria/sc.embedder/issues
.. _`collective.oembed`: http://pypi.python.org/pypi/collective.oembed
