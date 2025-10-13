# DialogsPlus
A drop-in enhancement for Robot Framework's Dialogs library with modern UI and extended user interaction keywords.

### ⚠️ Known Limitations

- Not supported in headless environments such as CI/CD pipelines (e.g., Jenkins, GitHub Actions)


## TODOs / Roadmap

- [✅] Get Secure Input From User
    - [✅] Like Get Value From User 
    - [❌] masks input (for passwords, tokens). Optional: hide/show toggle for user.

- [❌] Get Multi-Value Input
    - One dialog to get several values (name, email, password, etc.).
    - Returns a dictionary or list of values.

- [❌] Confirm With Checkbox
    - Instead of just yes/no, show checkboxes: “I accept the terms”, etc.
    - Useful for test prompts that require confirmation steps.

- [❌] Show HTML Message
    - Display rich text or simple HTML (bold, links, colors).
    - Useful for stylized instructions or alerts.

- [❌] Choose From File Dialog
    - Opens file picker to let user select a file (or multiple).
    - Returns file path(s).

- [❌] Choose Folder
    - Opens folder selection dialog.
    - Useful for directory inputs.

- [❌] Conditional Pause
    - Pause only if certain variable or condition is met.

- [❌]  Live Variable Inspector
    - Display current Robot variables in a pop-up during test.

- [✅] Execute Manual StepS

    ```bash
    @{steps}=    Create List
    ...    1. Go to toilet
    ...    2. open cover
    ...    3. make some shit
    ...    4. clean yourself
    ...    5. flush

    Execute Manual Steps
    ...    message=${steps}
    ...    log=warning
    ...    title=Firewall Setup Warning
    ...    buttons=Continue    Abort

    ```

- [❌] Get Confirmation From User

    ```bash
    ${answer}=    Get Confirmation From User
    ...    message=Do you want to shit now?
    ...    default=Yes
    ...    timeout=30s
    ```

- [❌] Get Date From User
    - Useful in business/testing apps.
    - Can return the selected date in a specific format (e.g., YYYY-MM-DD).

- [✅] Display Timer Dialog
    - Used in time-boxed manual tests.
    - Could auto-close or proceed after timeout.

    ```bash
    Display Timer Dialog
    ...    duration=10s
    ...    message=Prepare for next step
    ...    auto_continue=True

    ```

- [✅] change theme using yaml file
    ```
    Library    DialogsPlus    config=D:/path/to/your/config.yaml
    ```

## Next steps:
    - Get Confirmation From User ← Do this next (super simple, high value)
    - Get Multi-Value Input ← Second (medium complexity, high value)
    - Choose From File Dialog ← Third (easy, built-in tkinter)
    - Choose Folder ← Fourth (easy, built-in tkinter)
    - Get Date From User ← Fifth (medium, nice to have)
    - Confirm With Checkbox ← Sixth (medium)
    - Get Secure Input mask/toggle ← Finish Get Secure Input
    
### 🤝 Contributing

Pull requests are welcome! More info coming soon.