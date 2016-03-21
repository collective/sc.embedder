*** Settings ***

Library  sc.embedder.tests.test_robot.Keywords
Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

*** Variables ***

${html_text} =  HTML code
${embedder_title} =  Nulla in mundo pax sincera
${title_selector} =  input#form-widgets-IDublinCore-title
${description_selector} =  textarea#form-widgets-IDublinCore-description
${width_selector} =  input#form-widgets-width
${height_selector} =  input#form-widgets-height
${embed_html_selector} =  textarea#form-widgets-embed_html
${image_load_selector} =  input#form-widgets-image-load
${image_replace_selector} =  input#form-widgets-image-replace
${image_input_selector} =  input#form-widgets-image-upload
${url_selector} =  input#form-widgets-url

*** Keywords ***

Click Add Embedder
    Open Add New Menu
    Click Link  css=a#sc-embedder
    Page Should Contain  Add Embedder

Click Add Page
    Open Add New Menu
    Click Link  css=a#document
    Page Should Contain  Add Page

Select File
    [arguments]  ${file}

    ${PATH_TO_TESTS} =  Get path to tests
    Choose File  css=${image_input_selector}  ${PATH_TO_TESTS}/${file}

Create
    [arguments]  ${title}

    Click Add Embedder
    Input Text  css=${title_selector}  ${title}
    Input Text  css=${width_selector}  1
    Input Text  css=${height_selector}  1
    Input Text  css=${embed_html_selector}  <span>${html_text}</span>
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

