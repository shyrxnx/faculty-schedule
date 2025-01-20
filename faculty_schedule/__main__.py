import customtkinter as ctk
from tkinter import messagebox
from .utils.frames import FrameManager  # Import the FrameManager class
from .views import HomeFrame  # Import your initial frame (SearchFrame)

# Initialize the appearance mode and color theme for CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# TODO: Add watchdog to monitor files for changes

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
window = ctk.CTk()

# Set the window title
window.title("Faculty Scheduler")

# Set the window size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_width = int(screen_width * 0.8)  # 80% of screen width
window_height = int(screen_height * 0.8)  # 80% of screen height

x_position = int((screen_width - window_width) / 2)  # Center horizontally
y_position = int((screen_height - window_height) / 2)  # Center vertically

window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Set the window's minimum size to avoid overly small resizing
window.minsize(800, 600)

# Create the FrameManager instance
frame_manager = FrameManager(window)

# Show the SearchFrame as the initial frame
frame_manager.show_frame(HomeFrame)

# Bind the close event to the on_closing function
window.protocol("WM_DELETE_WINDOW", on_closing)


def main():
    # Create the main window
    window.mainloop()


if __name__ == "__main__":
    main()
