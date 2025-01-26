from faculty_schedule.utils.frames import BaseFrame
from .add_sched_code_frame import AddSchedCodeFrame
from .edit_sched_code_frame import EditSchedCodeFrame
from .delete_sched_code_frame import DeleteSchedCodeFrame
from ..schedules import ScheduleFrame


class SchedCodeFrame(BaseFrame):
    def __init__(self, master=None, frame_manager=None, *args, **kwargs):
        super().__init__(master, frame_manager, *args, **kwargs)

        self.frame_manager = frame_manager

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
            "Edit Schedule Code",
            "Delete Schedule Code",
        ]
        self.create_buttons(button_texts)

        # Table
        columns = ["Schedule Code", "Subject", "Section"]
        self.table = self.create_table(columns)

        # Set layout
        self.set_layout(button_texts)

        # # This is just to test the update_info method.
        # self.update_info("Shyrine Salvador", "12345")

    # Button click logic - This should probably be in the Controller
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
        AddSchedCodeFrame(self)

    def show_edit_schedule_code_screen(self):
        EditSchedCodeFrame(self)

    def show_delete_schedule_code_screen(self):
        DeleteSchedCodeFrame(self)

    # UI update method
    def update_info(self, name, emp_id):
        self.name_label.configure(text=f"Name: {name}")
        self.id_label.configure(text=f"ID: {emp_id}")
