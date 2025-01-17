import tkinter as tk
from tkinter import ttk

class FrameManager:
    """Manages switching between frames."""
    def __init__(self, master):
        self.master = master
        self.frames = {}  # Dictionary to store frames
        self.current_frame = None
        self.frame_history = []  # Stack to track the history of frames

    def show_frame(self, frame_class, *args, **kwargs):
        """Show a new frame and hide the previous one."""
        # Hide the previous frame and push to frame_history
        if self.current_frame:
            self.frame_history.append(self.current_frame)
            self.current_frame.pack_forget()  # Instead of destroying, just hide the current frame

        # Check if frame is already created
        if frame_class not in self.frames:
            kwargs.pop('frame_manager', None)  # Remove 'frame_manager' from kwargs to avoid duplication
            self.frames[frame_class] = frame_class(master=self.master, frame_manager=self, *args, **kwargs)

        # Set the new frame as the current one
        self.current_frame = self.frames[frame_class]
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def go_back(self):
        """Go back to the previous frame."""
        if self.frame_history:
            # Pop the last frame from the history stack
            previous_frame = self.frame_history.pop()

            # Hide the current frame
            if self.current_frame:
                self.current_frame.pack_forget()

            # Set the current frame to the previous one
            self.current_frame = previous_frame

            # Show the previous frame
            self.current_frame.pack(fill=tk.BOTH, expand=True)