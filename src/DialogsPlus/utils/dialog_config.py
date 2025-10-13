# dialog_config.py

import yaml

class DialogConfig:
    def __init__(
        self,
        title="Robot Framework",
        width=400,
        height=150,
        theme="blue",
        appearance_mode="system",

        button_width=120,
        button_height=32,
        label_font=("Arial", 12),
        entry_width= 200,
        entry_height=28,
        spacing=10,
        button_fg_color="#06bdb1"
    ):
        self.title = title
        self.width = width
        self.height = height
        self.theme = theme
        self.appearance_mode = appearance_mode

        # New UI element configs
        self.button_width = button_width
        self.button_height = button_height
        self.label_font = label_font
        self.entry_width = entry_width
        self.entry_height = entry_height
        self.spacing = spacing
        self.button_fg_color=button_fg_color
        

    @classmethod
    def from_yaml(cls, path: str):
        print(f"[DEBUG] Received config path: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls(
            title=data.get("title", "Dialog"),
            width=data.get("width", 300),
            height=data.get("height", 150),
            theme=data.get("theme", "blue"),
            appearance_mode=data.get("appearance_mode", "system"),

            button_width=data.get("button_width", 120),
            button_height=data.get("button_height", 32),
            label_font=tuple(data.get("label_font", ("Arial", 12))),
            entry_height=data.get("entry_height", 28),
            entry_width=data.get("entry_width",60),
            spacing=data.get("spacing", 10),
            button_fg_color=data.get("button_fg_color", "#06bdb1")
        )

    # def center_window(self, app, scaling):
    #     app.update_idletasks()
    #     screen_width = app.winfo_screenwidth()
        
    #     screen_width = app.winfo_screenwidth()
    #     screen_height = app.winfo_screenheight()
    #     x = int(((screen_width / 2) - (self.width / 2)) * scaling)
    #     y = int(((screen_height / 2) - (self.height / 2)) * scaling)
    #     app.geometry(f"{self.width}x{self.height}+{x}+{y}")
