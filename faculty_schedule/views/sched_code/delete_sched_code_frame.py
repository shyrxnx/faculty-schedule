import customtkinter as ctk
from tkinter import messagebox
from ...controllers import ScheduleController


class DeleteSchedCodeFrame(ctk.CTkToplevel):
    def __init__(self, master=None, sched_code = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Delete Schedule Code")
        self.controller = ScheduleController()
        self.sched_code = sched_code.id
        

        # Center the pop-up on the screen
        window_width = 275
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

        # Create a frame for sched code and input
        sched_code_frame = ctk.CTkFrame(self, width=15)
        sched_code_frame.pack(pady=10, anchor="w", padx=10)

        # Label for sched code
        ctk.CTkLabel(sched_code_frame, text=f"Schedule Code: {self.sched_code}", width=100).pack(side="left", padx=0)
        
        # Submit button centered at the bottom
        submit_button = ctk.CTkButton(self, text="Confirm", command=self.confirm)
        submit_button.pack(pady=10, anchor="center")

    def confirm(self):
        try:
            self.controller.delete_schedule(self.sched_code)
            messagebox.showinfo("Success", f"Schedule Code {self.sched_code} deleted successfully!")
            # Refresh the table in the main frame
            self.master.populate_table()
            self.destroy()  # Close the AddEmployeeFrame after success
        except Exception as e:
            messagebox.showerror("Error", str(e))