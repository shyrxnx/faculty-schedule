# from .utils import database_opener as do
import tkinter as tk
from tkinter import messagebox

from .utils.frames import FrameManager  # Import the FrameManager class
from .views import SearchFrame


# Start Apache and MySQL
# do.start_apache_mysql()  # Use this to start MySQL and Apache
# do.stop_apache_mysql()  # Use this to stop MySQL and Apache

# Function to handle the window close event
def on_closing():
    # Ask the user for confirmation before closing
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # do.stop_apache_mysql()  # Use this to stop MySQL and Apache
        window.destroy()  # Close the window


# Create the main window
window = tk.Tk()

# Set the window title
window.title("Faculty Scheduler")

# Set the window size
window.geometry(f"{int(window.winfo_screenwidth() * 0.8)}x{int(window.winfo_screenheight() * 0.8)}")

# Create the FrameManager instance
frame_manager = FrameManager(window)

# Show the SearchFrame as the initial frame
frame_manager.show_frame(SearchFrame)

# Bind the close event to the on_closing function
window.protocol("WM_DELETE_WINDOW", on_closing)


def main():
    # Create the main window
    window.mainloop()


if __name__ == "__main__":
    main()
