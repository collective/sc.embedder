*** Settings ***

Library  sc.embedder.tests.test_robot.Keywords
Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open Test Browser
Test Teardown  Close all browsers

*** Variables ***

${title_selector} =  input#form-widgets-IDublinCore-title
${description_selector} =  textarea#form-widgets-IDublinCore-description
${width_selector} =  input#form-widgets-width
${height_selector} =  input#form-widgets-height
${embed_html_selector} =  textarea#form-widgets-embed_html
${image_load_selector} =  input#form-widgets-image-load
${image_replace_selector} =  input#form-widgets-image-replace
${image_input_selector} =  input#form-widgets-image-upload
${url_selector} =  input#form-widgets-url

*** Test cases ***

Test CRUD
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create  Nulla in mundo pax sincera
    Update  Blando colore oculos mundus decepit
    Delete

Test Load
    Enable Autologin as  Site Administrator
    Go to Homepage
    Load  http://vimeo.com/17914974

Test Required Fields
    Enable Autologin as  Site Administrator
    Go to Homepage
    Click Add Embedder
    Click Button  Save
    Page Should Contain  There were some errors

*** Keywords ***

Click Add Embedder
    Open Add New Menu
    Click Link  css=a#sc-embedder
    Page Should Contain  Add Embedder

Select File
    [arguments]  ${file}

    ${PATH_TO_TESTS} =  Get path to tests
    Choose File  css=${image_input_selector}  ${PATH_TO_TESTS}/${file}

Create
    [arguments]  ${title}

    Click Add Embedder
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${width_selector}  0
    Input Text  css=${height_selector}  0
    Input Text  css=${embed_html_selector}  <br/>
    Click Button  Save
    Page Should Contain  Item created
    Page Should Contain  ${title}

Update
    [arguments]  ${description}

    Click Link  link=Edit
    Input Text  css=${description_selector}  ${description}
    Click Element  css=${image_input_selector}
    Select File  image.jpg
    Click Button  Save
    Page Should Contain  Changes saved
    Page Should Contain  ${description}

Delete
    Open Action Menu
    Click Link  css=#plone-contentmenu-actions-delete
    Click Button  Delete
    Page Should Contain  Plone site

Load
    [arguments]  ${url}

    Click Add Embedder
    Input Text  css=${url_selector}  ${url}
    Click Button  Load
    Click Button  Save
    Page Should Contain  Item created
