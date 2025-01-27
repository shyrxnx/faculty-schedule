import customtkinter as ctk
from tkinter import messagebox
from ...controllers.employee_controller import EmployeeController  # Import your controller here

class AddEmployeeFrame(ctk.CTkToplevel):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Input Box")
        self.controller = EmployeeController()  # Initialize the controller here
        
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
        ctk.CTkLabel(name_frame, text="Enter name:", width=100).pack(side="left", padx=0)
        # Entry field for name
        self.input_name = ctk.CTkEntry(name_frame)
        self.input_name.pack(side="left", padx=10)

        # Create a frame for id and input
        emp_id_frame = ctk.CTkFrame(self, width=15)
        emp_id_frame.pack(pady=10, anchor="w", padx=10)

        # Label for id
        ctk.CTkLabel(emp_id_frame, text="Enter id:", width=100).pack(side="left", padx=0)
        # Entry field for id
        self.input_id = ctk.CTkEntry(emp_id_frame)
        self.input_id.pack(side="left", padx=10)

        # Submit button centered at the bottom
        submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_data)
        submit_button.pack(pady=10, anchor="center")

    

    def submit_data(self):
        """Handles the Submit button click to add a new employee."""
        name = self.input_name.get().strip()
        emp_id = self.input_id.get().strip()

        if not name or not emp_id:
            messagebox.showerror("Input Error", "Both Name and ID fields are required!")
            return

        try:
            emp_id = int(emp_id)  # Validate that ID is an integer
        except ValueError:
            messagebox.showerror("Input Error", "ID must be a valid integer!")
            return

        # Create employee data dictionary
        employee_data = {
            "id": emp_id,
            "name": name
        }

        try:
            employee = self.controller.create_employee(employee_data)
            messagebox.showinfo("Success", f"Employee {employee.name} with ID {employee.id} created successfully!")
            # Refresh the table in the main frame
            self.master.populate_table()
            self.destroy()  # Close the AddEmployeeFrame after success
        except Exception as e:
            messagebox.showerror("Error", str(e))

    