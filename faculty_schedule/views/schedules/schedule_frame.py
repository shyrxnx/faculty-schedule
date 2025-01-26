from faculty_schedule.utils.frames import BaseFrame
from .timetable_base_frame import TimetableCanvas
from .add_schedule_frame import AddSchedFrame
from .edit_schedule_frame import EditSchedFrame
from .delete_schedule_frame import DeleteSchedFrame


class ScheduleFrame(BaseFrame):
    def __init__(self, master=None, frame_manager=None, *args, **kwargs):
        super().__init__(master, frame_manager, *args, **kwargs)
        self.frame_manager = frame_manager
        # Back Button
        self.create_back_button()
        # Buttons
        button_texts = [
            "Add Schedule",
            "Edit Schedule",
            "Delete Schedule",
        ]
        self.create_buttons(button_texts)

        # Timetable (Canvas instead of table)
        columns = ["Time", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        self.timetable_canvas = TimetableCanvas(self, columns=columns)
        self.timetable_canvas.grid(row=1, column=1, rowspan=7, sticky="nsew", padx=(0, 10), pady=5)

        # Set layout
        self.set_layout(button_texts)

    # Button click logic - This should probably be in the Controller
    def on_button_click(self, button_text):
        if button_text == "Add Schedule":
            self.show_add_schedule_screen()
        elif button_text == "Edit Schedule":
            self.show_edit_schedule_screen()
        elif button_text == "Delete Schedule":
            self.show_delete_schedule_screen()

    def show_add_schedule_screen(self):
        AddSchedFrame(self)

    def show_edit_schedule_screen(self):
        EditSchedFrame(self)

    def show_delete_schedule_screen(self):
        DeleteSchedFrame(self)

    def add_schedule(self, day, start_time, end_time):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        day_index = days.index(day) + 1  # +1 to account for the time column

        start_hour, start_minute = map(int, start_time.split(':'))
        end_hour, end_minute = map(int, end_time.split(':'))

        # Calculate start and end rows
        start_row = start_hour - 7 + (0.5 if start_minute == 30 else 0)
        end_row = end_hour - 7 + (0.5 if end_minute == 30 else 0)

        # Shade rows in the timetable
        # Note: Shading for only half of a row is not working
        for row in range(int(start_row * 2), int(end_row * 2)):
            self.timetable_canvas.shade_row(row // 2 + 1, full=False, columns=[day_index], color="#32CD32")
