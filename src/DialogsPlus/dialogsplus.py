from robot.api.deco import keyword
from typing import Any, Dict, List, Union, Optional
import copy
import os
from DialogsPlus.utils.config import DialogConfig
from DialogsPlus.widgets.wrappers import (
    GetValueFromUserDialog, 
    ExecuteManualStepDialog, 
    CountdownDialogRunner,
    GetConfirmationFromUser, 
    MultiValueInput,
    ChooseFromFileDialog,
    ChooseFolderDialog,
    ConfirmWithCheckbox,
    SelectOptionsWithCheckboxes,
    PauseExecution
)


ROBOT_LIBRARY_SCOPE = 'SUITE'

class DialogsPlus:
    """
    DialogsPlus is a modern, customizable drop-in enhancement for Robot Framework’s Dialogs library, built on top of customtkinter.

    This library extends standard dialog capabilities with stylish and user-friendly GUI dialogs, supporting customization of colors, fonts, and sizes via an external config.yaml file.

    Features:
        - Easy-to-use dialogs for interactive test runs.
        - Full GUI interface using customtkinter.
        - Customizable appearance (colors, fonts, sizes, etc.) through config.yaml.
        - Dynamic sizing based on user input or options.
        - Drop-in replacement for Robot Framework’s standard Dialogs library.

    Note:
        - Not supported in headless environments (e.g., CI/CD pipelines like Jenkins or GitHub Actions).

    DialogsPlus is ideal for enhancing user interactions in Robot Framework tests with modern UI elements and extended keyword support.
    """

    def __init__(self, config: Optional[str] = None):
        """Initialize DialogsPlus library with optional YAML config file."""
        if config and os.path.exists(config):
            self.config = DialogConfig.from_yaml(config)
        else:
            self.config = DialogConfig()

    @keyword
    def get_value_from_user_input(self, prompt: str = "Enter value:", default: str = "") -> Optional[str]:
        """Prompts user for text input via dialog.
        
        Arguments:
            - prompt: Text displayed above input field
            - default: Pre-filled value
        
        Returns string input or None if cancelled.
        """
        return GetValueFromUserDialog.show(prompt, default, config=self.config)

    @keyword
    def run_manual_steps(self, *steps) -> None:
        """Displays manual test steps with Pass/Fail buttons.

        Arguments:
            - steps: One step per argument (e.g. `open github    add username    add password`),
              or a single list/string variable (e.g. `${steps}`)

        Raises ExecutionFailed if user clicks Fail button.
        """
        if len(steps) == 1 and isinstance(steps[0], list):
            steps_list = steps[0]
        else:
            steps_list = list(steps)
        ExecuteManualStepDialog.run_steps(steps_list, config=self.config)

    @keyword
    def count_down(self, seconds: Union[int, str]) -> None:
        """Shows countdown timer dialog.
        
        Arguments:
            - seconds: Duration in seconds
        
        Dialog closes automatically when timer reaches zero.
        """
        CountdownDialogRunner.show(int(seconds), config=self.config)

    @keyword
    def get_confirmation(self, message: str) -> Optional[bool]:
        """Shows Yes/No/Cancel confirmation dialog.
        
        Arguments:
            - message: Question or prompt text
        
        Returns True for Yes, False for No, None for Cancel.
        """
        return GetConfirmationFromUser.show(message=message, config=self.config)

    @keyword
    def get_multi_value(self, fields: Union[str, List[str]], default: Optional[Dict[str, str]] = None) -> Optional[Dict[str, str]]:
        """Prompts user for multiple input values in one dialog.
        
        Arguments:
            - fields: List of field names or single field
            - default: Dictionary of default values per field
        
        Returns dictionary with field names as keys and user inputs as values, or None if cancelled.
        """
        fields_list = fields if isinstance(fields, list) else [fields]
        calculated_height = 150 + (len(fields_list) * 40) + 60
        max_field_length = 20
        calculated_width = 300 + (max_field_length * 8)
        self.config.height = calculated_height
        self.config.width = calculated_width
        return MultiValueInput.run_multival(fields=fields, defaults=default, config=self.config)

    @keyword
    def choose_file(self, message: str = "", filetypes: Optional[List[tuple]] = None, multiple: bool = False) -> Optional[Union[str, List[str]]]:
        """Opens file picker dialog.
        
        Arguments:
            - message: Instruction text
            - filetypes: List of (description, pattern) tuples, e.g. [("Text files", "*.txt")]
            - multiple: Allow selecting multiple files
        
        Returns file path string, list of paths if multiple=True, or None if cancelled.
        """
        return ChooseFromFileDialog.show(message, filetypes, multiple, self.config)

    @keyword
    def choose_folder(self, message: str) -> Optional[str]:
        """Opens folder picker dialog.
        
        Arguments:
            - message: Instruction text
        
        Returns folder path string or None if cancelled.
        """
        return ChooseFolderDialog.show(message, self.config)

    @keyword
    def confirm_with_checkbox(self, message: str, checkbox_text: str = "I agree") -> bool:
        """Shows confirmation dialog with checkbox.
        
        Arguments:
            - message: Prompt text
            - checkbox_text: Label for checkbox
        
        Returns True if checkbox was checked, False otherwise.
        """
        return ConfirmWithCheckbox.show(message, checkbox_text, self.config)

    @keyword
    def select_options_with_checkboxes(self, message: str, options: Union[str, List[str]], defaults: Optional[List[str]] = None) -> Dict[str, bool]:
        """Shows multiple checkboxes for selection.
        
        Arguments:
            - message: Instruction text
            - options: List of options or pipe-separated string
            - defaults: List of pre-selected option names
        
        Returns dictionary with option names as keys and True/False as values.
        """
        options_list = options if isinstance(options, list) else options.split('|')
        
        num_options = len(options_list)
        max_option_length = max(len(opt) for opt in options_list)
        message_length = len(message)
        
        calculated_height = 180 + (num_options * 40)
        width_from_message = min(600, max(300, message_length * 7))
        width_from_options = max(300, 200 + (max_option_length * 8))
        calculated_width = max(width_from_message, width_from_options)
        
        self.config.height = calculated_height
        self.config.width = calculated_width
        
        return SelectOptionsWithCheckboxes.show(message, options, defaults, self.config)
    

    @keyword
    def pause_test_execution(self, message: str = "Test execution paused", command: Optional[str] = None, command_args: Optional[List[str]] = None) -> None:
        """Pauses test execution until user clicks Continue.

        Arguments:
            - message: Text displayed in dialog
            - command: Optional keyword name. When given, an extra "Run" button is shown
              next to Continue that runs it via Robot Framework's Run Keyword, so it must
              be a keyword already available in the running suite (user keyword, resource
              file, or imported library) - can be clicked any number of times while paused.
            - command_args: Optional list of arguments passed to that keyword

        Test resumes when user clicks Continue button.

        Raises ExecutionFailed if the most recent "Run" click failed (e.g. the keyword
        doesn't exist or raised an error).
        """
        config = self.config
        if command:
            config = copy.copy(self.config)
            config.height = max(self.config.height, 260)
        PauseExecution.show(message, command, command_args, config)