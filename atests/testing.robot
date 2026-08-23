*** Settings ***
Library           DialogsPlus    #config=D:/robotframework-dialogsplus/atests/config.yaml
Library           OperatingSystem

# Suite Setup       Set Log Level    level=TRACE
# Test Setup        Log Test Case Name


*** Keywords ***
Log Test Case Name
    [Tags]    robot:flatten
    Log    <p style="background-color: #06bdb1; font-weight: bold; display: inline-block; padding: 4px;">*** Running Test: ${TEST NAME} ***</p>    html=${True}

log Hello
    Log     Hello    level=WARN

*** Variables ***

@{fields_val}     username    password    email    phone
@{fields}         username    password
&{default_val}    username=admin    password=P@55    phone=1234567
&{default}        username=user1    password=P@55

*** Test Cases ***

Get Value From User Default
    ${result}    Get Value From User Input   
    ...    prompt=Enter your name:    
    ...    default=Robot framework
    
    Should Be Equal    ${result}    Robot framework

Run Manual Steps Executes
    VAR    @{steps}        
    ...    Open the app    
    ...    Click Start button    
    ...    Verify status

    Run Manual Steps    ${steps}
    Log    Manual steps executed successfully

Run Manual Steps Executes With Plain Args
    Run Manual Steps    
    ...                open github    
    ...                add username    
    ...                add password    
    ...                press login

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

Choose Single XML File
    ${XML_FILETYPES}    Evaluate    [("xml files", "*.xml")]
    ${result}=    Choose File    
    ...    message=Select Single XML File    
    ...    filetypes=${XML_FILETYPES}
    
    Should Contain    ${result}    .xml

Choose Multiple HTML Files
    ${HTML_FILETYPES}    Evaluate    [("HTML", "*.html")]
    ${result}=    Choose File    
    ...    message=Select Multiple HTML Files    
    ...    filetypes=${HTML_FILETYPES}   multiple=True

    Should Contain    ${result}[0]    .html

Choose Folder Test
    ${result}=    Choose Folder    message=Select Any Directory
    Directory Should Exist    ${result}

Single Ceckbox Test
    ${r}    Confirm With Checkbox    
    ...    message=Do you accept the terms?    
    ...    checkbox_text=I accept, no matter what!

    Should Be True    ${r}

Select Many Checkbox Test
    ${r}    Select Options With Checkboxes    
    ...    message=Select as much as you want   
    ...    options=${fields_val}

    Should Not Be True    ${r}[username]
    Should Not Be True    ${r}[password]
    Should Not Be True    ${r}[email]
    Should Not Be True    ${r}[phone]

Select Many Checkbox With Defaults Test
    @{Contacts}    Create List        Email    SMS    Phone    Slack    Discord
    @{Selected_Defaults}    Create List    Email    SMS
    ${selected}=    Select Options With Checkboxes
    ...    message=Choose your preferences
    ...    options=${Contacts}
    ...    defaults=@{Selected_Defaults}         # Default Selected!
    
    Should Be True        ${selected}[Email]
    Should Be True        ${selected}[SMS]
    Should Not Be True    ${selected}[Phone]
    Should Not Be True    ${selected}[Slack]
    Should Not Be True    ${selected}[Discord]

Pause The Test
    Pause Test Execution    message=Check If System Is Running!

Pause The Test With Command
    Pause Test Execution    message=Check If System Is Running!    command=log Hello

Pause The Test With Command That Opens A Dialog
    @{args}    Create List    2
    Pause Test Execution
    ...    message=Check If System Is Running!
    ...    command=Count Down
    ...    command_args=${args}

Pause The Test With Command That Fails
    TRY
        Pause Test Execution    message=Click Run, then Continue    command=Not Exist Keyword
    EXCEPT    AS    ${error}
        Log    Caught expected failure: ${error}
    END

Create Dialog With Text Box And Checkbox
    Create Dialog    title=Login Form
    Add Text Box    name=username    label=Username    default=admin
    Add Checkbox    name=remember_me    label=Remember Me
    Add Button    text=OK
    Add Button    text=Cancel
    ${result}    Show Dialog
    Log    Button clicked: ${result}[button]
    Log    Username: ${result}[username]
    Log    Remember me: ${result}[remember_me]


Create Dialog With Side Command Button
    Create Dialog    title=Diagnostics
    Add Label    text=Run diagnostics before continuing if you like.
    Add Button    text=Run Diagnostics    command=log Hello    closes_dialog=False
    Add Button    text=OK
    ${result}    Show Dialog
    Should Be Equal    ${result}[button]    OK

Add Text Box Fails Without Create Dialog First
    TRY
        Add Text Box    name=orphan
    EXCEPT    AS    ${error}
        Log    Caught expected failure: ${error}
    END

Create Dialog Fails Without A Closing Button
    Create Dialog    title=No Closing Button
    Add Label    text=This has no OK/Cancel button
    TRY
        Show Dialog
    EXCEPT    AS    ${error}
        Log    Caught expected failure: ${error}
    END

Create Dialog With Masked Text Box
    Create Dialog    title=Login Form
    Add Text Box    name=username    label=Username    default=admin
    Add Text Box    name=password    label=Password    mask=True
    Add Button    text=OK
    ${result}    Show Dialog

Create Dialog With Radio Group
    Create Dialog    title=Test Result
    Add Radio Group    name=verdict    label=Verdict    options=Pass|Fail|Blocked    default=Pass
    Add Button    text=OK
    ${result}    Show Dialog
    Should Contain    ${{['Pass', 'Fail', 'Blocked']}}    ${result}[verdict]
    Log    Verdict selected: ${result}[verdict]

Add Radio Group Fail and Pass
    Create Dialog    title=Verdict
    Add Radio Group    name=verdict    options=Pass|Fail    default=Pass
    Add Button    text=OK
    ${result}    Show Dialog
    Should Be Equal    ${result}[verdict]    Pass

Create Dialog With Dropdown
    Create Dialog    title=Browser Selection
    Add Dropdown    name=browser    label=Browser    options=Chrome|Firefox|Edge    default=Firefox
    Add Button    text=OK
    ${result}    Show Dialog
    Log    Browser selected: ${result}[browser]

Add Dropdown Fails With Bad Default
    Create Dialog    title=Bad Dropdown Default
    TRY
        Add Dropdown    name=browser    options=Chrome|Firefox    default=Safari
    EXCEPT    AS    ${error}
        Log    Caught expected failure: ${error}
    END
    Add Dropdown    name=browser    options=Chrome|Firefox    default=Chrome
    Add Button    text=OK
    ${result}    Show Dialog
    Should Be Equal    ${result}[browser]    Chrome