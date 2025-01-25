import customtkinter as ctk
from tkinter import ttk


class BaseFrame(ctk.CTkFrame):
    def __init__(self, master=None, frame_manager=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame_manager = frame_manager

    def create_title_label(self, text, font=("Arial", 24, "bold"), row=0, column=0, columnspan=1, padx=10, pady=10):
        title_label = ctk.CTkLabel(self, text=text, font=font)
        title_label.grid(row=row, column=column, columnspan=columnspan, sticky="nsew", padx=padx, pady=pady)
        return title_label

    def create_buttons(self, button_texts, row_start=1, column_start=0):
        buttons = []
        for i, text in enumerate(button_texts):
            button = ctk.CTkButton(self, text=text, font=("Arial", 14, "bold"), width=180, height=34, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row_start + i, column=column_start, sticky="nsew", padx=10, pady=5)
            buttons.append(button)
        return buttons

    def on_button_click(self, button_name):
        print(button_name)

    def create_dropdown(self, values, default_value, row, column, width=180, padx=10, pady=30):
        dropdown = ctk.CTkOptionMenu(self, values=values, width=width, command=self.dropdown_click)
        dropdown.set(default_value)
        dropdown.grid(row=row, column=column, sticky="w", padx=padx, pady=pady)
        return dropdown

    def dropdown_click(self, selected_value):
        print(f"Dropdown selected: {selected_value}")
        # Add any additional handling logic here

    def create_search_bar(self, placeholder_text="Search...", font=("Arial", 12), row=0, column=1, padx=(20, 10),
                          pady=10):
        search_entry = ctk.CTkEntry(self, font=font, placeholder_text=placeholder_text)
        search_entry.grid(row=row, column=column, sticky="nsew", padx=padx, pady=pady)
        return search_entry

    def create_table(self, columns, row_start=1, column_start=1, height=10, width=150):
        table = ttk.Treeview(self, columns=columns, show="headings", height=height)
        table.grid(row=row_start, column=column_start, rowspan=7, sticky="nsew", padx=(0, 10), pady=5)

        style = ttk.Style()

        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0,
                        font=("Arial", 12))
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat",
                        font=("Arial", 12, "bold"))
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="center", width=width)
        return table

    def set_layout(self, button_texts):
        # Configure layout for the frame
        # self.grid_rowconfigure(0, weight=0)  # Title row
        # for i in range(1, len(button_texts)):  # Button and dropdown rows
        #     self.grid_rowconfigure(i, weight=0)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Left column (buttons)
        self.grid_columnconfigure(1, weight=1)  # Right column (table and search bar)

    def populate_tree(self, alist):
        # Clear existing data from the Treeview
        for item in self.table.get_children():
            self.table.delete(item)

        # Insert new data (sorted)
        for item in alist:
            self.table.insert("", "end", values=item)