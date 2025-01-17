# faculty_schedule/utils/frames/base_frame.py

import tkinter as tk
from tkinter import ttk

class BaseFrame(tk.Frame):
    """Base class for all frames."""
    def __init__(self, master=None, frame_manager=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.frame_manager = frame_manager
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Search bar frame (common across all frames)
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(side=tk.TOP, anchor="ne", padx=10, pady=10, fill=tk.X)

        # Search components (search bar, button)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search)
        self.search_button.pack(side=tk.RIGHT)
        self.search_bar = tk.Entry(self.search_frame)
        self.search_bar.pack(side=tk.RIGHT, padx=5)
        self.search_label = tk.Label(self.search_frame, text="Search:")
        self.search_label.pack(side=tk.RIGHT)

        # Treeview (for displaying data)
        self.tree = ttk.Treeview(self, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Button frame (common buttons: Back, View, Edit, Delete)
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM, anchor="ne", padx=10, pady=10)
        self.back_button = tk.Button(self.button_frame, text="Back", command=self.go_back)
        self.back_button.grid(row=0, column=0, padx=5)
        self.view_button = tk.Button(self.button_frame, text="View", state=tk.DISABLED, command=self.view_item)
        self.view_button.grid(row=0, column=1, padx=5)
        self.edit_button = tk.Button(self.button_frame, text="Edit", state=tk.DISABLED, command=self.edit_item)
        self.edit_button.grid(row=0, column=2, padx=5)
        self.delete_button = tk.Button(self.button_frame, text="Delete", state=tk.DISABLED, command=self.delete_item)
        self.delete_button.grid(row=0, column=4, padx=5)

        # Bind selection event
        self.tree.bind("<ButtonRelease-1>", self.on_row_select)

    def search(self):
        """Filter the treeview based on search input."""
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
        """Called when a row is clicked, enables buttons."""
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_row = self.tree.item(selected_item)["values"]
            self.view_button.config(state=tk.NORMAL)
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)

    def go_back(self):
        """Navigate to the previous frame."""
        self.frame_manager.go_back()

    def view_item(self):
        """To be overridden in subclasses for specific behavior."""
        if hasattr(self, 'selected_row'):
            print(f"Viewing: {self.selected_row}")
            self.frame_manager.show_frame(SchedCodesFrame, frame_manager=self.frame_manager, selected_item=self.selected_row)
        pass

    def edit_item(self):
        """To be overridden in subclasses for specific behavior."""
        pass

    def delete_item(self):
        """To be overridden in subclasses for specific behavior."""
        pass

    def set_columns(self, columns):
        """Set the columns for the treeview dynamically."""
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)

    def populate_tree(self, data):
        """Populate the treeview with data."""
        for item in data:
            self.tree.insert("", tk.END, values=item)
