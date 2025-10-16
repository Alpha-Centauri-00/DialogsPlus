from robot.api.deco import keyword
import os
from DialogsPlus.utils.config import DialogConfig
from DialogsPlus.widgets.wrappers import ( GetValueFromUserDialog, 
                                          ExecuteManualStepDialog, 
                                          CountdownDialogRunner,
                                          GetConfirmationFromUser, 
                                          MultiValueInput)


ROBOT_LIBRARY_SCOPE = 'SUITE'

class DialogsPlus:

    def __init__(self, config=None):
    
        if config and os.path.exists(config):
            self.config = DialogConfig.from_yaml(config)
        else:
            self.config = DialogConfig()  # use defaults

    @keyword
    def say_hello(self, name="World"):
        return f"Hello, {name}!"
    
    @keyword
    def get_value_from_user(self, prompt="Enter value:", default=""):
        return GetValueFromUserDialog.show(prompt,default,config=self.config)

    @keyword
    def run_manual_steps(self, steps):
        ExecuteManualStepDialog.run_steps(steps, config=self.config)

    @keyword
    def count_down(self, seconds):
        CountdownDialogRunner.show(int(seconds), config=self.config)
            
    @keyword
    def get_confirmation(self, message):
        return GetConfirmationFromUser.show(message=message,config=self.config)
    
    @keyword
    def get_multi_value(self, fields, default=None):
        fields_list = fields if isinstance(fields, list) else [fields]
        calculated_height = 150 + (len(fields_list) * 40) + 60
        #max_field_length = max(len(field) for field in fields_list)
        max_field_length = 20
        calculated_width = 300 + (max_field_length * 8)
        self.config.height = calculated_height
        self.config.width = calculated_width
        return MultiValueInput.run_multival(fields=fields,defaults=default,config=self.config)