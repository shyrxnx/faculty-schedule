import customtkinter as ctk


class DeleteSchedFrame(ctk.CTkToplevel):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Delete Schedule")

        # Center the pop-up on the screen
        window_width = 350
        window_height = 100
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Ensure the pop-up is on top
        self.lift()
        self.focus_force()
        self.grab_set()

        # Create a frame for selecting the schedule to delete
        delete_frame = ctk.CTkFrame(self, width=15)
        delete_frame.pack(pady=10, anchor="w", padx=10)

        # Label for Schedule
        ctk.CTkLabel(delete_frame, text="Select Schedule to Delete:", width=180).pack(side="left", padx=0)
        # Dropdown for Schedule
        self.input_schedule = ctk.CTkComboBox(delete_frame, values=["Schedule 1", "Schedule 2", "Schedule 3"])  # Example values, replace with actual schedule list
        self.input_schedule.pack(side="left", padx=10)

        # Delete button centered at the bottom
        delete_button = ctk.CTkButton(self, text="Delete")
        delete_button.pack(pady=10, anchor="center")
