*** Settings ***

Resource  keywords.robot

Test Setup  Open Test Browser
Test Teardown  Close all browsers

*** Test cases ***

Test Tinymce Plugin

    Enable Autologin as  Site Administrator
    Go to Homepage
    Create  ${embedder_title}
    Go to Homepage
    Click Add Page
    Input Text  title  Page Title
    Click Link  css=span .mce_scembedder
    Select Frame  id=mce_inlinepopups_16_ifr
    Select Radio Button  internallink  http://localhost:${ZOPE_PORT}/plone/nulla-in-mundo-pax-sincera
    Element Should Contain  css=#previewimagecontainer  ${html_text}
    Click Button  Insert
    Page Should Contain  ${html_text}
    Click Button  Save
    Page Should Contain  ${html_text}
    Page Should Contain  Changes saved.
