*** Settings ***

Resource  keywords.robot
Resource  Accessibility/wavetoolbar.robot

Suite setup  Run keywords
...  Open accessibility test browser  Maximize Browser Window
Suite teardown  Close all browsers

*** Test cases ***

Test A11Y
    [Documentation]  Test content type default view for accessibility
    ...              errors.
    Enable Autologin as  Site Administrator

    Go to Homepage
    Load  https://www.youtube.com/watch?v=S5XgulzFzgI
    ${url} =  Execute Javascript  window.location.href;

    ${errors} =  Count WAVE accessibility errors  ${url}
    Should be true  ${errors} == 0
    ...  WAVE Toolbar reported ${errors} errors for ${url}
