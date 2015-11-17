Changelog
---------

There's a frood who really knows where his towel is.

1.0b5 (unreleased)
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
.. _`#20`: https://github.com/simplesconsultoria/sc.embedder/issues/20
.. _`#32`: https://github.com/simplesconsultoria/sc.embedder/issues/32
.. _`#39`: https://github.com/simplesconsultoria/sc.embedder/issues/39
