# faculty_schedule/views/search_frame.py

from ..utils.frames import BaseFrame
from .sched_codes_frame import SchedCodesFrame

class SearchFrame(BaseFrame):
    """Frame for searching and viewing employee data."""
    def __init__(self, master, frame_manager):
        super().__init__(master, frame_manager)
        self.frame_manager = frame_manager
        
        # Set up columns
        self.set_columns(["Name", "Employee Id"])

        # Example data (this would be pulled from a database)
        data = [
            ("John Doe", 1),
            ("Jane Smith", 2),
            ("Alice Johnson", 3),
            ("Bob Brown", 4),
        ]
        self.populate_tree(data)

    def view_item(self):
        """Switch to the SchedCodesFrame when View is clicked."""
        if hasattr(self, 'selected_row'):
            selected_item = self.selected_row
            print(f"Viewing: {selected_item}")
            self.frame_manager.show_frame(SchedCodesFrame, selected_item=selected_item)
