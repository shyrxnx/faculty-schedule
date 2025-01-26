import customtkinter as ctk


class AddSchedCodeFrame(ctk.CTkToplevel):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Add Schedule Code")

        # Center the pop-up on the screen
        window_width = 300
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Ensure the pop-up is on top
        self.lift()
        self.focus_force()
        self.grab_set()

        # Create a frame for Schedule Code and input
        code_frame = ctk.CTkFrame(self, width=15)
        code_frame.pack(pady=10, anchor="w", padx=10)

        # Label for Schedule Code
        ctk.CTkLabel(code_frame, text="Enter Schedule Code:", width=120).pack(side="left", padx=0)
        # Entry field for Schedule Code
        self.input_code = ctk.CTkEntry(code_frame)
        self.input_code.pack(side="left", padx=10)

        # Create a frame for Subject and input
        subject_frame = ctk.CTkFrame(self, width=15)
        subject_frame.pack(pady=10, anchor="w", padx=10)

        # Label for Subject
        ctk.CTkLabel(subject_frame, text="Enter Subject:", width=120).pack(side="left", padx=0)
        # Entry field for Subject
        self.input_subject = ctk.CTkEntry(subject_frame)
        self.input_subject.pack(side="left", padx=10)

        # Create a frame for Section and input
        section_frame = ctk.CTkFrame(self, width=15)
        section_frame.pack(pady=10, anchor="w", padx=10)

        # Label for Section
        ctk.CTkLabel(section_frame, text="Enter Section:", width=120).pack(side="left", padx=0)
        # Entry field for Section
        self.input_section = ctk.CTkEntry(section_frame)
        self.input_section.pack(side="left", padx=10)

        # Submit button centered at the bottom
        submit_button = ctk.CTkButton(self, text="Submit")
        submit_button.pack(pady=10, anchor="center")
