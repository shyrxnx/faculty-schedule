import tkinter as tk
from tkinter import messagebox


# do.start_apache_mysql() #use this to start mysql and apache
# do.stop_apache_mysql() #use this to stop mysql and apache

# Function to handle the window close event
def on_closing():
    # Ask the user for confirmation before closing
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # do.stop_apache_mysql() #use this to stop mysql and apache
        window.destroy()  # Close the window

window = tk.Tk()

# Set the window title
window.title("Faculty Scheduler")

# Set the window size
window.geometry("400x300")

# Add a label widget
label = tk.Label(window, text="Hello, world!")
label.pack(pady=20)

# Bind the close event to the on_closing function
window.protocol("WM_DELETE_WINDOW", on_closing)

def main():
    # Create the main window
    window.mainloop()


if __name__ == "__main__":
    main()
