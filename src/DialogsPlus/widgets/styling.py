from DialogsPlus.widgets.base import BaseDialog
from robot.errors import ExecutionFailed
from robot.api import logger
import time
import customtkinter as ctk


class InputDialog(BaseDialog):
    
    def __init__(self, prompt, default="", config=None, is_error=False):
        super().__init__(config)
        self.prompt = prompt
        self.default = default
        self.is_error = is_error
    
    def build_ui(self, app):
        frame = ctk.CTkFrame(app, fg_color="transparent")
        frame.pack(pady=8)

        label = self.create_label(frame, text=self.prompt)
        label.pack() 
        entry = self.create_entry(frame)
        entry.insert(0, self.default)
        entry.pack()
        
        def on_submit():
            self.result['value'] = entry.get()
            app.quit()
        
        app.protocol("WM_DELETE_WINDOW", app.quit)
        app.bind('<Return>', lambda e: on_submit())
        app.bind('<Escape>', lambda e: app.quit())
        
        entry.focus_set()
        
        self.create_button(app, text="Submit", command=on_submit).pack()


class ManualStepDialog(BaseDialog):
    
    def __init__(self, message, config=None):
        super().__init__(config)
        self.message = message
    
    def build_ui(self, app):
        def on_pass():
            self.result["status"] = "pass"
            app.quit()

        def on_fail():
            self.result["status"] = "fail"
            app.quit()

        app.protocol("WM_DELETE_WINDOW", app.quit)
        app.bind('<Escape>', lambda e: app.quit())

        self.create_label(app, text=self.message).pack(pady=25)

        button_frame = ctk.CTkFrame(app,fg_color="transparent")
        button_frame.pack(pady=(10, self.config.spacing), expand=True)

        self.create_button(
            button_frame,
            text="PASS",
            command=on_pass).pack(side="left", padx=10)

        self.create_button(
            button_frame,
            text="FAIL",
            command=on_fail).pack(side="left", padx=10)


class CountdownDialog(BaseDialog):
    
    def __init__(self, seconds, message="Please wait...", config=None):
        super().__init__(config)
        self.seconds = seconds
        self.message = message
    
    def build_ui(self, app):
        
        label = self.create_label(app, text="")
        label.place(relx=0.5, rely=0.4, anchor="center")

        progress = ctk.CTkProgressBar(app, width=300, height=12, progress_color="#00c0b5")
        progress.place(relx=0.5, rely=0.8, anchor="center")
        progress.set(0)

        start_time = time.perf_counter()

        def update():
            elapsed = time.perf_counter() - start_time
            remaining = self.seconds - elapsed

            if remaining > 0:
                mins, secs = divmod(int(remaining), 60)
                label.configure(text=f"{self.message}\n{mins:02}:{secs:02}")
                progress.set(min(elapsed / self.seconds, 1))
                app.after(100, update)
            else:
                progress.set(1)
                label.configure(text=f"{self.message}\n00:00")
                app.quit()

        update()


# Static methods for backwards compatibility / convenience
class GetValueFromUserDialog:
    @staticmethod
    def show(prompt="Enter value:", default="", config=None):
        dialog = InputDialog(prompt, default, config)
        return dialog.show().get('value')


class ExecuteManualStepDialog:
    @staticmethod
    def show(message="Please perform the step and confirm.", config=None):
        logger.info(message)
        
        dialog = ManualStepDialog(message, config)
        result = dialog.show()

        if result.get("status") == "pass":
            return
        else:
            failure_dialog = InputDialog("Test Failed - Reason:", "", config, is_error=True)
            reason = failure_dialog.show().get('value', 'No reason provided')
            logger.error(f"{message} | Reason: {reason}")
            raise ExecutionFailed(reason)

    @staticmethod
    def run_steps(steps, config=None):
        if isinstance(steps, str):
            ExecuteManualStepDialog.show(steps, config)
        elif isinstance(steps, list):
            for step in steps:
                ExecuteManualStepDialog.show(step, config)
        else:
            raise ExecutionFailed("Invalid input: must be a string or a list of strings.")


class CountdownDialogRunner:
    @staticmethod
    def show(seconds=10, message="Please wait...", config=None):
        logger.info(f"Starting countdown for {seconds} seconds...")
        dialog = CountdownDialog(seconds, message, config)
        dialog.show()


class ConfirmationDialog(BaseDialog):
    def __init__(self, message, default="Yes", config=None):
        super().__init__(config)
        self.message = message
        self.default = default
    
    def build_ui(self, app):
        # Build UI here
        # Create label with message
        # Create 3 buttons
        # Set result based on which button clicked

        def on_yes():
            self.result["status"] = "yes"
            app.quit()

        def on_no():
            self.result["status"] = "no"
            app.quit()

        def on_cancel():
            self.result["status"] = "cancel"
            app.quit()

        app.protocol("WM_DELETE_WINDOW", app.quit)
        app.bind('<Escape>', lambda e: app.quit())

        self.create_label(app, text=self.message).pack(pady=25)

        button_frame = ctk.CTkFrame(app,fg_color="transparent")
        button_frame.pack(pady=(10, self.config.spacing), expand=True)

        self.create_button(
            button_frame,
            text="Yes",
            command=on_yes).pack(side="left", padx=5)

        self.create_button(
            button_frame,
            text="No",
            command=on_no).pack(side="left", padx=5)

        self.create_button(
            button_frame,
            text="Cancel",
            command=on_cancel).pack(side="left", padx=5)
        

class GetConfirmationFromUser:
    @staticmethod
    def show(message="Are you sure?", default="Yes", config=None):
        logger.info(message)
        dialog = ConfirmationDialog(message, default, config)
        dialog.config.width = 450
        result = dialog.show().get("status")
        
        if result == "yes":
            return True
        elif result == "no":
            return False
        else:  # cancel
            return None
        


class MultiValueInputDialog(BaseDialog):
    def __init__(self, fields, defaults=None, config=None):
        super().__init__(config)

        # Normalize string input to list
        self.fields = fields if isinstance(fields, list) else [fields]
        self.defaults = defaults or {}
        self.entries = {}

    def build_ui(self, app):
        def on_submit():
            self.result = {field: self.entries[field].get() for field in self.fields}
            self.result["status"] = "pass"
            app.quit()

        def on_cancel():
            self.result["status"] = "fail"
            app.quit()

        app.protocol("WM_DELETE_WINDOW", on_cancel)
        app.bind('<Escape>', lambda e: on_cancel())
        app.bind('<Return>', lambda e: on_submit())

        main_frame = ctk.CTkFrame(app, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        title = self.create_label(main_frame, text="Enter values")
        title.pack(pady=25)

        fields_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        fields_frame.pack(fill="both", expand=True)

        for field in self.fields:
            row_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)

            label = self.create_label(row_frame, text=field)
            label.pack(side="left", padx=(0, 10))

            entry = self.create_entry(row_frame)
            entry.insert(0, self.defaults.get(field, ""))
            entry.pack(side="left", fill="x", expand=True)

            self.entries[field] = entry

        # Buttons
        button_frame = ctk.CTkFrame(app, fg_color="transparent")
        button_frame.place(relx=0.5, rely=0.8, anchor="center")

        submit_btn = self.create_button(button_frame, text="Submit", command=on_submit)
        submit_btn.pack(side="left", padx=5)

        cancel_btn = self.create_button(button_frame, text="Cancel", command=on_cancel)
        cancel_btn.pack(side="left", padx=5)


class MultiValueInput:
    @staticmethod
    def show(fields, defaults=None, config=None):
        logger.info(f"Showing input dialog for: {fields}")
        dialog = MultiValueInputDialog(fields, defaults=defaults, config=config)
        result = dialog.show()
        if result.get("status") == "pass":
            return result
        else:
            return None

    @staticmethod
    def run_multival(fields, config=None, defaults=None):
        return MultiValueInput.show(fields, defaults=defaults, config=config)


# def run_multi():
#     fields = ['username', 'password', 'email','phone']
#     defaults = {'username': 'admin'}
#     result = MultiValueInput.run_multival(fields, defaults=defaults)
#     print("User Input:", result)


# if __name__ == "__main__":
#     run_multi()