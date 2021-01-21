Changelog
---------

There's a frood who really knows where his towel is.

1.5.1 (2021-01-21)
^^^^^^^^^^^^^^^^^^

- Fix error 403 on YouTube's oEmbed endpoint (Ref. `#95`_).
  [idgserpro]

1.5.0 (2019-05-07)
^^^^^^^^^^^^^^^^^^

- Allows Embedder content to be linkcable in TinyMCE.
  [idgserpro]

- Add ``cssselect`` as pakage dependency.
  [idgserpro]


1.5b2 (2017-10-10)
^^^^^^^^^^^^^^^^^^

- Code clean up;
  enforce usage of Products.PortalTransforms >=2.1.10 as ``<iframe>`` must be listed as a valid tag.
  [hvelarde]

- Remove hard dependency on collective.dexteritytextindexer.
  [hvelarde]

- Update ``SearchableText`` index for Embedder objects.
  [hvelarde]


1.5b1 (2017-09-20)
^^^^^^^^^^^^^^^^^^

- Fix i18n and update Brazilian Portuguese and Spanish translations.
  [rafahela, hvelarde]

- ``SearchableText`` index for Embedder content type now includes object id and keywords.
  [hvelarde]

- Remove dependency on collective.dexteritytextindexer.
  [hvelarde]


1.4b1 (2017-09-06)
^^^^^^^^^^^^^^^^^^

- Add Related Items behavior to Embedder content type by default (closes `#80 <https://github.com/simplesconsultoria/sc.embedder/issues/80>`_).
  [hvelarde]

- Add Embedder to TinyMCE's list of linkable content types (closes `#79 <https://github.com/simplesconsultoria/sc.embedder/issues/79>`_).
  [hvelarde]

- Remove hard dependency on Products.TinyMCE.
  [hvelarde]

- Drop support for Plone 4.2.
  [hvelarde]


1.3b1 (2017-02-20)
^^^^^^^^^^^^^^^^^^

- Use semantic markup on the Embedder view (for simplicity, we are using `WebPage <http://schema.org/WebPage>`_  type).
  [hvelarde]

- Remove references to Grok's ``w`` dictionary used on the view template (fixes `#72`_).
  [rodfersou]


1.2b2 (2017-01-09)
^^^^^^^^^^^^^^^^^^

- Update list of package dependencies.
  [hvelarde]

- Fix width validator.
  [hvelarde]

- Remove dependency on plone.directives.form and latest traces of Grok.
  [hvelarde]


1.2b1 (2016-12-16)
^^^^^^^^^^^^^^^^^^

- Remove dependency on five.grok (closes `#63`_).
  [rodfersou]

- Package is compatible with Plone 4.2 again.
  [hvelarde]

- Avoid `TypeError` while running upgrade step (fixes `#58`_).
  [hvelarde]


1.1b2 (2016-04-25)
^^^^^^^^^^^^^^^^^^

- Implement `Subresource Integrity <https://www.w3.org/TR/SRI/>`_ (closes `#55`_).
  [cleberjsantos]

- Sanitize <iframe> tags to avoid including invalid HTML attributes;
  an upgrade step is included to clean up existing objects (closes `#44`_).
  [rodfersou, hvelarde]

- Update Video.js to v5.8 and load it from CDN (closes `#50`_).
  [rodfersou]


1.1b1 (2016-03-24)
^^^^^^^^^^^^^^^^^^

- Remove hard dependency on plone.app.referenceablebehavior as Archetypes is no longer the default framework in Plone 5.
  Under Plone < 5.0 you should now explicitly add it to the `eggs` part of your buildout configuration to avoid issues while upgrading.
  [hvelarde]

- Fixes issue in TinyMCE plugin when clicked in Insert button (closes `#16`_).
  [idgserpro]

- Fix error in TinyMCE plugin if the property icon_visibility is disabled (closes `#42`_).
  [rodfersou]


1.0b5 (2015-11-18)
^^^^^^^^^^^^^^^^^^

- Fix the stripping of embed code when it has more than one tag, like in Facebook videos (closes `#39`_).
  [rodfersou]

- Use "application/javascript" media type instead of the obsolete "text/javascript".
  [hvelarde]

- Remove Chrome Frame from ``X-UA-Compatible`` HTTP header as it's deprecated.
  [hvelarde]

- Allow use of percent sign (%) on width properties (closes `#6`_).
  [rodfersou, hvelarde]

- Added italian translation
  [keul]


1.0b4 (2015-09-03)
^^^^^^^^^^^^^^^^^^

- Add Embedder tile for collective.cover (closes `#32`_).
  [rodfersou]

- Brazilian Portuguese and Spanish translations were updated.
  [rodfersou, hvelarde]

- Add portal message instead of log info on HTTP request errors (closes `#14`_).
  [rodfersou]

- Add validation in URL field to avoid hiding errors when using the Load button (closes `#20`_).
  [rodfersou]

- Remove dependency on collective.oembed (closes `#3`_).
  [hvelarde]

- Drop support for Plone 4.1 and 4.2; remove dependency on unittest2.
  [hvelarde]


1.0b3 (2013-07-23)
^^^^^^^^^^^^^^^^^^

- Fix a couple AJAX quoting/unquoting problems on the TinyMCE plugin.
  [jsbueno]

- Add helper methods image_thumb and tag in order to be listed in
  folder_summary_view [ericof]

- Fix an UnicodeDecodeError with our plugin for TinyMCE [ericof]


1.0b2 (2012-12-03)
^^^^^^^^^^^^^^^^^^

- Fix a conflict with plone.formwidget.namedfile NamedImage widget
  implementation. [jpgimenez]


1.0b1 (2012-11-27)
^^^^^^^^^^^^^^^^^^

- Update package dependecies for Plone 4.3 compatibility. [hvelarde]

- Fix functional tests. [hvelarde]

- Rename package: was sc.content.embedder and now is sc.embedder. [hvelarde]

- Support for VideoJS as fallback if static file and no supported provider.
  [jpgimenez]

- Fixed the rendering of the embedded code to not break the main view.
  [jpgimenez]

- Allow selecting, embedding and rendering sc.embedder content into TinyMCE
  widgets as if it were images. [jpgimenez]

- VideoJS embedder code implemented as an iframe, to simplify the integration
  with TinyMCE. [jpgimenez]


1.0a3 (2012-10-04)
^^^^^^^^^^^^^^^^^^

- Fixed KeyError: 'width' when saving embeded HTML with percentages.
  [davilima6]


1.0a2 (2012-09-05)
^^^^^^^^^^^^^^^^^^

- Functional tests were updated to run with robotframework-selenium2library.
  [hvelarde]

- i18n was fixed and Spanish translation was updated. [hvelarde]

- Brazilian Portuguese translation was fixed. [agnogueira]


1.0a1 (2012-09-05)
^^^^^^^^^^^^^^^^^^^

- Initial release.

.. _`#3`: https://github.com/simplesconsultoria/sc.embedder/issues/3
.. _`#6`: https://github.com/simplesconsultoria/sc.embedder/issues/6
.. _`#14`: https://github.com/simplesconsultoria/sc.embedder/issues/14
.. _`#16`: https://github.com/simplesconsultoria/sc.embedder/issues/16
.. _`#20`: https://github.com/simplesconsultoria/sc.embedder/issues/20
.. _`#32`: https://github.com/simplesconsultoria/sc.embedder/issues/32
.. _`#39`: https://github.com/simplesconsultoria/sc.embedder/issues/39
.. _`#42`: https://github.com/simplesconsultoria/sc.embedder/issues/42
.. _`#44`: https://github.com/simplesconsultoria/sc.embedder/issues/44
.. _`#50`: https://github.com/simplesconsultoria/sc.embedder/issues/50
.. _`#55`: https://github.com/simplesconsultoria/sc.embedder/issues/55
.. _`#58`: https://github.com/simplesconsultoria/sc.embedder/issues/58
.. _`#63`: https://github.com/simplesconsultoria/sc.embedder/issues/63
.. _`#72`: https://github.com/simplesconsultoria/sc.embedder/issues/72
.. _`#95`: https://github.com/simplesconsultoria/sc.embedder/issues/95
