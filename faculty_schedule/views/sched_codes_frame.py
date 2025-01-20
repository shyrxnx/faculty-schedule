# faculty_schedule/views/sched_codes_frame.py

from ..utils.frames import BaseFrame


class SchedCodesFrame(BaseFrame):
    """Frame for displaying and managing schedule codes."""

    def __init__(self, master=None, frame_manager=None, selected_item=None):
        super().__init__(master, frame_manager)

        print(f'Selected Item Passed: {selected_item}')

        if selected_item:
            print(f'Selected Item Passed: {selected_item[1]}')

        # Define columns
        self.set_columns(['Schedule Code', 'Description'])

        # Sample data (to be fetched from a database)
        id_map = {
            1: [('SC001', 'Math 101'), ('SC002', 'Science 101')],
            2: [('SC003', 'History 101'), ('SC004', 'Computer Science 101')],
        }

        # Populate the treeview
        self.populate_tree(id_map[selected_item[1]])
