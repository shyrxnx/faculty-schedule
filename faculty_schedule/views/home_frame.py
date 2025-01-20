import customtkinter as ctk

from ..utils.frames import BaseFrame


class HomeFrame(BaseFrame):
    def __init__(self, master=None, frame_manager=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame_manager = frame_manager

        # Title
        self.create_title_label("Faculty Scheduler")

        # Buttons
        button_texts = [
            "Import from Excel File",
            "Export Data",
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

        self.data = [
            ("John Doe", 1),
            ("Jane Smith", 2),
            ("Alice Johnson", 3),
            ("Bob Brown", 4),
        ]

        self.dropdown_click("Sort by Name")

    def on_button_click(self, button_text):
        if button_text == "Import from Excel File":
            self.import_from_excel()
        elif button_text == "Export Data":
            self.export_data()
        elif button_text == "Add Employee":
            self.show_add_employee_screen()
        elif button_text == "Edit Employee":
            pass
        elif button_text == "Delete Employee":
            pass

    def dropdown_click(self, selected_value):
        # Sort data based on the selected value
        if selected_value == "Sort by Name":
            # Sort by name (alphabetically)
            sorted_data = sorted(self.data, key=lambda x: x[0])  # Sort by the first element (name)
        elif selected_value == "Sort by ID":
            # Sort by ID (numerically)
            sorted_data = sorted(self.data, key=lambda x: x[1])  # Sort by the second element (ID)

        # Update the tree with sorted data
        self.populate_tree(sorted_data)

    def import_from_excel(self):
        print("Importing from Excel File...")  # Placeholder for actual functionality

    def export_data(self):
        print("Exporting Data...")  # Placeholder for actual functionality

    def show_add_employee_screen(self):
        input_box = ctk.CTkToplevel(self)
        input_box.title("Input Box")

        # Center the pop-up on the screen
        window_width = 275
        window_height = 150
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)

        input_box.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Ensure the pop-up is on top
        input_box.lift()          # Bring to front
        input_box.focus_force()   # Focus on the pop-up
        input_box.grab_set()      # Prevent interaction with the main window

        # Create a frame for name and input
        name_frame = ctk.CTkFrame(input_box, width=15)
        name_frame.pack(pady=10, anchor="w", padx=10)

        # Label for name
        ctk.CTkLabel(name_frame, text="Enter name:", width=100).pack(side="left", padx=0)
        # Entry field for name
        input_name = ctk.CTkEntry(name_frame)
        input_name.pack(side="left", padx=10)

        # Create a frame for id and input
        emp_id_frame = ctk.CTkFrame(input_box, width=15)
        emp_id_frame.pack(pady=10, anchor="w", padx=10)

        # Label for id
        ctk.CTkLabel(emp_id_frame, text="Enter id:", width=100).pack(side="left", padx=0)
        # Entry field for id
        input_id = ctk.CTkEntry(emp_id_frame)
        input_id.pack(side="left", padx=10)

        # Function to handle the input when the button is clicked
        def handle_input():
            user_name = input_name.get()
            user_id = input_id.get()
            self.data.append((user_name, int(user_id)))
            self.dropdown_click("Sort by Name")
            print(f"User entered: {user_name} id: {user_id}")
            input_box.destroy()  # Close the pop-up

        # Submit button centered at the bottom
        submit_button = ctk.CTkButton(input_box, text="Submit", command=handle_input)
        submit_button.pack(pady=10, anchor="center")

    def show_edit_employee_screen(self):
        print("Showing Edit Employee Screen...")  # Placeholder for actual functionality

    def show_delete_employee_screen(self):
        print("Showing Delete Employee Screen...")  # Placeholder for actual functionality