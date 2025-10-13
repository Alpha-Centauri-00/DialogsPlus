import customtkinter as ctk
from DialogsPlus.utils.dialog_config import DialogConfig
import os

class BaseDialogRunner:
    _theme_initialized = False
    
    @staticmethod
    def _center_window(app, config):
        app.update_idletasks()
        
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        
        x = (screen_width - config.width) // 2
        y = (screen_height - config.height) // 2       
        app.geometry(f"{config.width}x{config.height}+{x}+{y}")
    
    @staticmethod
    def create_app(config: DialogConfig):
        # Initialize theme once on first dialog creation
        if not BaseDialogRunner._theme_initialized:
            ctk.set_appearance_mode(config.appearance_mode)
            ctk.set_default_color_theme(config.theme)
            BaseDialogRunner._theme_initialized = True
        
        app = ctk.CTk()
        app.title(config.title)

        icon_path = os.path.join(os.path.dirname(__file__), "assets", "robot.ico")
        try:
            app.iconbitmap(icon_path)
        except (FileNotFoundError, Exception):
            pass

        BaseDialogRunner._center_window(app, config)
        return app

    @staticmethod
    def run_dialog(ui_builder_func, config: DialogConfig):
        app = BaseDialogRunner.create_app(config)
        ui_builder_func(app)
        app.mainloop()
        
        app.withdraw()
        
        try:
            after_ids = app.tk.call('after', 'info')
            for after_id in after_ids:
                try:
                    app.after_cancel(after_id)
                except:
                    pass
        except:
            pass
        
        app.update_idletasks()
        
        try:
            app.quit()
        except:
            pass
        
        try:
            app.destroy()
        except:
            pass


class BaseDialog:
    
    def __init__(self, config=None):
        self.config = config if config else DialogConfig()
        self.result = {}
    
    def create_button(self, parent, text, command, **kwargs):
        """Create a button with consistent styling from config"""
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=("Courier New", 16, "bold"),
            fg_color=self.config.button_fg_color,
            text_color="black",                    # Set button text color to black
            hover_color=kwargs.get('hover_color', "#06bdb1"),  # Change hover background color (use any color you want)
            width=kwargs.get('width', self.config.button_width),
            height=kwargs.get('height', self.config.button_height),
            **{k: v for k, v in kwargs.items() if k not in ['width', 'height', 'hover_color']}
        )
    
    def create_label(self, parent, text, **kwargs):
        """Create a label with consistent styling from config"""
        
        # Font configuration
        font_family = kwargs.get('font_family', "Courier New")
        font_size = kwargs.get('font_size', 16)
        font_weight = kwargs.get('font_weight', "bold")
        font = (font_family, font_size, font_weight)

        return ctk.CTkLabel(
            parent,
            text=text,
            font=font,
            text_color=kwargs.get('text_color', "black"),
            anchor=kwargs.get('anchor', "center"),  # Default anchor
            justify=kwargs.get('justify', "left"),  # Text justification
            wraplength=kwargs.get('wraplength', 0),  # 0 = no wrap
            **{k: v for k, v in kwargs.items() if k not in ['font_family', 'font_size', 'font_weight', 'text_color', 'anchor', 'justify', 'wraplength']}
        )


# testing this shit
    
    def show(self):
        def ui(app):
            self.build_ui(app)
        
        BaseDialogRunner.run_dialog(ui, self.config)
        return self.result
    
    def build_ui(self, app):
        raise NotImplementedError