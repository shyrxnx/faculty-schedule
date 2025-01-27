import customtkinter as ctk
from tkinter import messagebox
from ...controllers.employee_controller import EmployeeController  # Import your controller here



class DeleteEmployeeFrame(ctk.CTkToplevel):
    def __init__(self, master=None, selected_player = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Delete Employee")
        self.controller = EmployeeController()
        self.selected_player = selected_player

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

        # Create a frame for id and input
        emp_id_frame = ctk.CTkFrame(self, width=15)
        emp_id_frame.pack(pady=10, anchor="w", padx=10)

        # Label for id
        ctk.CTkLabel(name_frame, text=f"Employee Name: {self.selected_player.name}", width=200).pack(side="left", padx=0)
        # Label for id
        ctk.CTkLabel(emp_id_frame, text=f"Employee ID: {self.selected_player.id}", width=200).pack(side="left", padx=0)
        

        # Submit button centered at the bottom
        submit_button = ctk.CTkButton(self, text="Confirm", command=self.confirm)
        submit_button.pack(pady=10, anchor="center")

    def confirm(self):
        try:
            self.controller.delete_employee(self.selected_player.id)
            messagebox.showinfo("Success", f"Employee {self.selected_player.name} with ID {self.selected_player.id} deleted successfully!")
            # Refresh the table in the main frame
            self.master.populate_table()
            self.destroy()  # Close the AddEmployeeFrame after success
        except Exception as e:
            messagebox.showerror("Error", str(e))