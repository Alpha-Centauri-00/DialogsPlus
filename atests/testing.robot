*** Settings ***
Library           DialogsPlus    #config=D:/robotframework-dialogsplus/atests/config.yaml
Library           OperatingSystem

Suite Setup       Set Log Level    level=TRACE
Test Setup        Log To Console    \n*** Running Test: ${TEST NAME} ***

*** Variables ***

@{fields_val}     username    password    email    phone
@{fields}         username    password
&{default_val}    username=admin    password=P@55    phone=1234567
&{default}        username=user1    password=P@55

*** Test Cases ***

Get Value From User Default
    ${result}    Get Value From User    prompt=Enter your name:    default=Robot framework
    Should Be Equal    ${result}    Robot framework

Run Manual Steps Executes
    ${steps}    Create List    Open the app    Click Start button    Verify status
    Run Manual Steps    ${steps}
    Log    Manual steps executed successfully

Count Down Runs
    Count Down    3
    Log    Countdown executed for 3 seconds

Get Confirmation Returns Boolean
    ${result}    Get Confirmation    Are you sure?
    Should Be True    isinstance(${result}, bool)

Get Multi Value
    ${result}    Get Multi Value    ${fields}    default=${default}
    Should Be Equal    ${result}[username]    user1


Get Multi Value Multiple Fields
    ${result}    Get Multi Value    ${fields_val}    default=${default_val}
    Should Be Equal    ${result}[password]    P@55
    Should Be Equal    ${result}[phone]       1234567

Choose File Single
    ${XML_FILETYPES}    Evaluate    [("xml files", "*.xml")]
    ${result}=    Choose File    message=Select file to upload    filetypes=${XML_FILETYPES}
    Should Contain    ${result}    .xml

Choose File Multiple
    ${HTML_FILETYPES}    Evaluate    [("HTML", "*.html")]
    ${result}=    Choose File    message=Select multiple files    filetypes=${HTML_FILETYPES}   multiple=True
    Should Contain    ${result}[0]    .html

Choose Folder Test
    ${result}=    Choose Folder    message=Select a directory
    Directory Should Exist    ${result}
