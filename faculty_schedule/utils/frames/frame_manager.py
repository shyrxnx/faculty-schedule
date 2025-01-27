import tkinter as tk


class FrameManager:
    """Manages switching between frames."""

    def __init__(self, master):
        self.master = master
        self.frames = {}  # Dictionary to store persistent frames
        self.current_frame = None
        self.frame_history = []  # Stack to track the history of frames

    def show_frame(self, frame_class, *args, **kwargs):
        """Show a new frame, hide and forget the previous one if necessary."""
        # Hide the current frame and add it to the history
        if self.current_frame:
            self.frame_history.append(self.current_frame)
            self.current_frame.pack_forget()  # Hide the current frame

        # Destroy and forget the frame if it already exists (to create a fresh instance)
        if frame_class in self.frames:
            self.frames[frame_class].destroy()
            del self.frames[frame_class]

        # Create a new frame instance
        frame = frame_class(master=self.master, frame_manager=self, *args, **kwargs)
        self.frames[frame_class] = frame

        # Set the new frame as the current one
        self.current_frame = frame
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def go_back(self):
        """Go back to the previous frame, destroying the current frame."""
        if self.current_frame:
            # Destroy the current frame
            self.current_frame.destroy()
            self.current_frame = None

        if self.frame_history:
            # Retrieve the last frame from history
            previous_frame = self.frame_history.pop()

            # Set the previous frame as the current one
            self.current_frame = previous_frame
            self.current_frame.pack(fill=tk.BOTH, expand=True)
