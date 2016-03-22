*** Settings ***

Resource  keywords.robot

Test Setup  Open Test Browser
Test Teardown  Close all browsers

*** Test cases ***

Test CRUD
    Enable Autologin as  Site Administrator
    Go to Homepage
    Create  ${embedder_title}
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
