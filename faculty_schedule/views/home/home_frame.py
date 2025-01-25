from faculty_schedule.utils.frames import BaseFrame
from .add_employee_frame import AddEmployeeFrame
from .edit_employee_frame import EditEmployeeFrame


class HomeFrame(BaseFrame):
    def __init__(self, master=None, frame_manager=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame_manager = frame_manager

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

    # Button click logic - This should probably be in the Controller
    def on_button_click(self, button_text):
        if button_text == "View Employee":
            self.view_employee()
        elif button_text == "Add Employee":
            self.show_add_employee_screen()
        elif button_text == "Edit Employee":
            self.show_edit_employee_screen()
        elif button_text == "Delete Employee":
            pass

    def view_employee(self):
        print("Viewing Employee...")  # Placeholder for actual functionality

    def show_add_employee_screen(self):
        AddEmployeeFrame(self)

    def show_edit_employee_screen(self):
        EditEmployeeFrame(self)

    def show_delete_employee_screen(self):
        print("Showing Delete Employee Screen...")  # Placeholder for actual functionality
