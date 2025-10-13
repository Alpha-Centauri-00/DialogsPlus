*** Settings ***
Library    DialogsPlus    #config=D:/robotframework-dialogsplus/atests/config.yaml
Test Setup    Set Log Level    level=TRACE


*** Variables ***

${username}    user1
${password}    pass1

@{texts}    open window
...         go to github
...         add ${username} and ${password}
...         click of singin
...         check the main window

*** Test Cases ***
new
    VAR        @{mylist}
    ...         go to github
    ...         add username and pass
    ...         click of singin
    ...         check the main window

    @{new_list}    Create List       
    ...         go to github1
    ...         add username and pass1
    ...         click of singin1
    ...         check the main window1

    DialogsPlus.Run Manual Steps    ${texts}

    ${r}    DialogsPlus.Get Value From User    prompt=give me the value you mother fucker!
    DialogsPlus.Run Manual Steps    this is one step
    # Log     i love to travel
    # DialogsPlus.Count Down    10

another
    ${r}    Get Confirmation    message=what are you doing? are you happy?
    IF    ${r} == ${True}
        Should Be True    ${r}

    ELSE IF    ${r} == ${False}
        Should Be Equal    ${r}    ${False}

    ELSE IF    ${r} == ${None}
        Should Be Equal    ${r}    ${None}
    END
    
testing
    ${lis}    Create List    username    password    email    phone
    &{def_val}    Create Dictionary    username=admin    password=P@55
    ${r}    Get Multi Value    ${lis}     default=${def_val}
