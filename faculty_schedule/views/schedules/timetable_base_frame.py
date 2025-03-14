import tkinter as tk


class TimetableCanvas(tk.Canvas):
    def __init__(self, master, columns, row_height=30, column_width=120, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Canvas Configurations
        self.configure(bg="#2a2d2e", scrollregion=(0, 0, column_width * len(columns), row_height * 15))
        self.columns = columns
        self.row_height = row_height
        self.column_width = column_width

        # Header Styling
        self.header_bg = "#565b5e"
        self.header_fg = "white"
        self.cell_bg = "#343638"
        self.time_bg = "#3e4451"
        self.shade_full_bg = "#32CD32"
        self.shade_half_bg = "#32CD32"
        self.text_font = ("Arial", 12)
        self.header_font = ("Arial", 12, "bold")

        # Draw the timetable grid
        self.create_table()

        # Bind resize event
        self.bind("<Configure>", self.on_resize)

    def create_table(self):
        # Draw headers
        for col_idx, column_name in enumerate(self.columns):
            x1 = col_idx * self.column_width
            x2 = x1 + self.column_width
            self.create_rectangle(x1, 0, x2, self.row_height, fill=self.header_bg, outline="white")
            self.create_text((x1 + x2) / 2, self.row_height / 2, text=column_name, fill=self.header_fg,
                             font=self.header_font)

        # Draw rows and apply row styles
        for row_idx in range(14):  # Adjust the number of rows as needed (e.g., 20 rows)
            y1 = self.row_height + row_idx * self.row_height
            y2 = y1 + self.row_height
            # Time range format (7:00 - 8:00, 8:00 - 9:00, ...)
            time_range = f"{7 + row_idx}:00 - {8 + row_idx}:00"
            for col_idx in range(len(self.columns)):
                x1 = col_idx * self.column_width
                x2 = x1 + self.column_width
                if col_idx == 0:  # Time column
                    self.create_rectangle(x1, y1, x2, y2, fill=self.time_bg, outline="white")
                    # Time Range Font
                    self.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=time_range, fill=self.header_fg,
                                     font=("Arial", 12, "bold"))
                else:
                    self.create_rectangle(x1, y1, x2, y2, fill=self.cell_bg, outline="white")

    def on_resize(self, event):
        # Recalculate the column width and row height based on window size
        new_width = event.width
        new_height = event.height

        # Dynamically adjust the column width and row height based on the window size
        self.column_width = new_width // len(self.columns)
        self.row_height = new_height // 14  # Assuming you want 20 rows

        # Redraw the table with the updated dimensions
        self.delete("all")
        self.create_table()

    # The shading for half row is not working.
    def shade_row(self, row, full=True, columns=None, color=None):
        """
        Shade rows in full or partially. Rows are indexed from 1.
        """
        

        y1 = self.row_height + (row - 1) * self.row_height
        y2 = y1 + self.row_height
        color = color or (self.shade_full_bg if full else self.shade_half_bg)

        if full:
            for col_idx in range(len(self.columns)):
                x1 = col_idx * self.column_width
                x2 = x1 + self.column_width
                if col_idx > 0:
                    # Delete any existing shapes in the area first
                    self.delete("shade_{}_{}".format(row, col_idx))
                    rect = self.create_rectangle(x1, y1, x2, y2, fill=color, outline=self.cell_bg)
                    self.itemconfig(rect, tags="shade_{}_{}".format(row, col_idx))
        else:
            for col_idx in columns or []:
                x1 = col_idx * self.column_width
                x2 = x1 + self.column_width
                self.delete("shade_{}_{}".format(row, col_idx))
                rect = self.create_rectangle(x1, y1, x2, y2, fill=color, outline=self.cell_bg)
                self.itemconfig(rect, tags="shade_{}_{}".format(row, col_idx))

    

        
