import customtkinter as ctk
from tkinter import ttk
from ...controllers import ScheduleController


class AddSchedFrame(ctk.CTkToplevel):
    def __init__(self, master=None, sched_id = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.sched_id= sched_id
        self.controller = ScheduleController()
        self.title("Add Schedule")

        # Center the pop-up on the screen
        window_width = 300
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Ensure the pop-up is on top
        self.lift()
        self.focus_force()
        self.grab_set()

        # Create a frame for Date
        date_frame = ctk.CTkFrame(self, width=15)
        date_frame.pack(pady=10, anchor="w", padx=10)

        # Label for Date
        ctk.CTkLabel(date_frame, text="Enter Date:", width=120).pack(side="left", padx=0)

        # Dropdown for Date
        self.input_date = ctk.CTkComboBox(
            date_frame,
            values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        )
        self.input_date.pack(side="left", padx=10)

        # Create a frame for Start Time
        start_time_frame = ctk.CTkFrame(self, width=15)
        start_time_frame.pack(pady=10, anchor="w", padx=20)

        # Label for Start Time
        ctk.CTkLabel(start_time_frame, text="Enter Start Time:", width=120).pack(side="left", padx=0)

        # Spinboxes for Start Time
        self.input_start_hour = ttk.Spinbox(
            start_time_frame, from_=7, to=21, width=3, font=("Helvetica", 12)
        )
        self.input_start_hour.pack(side="left", padx=2)
        ctk.CTkLabel(start_time_frame, text=":").pack(side="left", padx=0)

        self.input_start_minute = ttk.Spinbox(
            start_time_frame, values=("00", "30"), width=3, font=("Helvetica", 12)
        )
        self.input_start_minute.pack(side="left", padx=2)

        # Create a frame for End Time
        end_time_frame = ctk.CTkFrame(self, width=15)
        end_time_frame.pack(pady=10, anchor="w", padx=20)

        # Label for End Time
        ctk.CTkLabel(end_time_frame, text="Enter End Time:", width=120).pack(side="left", padx=0)

        # Spinboxes for End Time
        self.input_end_hour = ttk.Spinbox(
            end_time_frame, from_=7, to=21, width=3, font=("Helvetica", 12)
        )
        self.input_end_hour.pack(side="left", padx=2)
        ctk.CTkLabel(end_time_frame, text=":").pack(side="left", padx=0)

        self.input_end_minute = ttk.Spinbox(
            end_time_frame, values=("00", "30"), width=3, font=("Helvetica", 12)
        )
        self.input_end_minute.pack(side="left", padx=2)

        # Submit button centered at the bottom
        submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_schedule)
        submit_button.pack(pady=10, anchor="center")

    def submit_schedule(self):
        date = self.input_date.get()
        start_time = f"{self.input_start_hour.get().zfill(2)}:{self.input_start_minute.get().zfill(2)}"
        end_time = f"{self.input_end_hour.get().zfill(2)}:{self.input_end_minute.get().zfill(2)}"

        self.master.add_schedule(date, start_time, end_time)

        try:
            self.controller.add_schedule_slot({
                'schedule_id': self.sched_id,
                'day': date,  # Map date to the correct Day enum if necessary
                'start_time': start_time,
                'end_time': end_time,
                'detail': 'Nothing',  # Example detail, can be dynamic
            })
            print("Schedule slot added successfully!")
        except Exception as e:
            print(f"Failed to add schedule slot: {e}")

        self.destroy()
