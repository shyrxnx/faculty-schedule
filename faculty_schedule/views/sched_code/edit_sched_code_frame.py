import customtkinter as ctk
from ...controllers import ScheduleController  # Import your controller here
from tkinter import messagebox
from ...exceptions import ValidationError

class EditSchedCodeFrame(ctk.CTkToplevel):
    def __init__(self, master=None, schedule_id=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.schedule_id = schedule_id
        self.controller = ScheduleController()
        self.title("Edit Schedule Code")

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
        ctk.CTkLabel(code_frame, text="Edit Schedule Code:", width=120).pack(side="left", padx=0)
        # Entry field for Schedule Code
        self.input_code = ctk.CTkEntry(code_frame)
        self.input_code.pack(side="left", padx=10)

        # Create a frame for Subject and input
        subject_frame = ctk.CTkFrame(self, width=15)
        subject_frame.pack(pady=10, anchor="w", padx=10)

        # Label for Subject
        ctk.CTkLabel(subject_frame, text="Edit Subject:", width=120).pack(side="left", padx=0)
        # Entry field for Subject
        self.input_subject = ctk.CTkEntry(subject_frame)
        self.input_subject.pack(side="left", padx=10)

        # Create a frame for Section and input
        section_frame = ctk.CTkFrame(self, width=15)
        section_frame.pack(pady=10, anchor="w", padx=10)

        # Label for Section
        ctk.CTkLabel(section_frame, text="Edit Section:", width=120).pack(side="left", padx=0)
        # Entry field for Section
        self.input_section = ctk.CTkEntry(section_frame)
        self.input_section.pack(side="left", padx=10)

        # Submit button centered at the bottom
        submit_button = ctk.CTkButton(self, text="Submit", command=self.on_submit)
        submit_button.pack(pady=10, anchor="center")

        self.load_existing_schedule()

    def load_existing_schedule(self):
        """Load the existing schedule details into the input fields."""
        # Retrieve schedule data for the given schedule_id
        schedule_data = self.schedule_id
        print(schedule_data)  # Ensure you're getting the correct schedule object
        self.id = schedule_data.id
        if schedule_data:
            # Access the code attribute directly
            self.input_code.insert(0, schedule_data.code)

            # Split the description into subject and section
            description = schedule_data.description
            if " - " in description:
                subject, section = description.split(" - ", 1)  # Split only at the first occurrence of " - "
                self.input_subject.insert(0, subject)  # Fill the subject input
                self.input_section.insert(0, section)  # Fill the section input
            else:
                # If no " - " exists, populate subject and leave section empty
                self.input_subject.insert(0, description)
                self.input_section.insert(0, "")

    def on_submit(self):
        """Handle the submit button click."""
        # Gather data from the input fields
        code = self.input_code.get()
        subject = self.input_subject.get()
        section = self.input_section.get()

        # Prepare data dictionary to pass to the update function
        data = {
            "code": code,
            "description": f"{subject} - {section}",  # Combine subject and section for description
        }

        # Call the update function from the controller
        try:
            updated_schedule = self.controller.update_schedule(self.id, data)
            messagebox.showinfo("Success", "Schedule updated successfully!")
            self.master.populate_table()
            self.destroy()  # Close the edit window after a successful update
        except NotFoundError as e:
            messagebox.showerror("Error", str(e))
        except ValidationError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")