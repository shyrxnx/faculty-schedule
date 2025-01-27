import customtkinter as ctk
from tkinter import messagebox
from ...controllers.employee_controller import EmployeeController  # Import your controller here

class EditEmployeeFrame(ctk.CTkToplevel):
    def __init__(self, master=None, selected_employee=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = EmployeeController()
        self.selected_employee = selected_employee  # Store the selected employee
        self.title("Edit Employee")

        # Center the pop-up on the screen
        window_width = 275
        window_height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Ensure the pop-up is on top
        self.lift()
        self.focus_force()
        self.grab_set()

        # Create a frame for name and input
        name_frame = ctk.CTkFrame(self, width=15)
        name_frame.pack(pady=10, anchor="w", padx=10)

        # Label for name
        ctk.CTkLabel(name_frame, text="Edit name:", width=100).pack(side="left", padx=0)
        # Entry field for name
        self.input_name = ctk.CTkEntry(name_frame)
        self.input_name.pack(side="left", padx=10)

        # Create a frame for id and input
        emp_id_frame = ctk.CTkFrame(self, width=15)
        emp_id_frame.pack(pady=10, anchor="w", padx=10)

        # Label for id
        ctk.CTkLabel(emp_id_frame, text="Edit id:", width=100).pack(side="left", padx=0)
        # Entry field for id
        self.input_id = ctk.CTkEntry(emp_id_frame)
        self.input_id.pack(side="left", padx=10)

        if self.selected_employee:
            self.input_id.insert(0, str(self.selected_employee.id))
            self.input_name.insert(0, str(self.selected_employee.name))

        # Submit button centered at the bottom
        submit_button = ctk.CTkButton(self, text="Submit",command=self.submit_changes)
        submit_button.pack(pady=10, anchor="center")


    def submit_changes(self):
        """Handle the submission of changes."""
        name = self.input_name.get().strip()
        emp_id = self.input_id.get().strip()

        # Validate input
        if not name or not emp_id.isdigit():
            messagebox.showerror("Error", "Please enter valid name and ID.")
            return

        # Convert ID to integer
        emp_id = int(emp_id)

        # Update the employee with the new name and ID
        try:
            updated_employee = self.controller.update_employee(self.selected_employee.id, {'name': name})
            updated_employee.id = emp_id  # Directly set the new ID
            self.selected_employee = updated_employee  # Update the selected employee instance

            messagebox.showinfo("Success", f"Employee {name} has been updated.")
            # Refresh the table in the main frame
            self.master.populate_table()
            self.destroy()  # Close the window after saving the changes
        except Exception as e:
            messagebox.showerror("Error", str(e))