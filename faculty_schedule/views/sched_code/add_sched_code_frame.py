import customtkinter as ctk
from ...controllers import ScheduleController  # Import your controller here
from tkinter import messagebox
from ...exceptions import ValidationError




class AddSchedCodeFrame(ctk.CTkToplevel):
    def __init__(self, master=None, id= None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Add Schedule Code")
        self.id = id
        self.schedule_controller = ScheduleController()
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
        submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_schedule)
        submit_button.pack(pady=10, anchor="center")

    def submit_schedule(self):
        # Retrieve input values
        schedule_code = self.input_code.get()
        subject = self.input_subject.get()
        section = self.input_section.get()

        if not schedule_code or not subject or not section:
            ctk.CTkMessageBox(title="Error", message="All fields are required!")
            return

        # Prepare data for creating the schedule
        data = {
            'employee_id': self.id,  # Replace with actual employee ID
            'code': schedule_code,
            'description': f"{subject} - {section}"  # Or however you want to format the description
        }

        try:
            # Create the schedule using the controller
            new_schedule = self.schedule_controller.create_schedule(data)
            messagebox.showinfo(title="Success", message=f"Schedule {new_schedule.code} added successfully!")
            self.master.populate_table()
            self.destroy()  # Close the window after successful submission
        except ValidationError as e:
            messagebox.showerror("Error", str(e))
        
