import customtkinter as ctk
from tkinter import ttk, messagebox
from ...controllers import ScheduleController
from ...exceptions import *



class EditSchedFrame(ctk.CTkToplevel):
    def __init__(self, master=None,schedule_code = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Edit Schedule")
        self.master = master

        self.controller = ScheduleController()
        self.schedule_code = schedule_code

        # Center the pop-up on the screen
        window_width = 300
        window_height = 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Ensure the pop-up is on top
        self.lift()
        self.focus_force()
        self.grab_set()

        # Create a frame for Schedule Slot
        slot_frame = ctk.CTkFrame(self, width=15)
        slot_frame.pack(pady=10, anchor="w", padx=10)

        # Label for Schedule Slot
        ctk.CTkLabel(slot_frame, text="Select Slot:", width=120).pack(side="left", padx=0)

        # Dropdown for Schedule Slot
        # self.input_slot = ctk.CTkComboBox(slot_frame)
        self.input_slot = ctk.CTkComboBox(slot_frame, command=self.on_slot_selected)
        self.input_slot.pack(side="left", padx=10)
        # Load schedule slots into the dropdown
        self.load_schedule_slots()




        # Create a frame for Date
        date_frame = ctk.CTkFrame(self, width=15)
        date_frame.pack(pady=10, anchor="w", padx=10)

        # Label for Date
        ctk.CTkLabel(date_frame, text="Edit Date:", width=120).pack(side="left", padx=0)

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
        ctk.CTkLabel(start_time_frame, text="Edit Start Time:", width=120).pack(side="left", padx=0)

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
        ctk.CTkLabel(end_time_frame, text="Edit End Time:", width=120).pack(side="left", padx=0)

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
        submit_button = ctk.CTkButton(self, text="Submit", command= self.edit)
        submit_button.pack(pady=10, anchor="center")

        

    def edit(self):
        """Handle the submit button click and update the selected schedule slot."""
        try:
            # Ensure a slot is selected
            if not hasattr(self, 'selected_slot_id') or self.selected_slot_id is None:
                print("Error: No slot selected to edit.")
                return

            # Collect updated values from input fields
            day = self.input_date.get()
            start_time = f"{self.input_start_hour.get().zfill(2)}:{self.input_start_minute.get().zfill(2)}"
            end_time = f"{self.input_end_hour.get().zfill(2)}:{self.input_end_minute.get().zfill(2)}"
            detail = "Nothing"
            print(self.selected_slot_id)
            print(day)
            print(start_time)
            print(end_time)
            print(detail)
            # Validate collected data
            if not day or not start_time or not end_time:
                print("Error: Missing required fields.")
                return

            # Prepare data in the format expected by edit_schedule_slot
            updated_data = {
                'schedule_id': self.selected_slot_id,
                "day": day,
                "start_time": start_time,
                "end_time": end_time,
                "detail": detail,
            }

            # Call the edit_schedule_slot function
            updated_slot = self.controller.edit_schedule_slot(self.selected_slot_id, updated_data)
            print(f"Slot updated successfully: {updated_slot}")
            self.master.populate_slots()
            
            self.destroy()

            # Optionally, show a success message to the user
            # ctk.CTkMessagebox.show_info("Success", "Schedule slot updated successfully!")

        except ValidationError as e:
            print(f"Validation Error: {e}")
            # ctk.CTkMessagebox.show_error("Error", f"Validation Error: {e}")
        except NotFoundError as e:
            print(f"Error: {e}")
            # ctk.CTkMessagebox.show_error("Error", f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            # ctk.CTkMessagebox.show_error("Error", f"Unexpected error occurred: {e}")

    def load_schedule_slots(self):
        """Load schedule slots for the provided schedule code and populate the dropdown."""
        try:
            # Fetch schedule data
            slots_data = self.controller.get_schedule_slots(self.schedule_code)
            
            # Create a mapping of slot values to their IDs
            self.slot_map = {
                f"{slot['day']} {slot['start_time']} - {slot['end_time']}": slot['id']
                for _, slot in slots_data.iterrows()
            }
            
            # Populate the dropdown with the slot values (without IDs)
            slot_values = list(self.slot_map.keys())
            print("Loaded slot values:", slot_values)  # Debugging line
            self.input_slot.configure(values=slot_values)

            # Manually select the first value to trigger the callback
            if slot_values:
                self.input_slot.set(slot_values[0])  # Set the first value
                self.after(100, lambda: self.on_slot_selected(slot_values[0]))  # Trigger the callback manually
        except NotFoundError as e:
            print(f"Error: {e}")

    def on_slot_selected(self, selected_value=None):
        """Update the input fields based on the selected schedule slot."""
        selected_slot = selected_value if selected_value else self.input_slot.get()
        print("Selected slot:", selected_slot)  # Debugging

        if selected_slot:
            try:
                # Retrieve the slot ID using the selected slot
                slot_id = self.slot_map.get(selected_slot, None)
                print("Selected slot ID:", slot_id)  # Debugging

                # Parse the slot details
                day, times = selected_slot.split(" ", 1)
                start_time, end_time = times.split(" - ")
                start_hour, start_minute = start_time.split(":")
                end_hour, end_minute = end_time.split(":")

                # Update input fields
                self.input_date.set(day)
                self.input_start_hour.set(start_hour)
                self.input_start_minute.set(start_minute)
                self.input_end_hour.set(end_hour)
                self.input_end_minute.set(end_minute)

                # Store the selected slot ID for later use (e.g., when submitting changes)
                self.selected_slot_id = slot_id
            except ValueError:
                print(f"Error: Could not parse the selected slot '{selected_slot}'. Ensure it's in 'Day StartTime - EndTime' format.")
        else:
            print("No slot selected.")


