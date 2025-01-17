import tkinter as tk


class FrameManager:
    """Manages switching between frames."""

    def __init__(self, master):
        self.master = master
        self.frames = {}  # Dictionary to store persistent frames
        self.current_frame = None
        self.frame_history = []  # Stack to track the history of frames

    def show_frame(self, frame_class, *args, **kwargs):
        """Show a new frame, hide the previous one, and update it if necessary."""
        # Hide the current frame and add it to history
        if self.current_frame:
            self.frame_history.append(self.current_frame)
            self.current_frame.pack_forget()  # Keep the current frame hidden

        # Check if the frame already exists in the dictionary
        if frame_class in self.frames:
            frame = self.frames[frame_class]

            # Reinitialize the frame if new arguments are passed
            if kwargs.get('selected_item') is not None:
                frame.destroy()
                frame = frame_class(master=self.master, frame_manager=self, *args, **kwargs)
                self.frames[frame_class] = frame
        else:
            # Create a new frame if it doesn't exist
            frame = frame_class(master=self.master, frame_manager=self, *args, **kwargs)
            self.frames[frame_class] = frame

        # Set the new frame as the current one
        self.current_frame = frame
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def go_back(self):
        """Go back to the previous frame."""
        if self.frame_history:
            # Hide the current frame
            if self.current_frame:
                self.current_frame.pack_forget()

            # Pop the last frame from the history stack
            previous_frame = self.frame_history.pop()
            self.current_frame = previous_frame

            # Show the previous frame
            self.current_frame.pack(fill=tk.BOTH, expand=True)
