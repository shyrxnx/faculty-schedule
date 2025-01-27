from faculty_schedule.utils.frames import BaseFrame
from .add_employee_frame import AddEmployeeFrame
from .edit_employee_frame import EditEmployeeFrame
from .delete_employee_frame import DeleteEmployeeFrame
from ..sched_code import SchedCodeFrame
from ...controllers.employee_controller import EmployeeController  # Import your controller here



class HomeFrame(BaseFrame):
    def __init__(self, master=None, frame_manager=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame_manager = frame_manager
        self.controller = EmployeeController()  # Initialize the controller here


        # Title
        self.create_title_label("Faculty Scheduler")

        # Buttons
        button_texts = [
            "View Employee",
            "Add Employee",
            "Edit Employee",
            "Delete Employee",
        ]
        self.create_buttons(button_texts)

        # Sort dropdown
        self.create_dropdown(["Sort by Name", "Sort by ID"], "Sort by Name", row=len(button_texts) + 1, column=0)

        # Search bar
        self.create_search_bar("Search...", row=0, column=1)

        # Table
        columns = ["Name", "Employee ID"]
        self.table = self.create_table(columns)

        self.set_layout(button_texts)

        self.dropdown_click("Sort by Name")

        self.populate_table()

    # Button click logic - This should probably be in the Controller
    def on_button_click(self, button_text):
        if button_text == "View Employee":
            self.view_employee()
        elif button_text == "Add Employee":
            self.show_add_employee_screen()
        elif button_text == "Edit Employee":
            self.show_edit_employee_screen()
        elif button_text == "Delete Employee":
            self.show_delete_employee_screen()

    def dropdown_click(self, option):
        if option == "Sort by Name":
            employees = self.controller.get_employees()
            employees.sort(key=lambda emp: emp.name.lower())
        elif option == "Sort by ID":
            employees = self.controller.get_employees()
            employees.sort(key=lambda emp: emp.id)

        # Update the table
        self.clear_table()
        for employee in employees:
            self.table.insert("", "end", values=(employee.name, employee.id))


    # In the method where you navigate to SchedCodeFrame:
    def view_employee(self):
        selected_employee = self.get_selected_employee()  # Assume this gets the selected employee object
        if selected_employee:
            # Pass the selected employee to the new frame
            self.frame_manager.show_frame(SchedCodeFrame, employee=selected_employee)


    def show_add_employee_screen(self):
        add_employee_frame = AddEmployeeFrame(self)

        def on_close():
        # Refresh the table after the frame is closed
            self.populate_table()
            add_employee_frame.destroy()

        # Attach the on_close method to execute when the frame is destroyed
        add_employee_frame.protocol("WM_DELETE_WINDOW", on_close)

    def get_selected_employee(self):
        """Retrieve the selected employee using the Employee ID."""
        selected_item = self.table.selection()
        if not selected_item:
            return None

        # Extract Employee ID from the selected row
        item_values = self.table.item(selected_item, "values")
        
        if not item_values or len(item_values) < 2:
            return None

        employee_id = int(item_values[1])  # Assuming ID is in the second column
        try:
            return self.controller.get_employee(employee_id)
        except FileNotFoundError:
            ctk.CTkMessagebox.show_warning(title="Warning", message="Employee not found.")
            return None

    def show_edit_employee_screen(self):
        """Show the edit employee screen with the selected employee's data."""
        selected_employee = self.get_selected_employee()
        if not selected_employee:
            return

        # Open EditEmployeeFrame and pass the selected employee
        edit_employee_frame = EditEmployeeFrame(self, selected_employee)

        def on_close():
            # Refresh the table after editing
            self.populate_table()
            edit_employee_frame.destroy()

        edit_employee_frame.protocol("WM_DELETE_WINDOW", on_close)


    def show_delete_employee_screen(self):
        """Show the delete employee screen with the selected employee's data."""
        selected_employee = self.get_selected_employee()
        if not selected_employee:
            return

        delete_employee_frame = DeleteEmployeeFrame(self,selected_employee)

        def on_close():
            # Refresh the table after editing
            self.populate_table()
            delete_employee_frame.destroy()

        delete_employee_frame.protocol("WM_DELETE_WINDOW", on_close)

    def populate_table(self):
        """Populate the table with employee data using the EmployeeController."""
        # Clear the current table contents
        self.clear_table()
        # Get employees from the controller
        employees = self.controller.get_employees()

        # Populate the table with the retrieved employees
        for employee in employees:
            self.table.insert("", "end", values=(employee.name, employee.id))

    def clear_table(self):
        """Clear all rows from the table."""
        for row in self.table.get_children():
            self.table.delete(row)

    
