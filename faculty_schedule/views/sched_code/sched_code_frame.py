from faculty_schedule.utils.frames import BaseFrame
from .add_sched_code_frame import AddSchedCodeFrame
from .edit_sched_code_frame import EditSchedCodeFrame
from .delete_sched_code_frame import DeleteSchedCodeFrame
from ..schedules import ScheduleFrame
from ...controllers import ScheduleController  # Import your controller here


class SchedCodeFrame(BaseFrame):
    def __init__(self, master=None, frame_manager=None, employee=None, *args, **kwargs):
        super().__init__(master, frame_manager, *args, **kwargs)
        self.employee = employee
        self.frame_manager = frame_manager
        self.controller = ScheduleController()
        
        # Back Button
        self.create_back_button()

        # Labels for Name and ID
        self.name_label = self.create_info_label("Name: ", row=0, column=1)
        # Currently not showing. It is at the back of the table
        self.id_label = self.create_info_label("ID: ", row=1, column=1)

        # Buttons
        button_texts = [
            "View Schedule Code",
            "Add Schedule Code",
            "Delete Schedule Code",
        ]
        self.create_buttons(button_texts)

        # Table
        columns = ["Schedule Code", "Subject", "Section"]
        self.table = self.create_table(columns)

        # Set layout
        self.set_layout(button_texts)

        # # This is just to test the update_info method.
        if self.employee:
            self.update_info(self.employee.name, self.employee.id)

        self.populate_table()

    

    def on_button_click(self, button_text):
        if button_text == "View Schedule Code":
            self.view_schedule_code()
        elif button_text == "Add Schedule Code":
            self.show_add_schedule_code_screen()
        elif button_text == "Edit Schedule Code":
            self.show_edit_schedule_code_screen()
        elif button_text == "Delete Schedule Code":
            self.show_delete_schedule_code_screen()

    def view_schedule_code(self):
        if self.frame_manager:
            # Use the frame manager to navigate to SchedCodeFrame
            self.frame_manager.show_frame(ScheduleFrame)

    def show_add_schedule_code_screen(self):
        id = self.employee.id

        add_schedule_code_frame = AddSchedCodeFrame(self,id)

        def on_close():
        # Refresh the table after the frame is closed
            self.populate_table()
            add_schedule_code_frame.destroy()

        # Attach the on_close method to execute when the frame is destroyed
        add_schedule_code_frame.protocol("WM_DELETE_WINDOW", on_close)
        

    def show_edit_schedule_code_screen(self):
        id = self.employee.id

        add_schedule_code_frame = AddSchedCodeFrame(self,id)

        def on_close():
        # Refresh the table after the frame is closed
            self.populate_table()
            add_schedule_code_frame.destroy()

        # Attach the on_close method to execute when the frame is destroyed
        add_schedule_code_frame.protocol("WM_DELETE_WINDOW", on_close)
        EditSchedCodeFrame(self)

    def show_delete_schedule_code_screen(self):
        
        
        sched_id = self.get_selected_sched_code()

        del_schedule_code_frame = DeleteSchedCodeFrame(self,sched_id)

        def on_close():
        # Refresh the table after the frame is closed
            self.populate_table()
            del_schedule_code_frame.destroy()

        # Attach the on_close method to execute when the frame is destroyed
        del_schedule_code_frame.protocol("WM_DELETE_WINDOW", on_close)
        

    def get_selected_sched_code(self):
        """Retrieve the selected schedule code using the Schedule Code."""
        selected_item = self.table.selection()
        if not selected_item:
            return None

        # Extract Schedule Code from the selected row
        item_values = self.table.item(selected_item, "values")
        
        if not item_values:
            return None
        print(item_values)
        sched_id = int(item_values[0])  # Assuming ID is in the second column
        try:
            return self.controller.get_schedule(sched_id)
        except FileNotFoundError:
            ctk.CTkMessagebox.show_warning(title="Warning", message="Employee not found.")
            return None

    # UI update method
    def update_info(self, name, emp_id):
        self.name_label.configure(text=f"Name: {name}")
        self.id_label.configure(text=f"ID: {emp_id}")

    def populate_table(self):
        """Populate the table with schedule data using the ScheduleController."""
        # Clear the current table contents
        self.clear_table()

        # Get schedule codes of the employee and display them
        employee_id = self.employee.id
        
        # Initialize the ScheduleController to access schedule data
        schedule_controller = ScheduleController()

        try:
            # Get all schedules for the employee
            schedules = schedule_controller._load_df(schedule_controller.schedules_file)

            # Filter schedules for the specific employee
            employee_schedules = schedules[schedules['employee_id'] == employee_id]

            # Add rows to the table for each schedule
            for _, schedule in employee_schedules.iterrows():
                schedule_code = schedule['code']
                description = schedule['description']

                # Split description into subject and section
                if "-" in description:
                    subject, section = description.split(" - ", 1)
                else:
                    subject, section = description, ""

                # Add the schedule code, subject, and section to the table
                self.table.insert("", "end", values=(schedule_code, subject, section))

        except Exception as e:
            # Handle errors if any (e.g., file loading errors)
            print(f"Error loading schedules: {e}")


        

    def clear_table(self):
        """Clear all rows from the table."""
        for row in self.table.get_children():
            self.table.delete(row)