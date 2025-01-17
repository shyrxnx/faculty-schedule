import tkinter as tk
from tkinter import ttk

class BaseFrame(tk.Frame):
    """Base class for all frames."""
    def __init__(self, master=None, frame_manager=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.frame_manager = frame_manager
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a separate frame for the search bar at the top-right corner
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(side=tk.TOP, anchor="ne", padx=10, pady=10, fill=tk.X)

        # Search button (to filter the table)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search)
        self.search_button.pack(side=tk.RIGHT)

        # Search bar entry
        self.search_bar = tk.Entry(self.search_frame)
        self.search_bar.pack(side=tk.RIGHT, padx=5)

        # Search label
        self.search_label = tk.Label(self.search_frame, text="Search:")
        self.search_label.pack(side=tk.RIGHT)


        # Treeview for displaying data (to be used in subclasses)
        self.tree = ttk.Treeview(self, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        
        # Button frame at the bottom-right corner
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM, anchor="ne", padx=10, pady=10)
        # Back button
        self.back_button = tk.Button(self.button_frame, text="Back", command=self.go_back)
        self.back_button.grid(row=0, column=0, padx=5)

        self.view_button = tk.Button(self.button_frame, text="View", state=tk.DISABLED, command=self.view_item)
        self.view_button.grid(row=0, column=1, padx=5)

        self.edit_button = tk.Button(self.button_frame, text="Edit", state=tk.DISABLED, command=self.edit_item)
        self.edit_button.grid(row=0, column=2, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete", state=tk.DISABLED, command=self.delete_item)
        self.delete_button.grid(row=0, column=4, padx=5)

        # Bind row selection event
        self.tree.bind("<ButtonRelease-1>", self.on_row_select)

    def search(self):
        """Filter the table based on search input."""
        query = self.search_bar.get().lower()
        for item in self.tree.get_children():
            row_values = self.tree.item(item)["values"]
            if query in str(row_values[0]).lower() or query in str(row_values[1]).lower():
                self.tree.item(item, tags="match")
            else:
                self.tree.item(item, tags="no_match")

        for item in self.tree.get_children():
            if "match" in self.tree.item(item, "tags"):
                self.tree.item(item, open=True)
            else:
                self.tree.item(item, open=False)

    def on_row_select(self, event):
        """Called when a row is clicked, enables the buttons."""
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_row = self.tree.item(selected_item)["values"]
            # Enable buttons when a row is selected
            self.view_button.config(state=tk.NORMAL)
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
    
    def go_back(self):
        """Navigate to the previous frame."""
        self.frame_manager.go_back()

    def view_item(self):
        """Display details of the selected item."""
        if hasattr(self, 'selected_row'):
            # Implement what to do when View is clicked
            print(f"Viewing: {self.selected_row}")


    def edit_item(self):
        """Edit the selected item."""
        if hasattr(self, 'selected_row'):
            # Implement what to do when Edit is clicked
            print(f"Editing: {self.selected_row}")
    
    def delete_item(self):
        """Delete the selected item."""
        if hasattr(self, 'selected_row'):
            # Implement what to do when Delete is clicked
            print(f"Deleting: {self.selected_row}")
            selected_item = self.tree.selection()
            self.tree.delete(selected_item)

    def set_columns(self, columns):
        """Set the columns for the Treeview dynamically."""
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)

    def populate_tree(self, data):
        """Populate the Treeview with data."""
        for item in data:
            self.tree.insert("", tk.END, values=item)

    def on_resize(self, event):
        """Handle window resizing, adjusts column width dynamically."""
        total_width = event.width
        num_columns = len(self.tree["columns"])

        # We will allocate a portion of the total width for each column
        if num_columns > 0:
            column_width = total_width // num_columns
            for col in self.tree["columns"]:
                self.tree.column(col, width=column_width, anchor="center")
        pass

class SearchFrame(BaseFrame):
    """Frame for search bar and table."""
    def __init__(self, master, frame_manager):
        super().__init__(master)
        self.frame_manager = frame_manager
    
        # Define columns for employee list
        self.set_columns(["Name", "Employee Id"])

        # Sample employee data need to get this from database
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
            # Get the selected row (you can also pass specific data like ID, name, etc.)
            selected_item = self.selected_row
            print(f"Viewing: {selected_item}")
            
            # Switch to the SchedCodesFrame
            self.frame_manager.show_frame(SchedCodesFrame, frame_manager=self.frame_manager, selected_item=selected_item)

    

class SchedCodesFrame(BaseFrame):
    """Frame for displaying and managing schedule codes."""
    def __init__(self, master=None, frame_manager=None,selected_item = None):
        super().__init__(master)
        self.frame_manager = frame_manager


        if selected_item:
            print(f"Selected Item Passed: {selected_item[1]}")

        # Define columns
        self.set_columns(["Schedule Code", "Description"])

        # hash map populate this from database
        id_map = {
            1:[
            ("SC001", "Math 101"),
            ("SC002", "Science 101"),
            ("SC003", "History 101"),
            ("SC004", "Computer Science 101"),
            ],
            2:[
            ("SC005", "Math 201"),
            ("SC006", "Science 201"),
            ("SC007", "History 201"),
            ("SC008", "Computer Science 201"),
            ],
        }
        
        self.populate_tree(id_map[selected_item[1]]) # put emplyee id

