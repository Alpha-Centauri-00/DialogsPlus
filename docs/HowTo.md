# 📘 DialogsPlus Documentation

DialogsPlus is an extended UI/dialog library for Robot Framework, designed to interactively collect user inputs, confirmations, file/folder selections, and control test execution flow with dialogs.

This document describes the available keywords and provides usage examples.

# 🔧 Configuration
Before using the library, you can specify an optional YAML config:

```bach
*** Settings ***
Library    DialogsPlus    #config=path/to/config.yaml
```
Optional config file allows customization of:

- Theme colors

- Font sizes

- Window dimensions

- Padding
```yaml
title: "Custom Dialog"
width: 400
height: 200
theme: "green"
appearance_mode: "light"
button_fg_color: "#aaa"
etc...
```

## 🧩 Keywords Overview

🧾 `Get Value From User Input`
Prompts the user for a single line of text input.

```r
${result}          Get Value From User Input    prompt=Enter your name:    default=Robot framework
Should Be Equal    ${result}    Robot framework
```

📝 `Run Manual Steps`
Displays manual test steps with Pass/Fail buttons.

```r
${steps}    Create List    
...         01 Open the app    
...         02 Click Start button    
...         03 Verify status

Run Manual Steps    ${steps}
# Or One Test Step as normal text:
Run Manual Steps    Open Google
```
⏳ `Count Down`
Shows a countdown timer dialog that automatically closes.
```r
Count Down    5
```
❓ `Get Confirmation` Displays a Yes / No / Cancel dialog.
```r
${result}    Get Confirmation    Are you sure?
Should Be True    ${result}
```
🧮 `Get Multi Value` Prompts for multiple input fields in a single dialog.
```r
*** Test Cases ***
Get Value Test
    ${result}    Get Multi Value    username
    Should Be Equal    ${result}[username]    user1

    # Or another approach, with more fields!

*** Variables ***
@{fields_val}     username    password    email    phone
&{default_val}    username=admin    password=P@55    phone=1234567

*** Test Cases ***
Get Multi Value Multiple Fields
    ${result}    Get Multi Value    ${fields_val}    default=${default_val}
    Should Be Equal    ${result}[password]    P@55
    Should Be Equal    ${result}[phone]       1234567
```
📄 `Choose File` Opens a native file picker dialog and Returns file **PATH** as a string.
```r
Choose Single XML File
    ${XML_FILETYPES}    Evaluate    [("xml files", "*.xml")]    # [("Text files", "*.txt")]
    ${result}=    Choose File    
    ...           message=Select Single XML File    
    ...           filetypes=${XML_FILETYPES}

    # Or another approach, with many files path and return as a list[str]!

Choose Multiple HTML Files
    ${HTML_FILETYPES}    Evaluate    [("HTML", "*.html")]
    ${result}=    Choose File    
    ...           message=Select Multiple HTML Files    
    ...           filetypes=${HTML_FILETYPES}   multiple=True
    Should Contain    ${result}[0]    .html
```
📁 `Choose Folder` Opens a folder selection dialog.
```r
${dir}    Choose Folder    message=Select output directory
Directory Should Exist    ${dir}
```
✅ `Confirm With Checkbox` Prompts the user to confirm an action with a checkbox.
```r
Select Single CheckBox
    ${confirmed}    Confirm With Checkbox    
        ...         message=Accept terms?    
        ...         checkbox_text=I accept
    Should Be True    ${confirmed}  

    # Or with many checkboxes

*** Variables ***
@{fields_val}     username    password    email    phone

*** Test Cases ***
Select Many Checkbox Test
    ${r}    Select Options With Checkboxes    
    ...    message=Select as much as you want   
    ...    options=${fields_val}

    Should Not Be True    ${r}[username]
    Should Not Be True    ${r}[password]
    Should Not Be True    ${r}[email]
    Should Not Be True    ${r}[phone]

    # Another example with default checkboxes checked!

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
```
⏸️ `Pause Test Execution` Pauses the test run and waits for the user to click "Continue".
```r
Pause Test Execution    message=Manually verify system state
```