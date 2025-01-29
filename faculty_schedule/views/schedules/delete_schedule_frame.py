import customtkinter as ctk
from tkinter import ttk, messagebox
from ...controllers import ScheduleController
from ...exceptions import *


class DeleteSchedFrame(ctk.CTkToplevel):
    def __init__(self, master=None,schedule_code = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Delete Schedule")
        self.master = master

        self.controller = ScheduleController()
        self.schedule_code = schedule_code

        # Center the pop-up on the screen
        window_width = 350
        window_height = 100
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Ensure the pop-up is on top
        self.lift()
        self.focus_force()
        self.grab_set()


        # Create a frame for selecting the schedule to delete
        delete_frame = ctk.CTkFrame(self, width=15)
        delete_frame.pack(pady=10, anchor="w", padx=10)

        # Label for Schedule
        ctk.CTkLabel(delete_frame, text="Select Schedule to Delete:", width=180).pack(side="left", padx=0)
        # Dropdown for Schedule
        self.input_schedule = ctk.CTkComboBox(delete_frame,command=self.on_slot_selected)  # Example values, replace with actual schedule list
        self.input_schedule.pack(side="left", padx=10)
        self.load_schedule_slots()

        # Delete button centered at the bottom
        delete_button = ctk.CTkButton(self, text="Delete", command=self.delete)
        delete_button.pack(pady=10, anchor="center")

    def delete(self):
        """Handle the delete button click and delete the selected schedule slot."""
        try:
            # Ensure a slot is selected
            if not hasattr(self, 'selected_slot_id') or self.selected_slot_id is None:
                print("Error: No slot selected to edit.")
                return

            # Validate collected data
            if not self.selected_slot_id:
                print("Error: Missing required fields.")
                return

            

            # Call the edit_schedule_slot function
            deleted_slot = self.controller.delete_schedule_slot(self.selected_slot_id)
            messagebox.Message(f"Slot deleted successfully: {deleted_slot}")
            self.master.populate_slots()


            self.destroy()

            

        except ValidationError as e:
            print(f"Validation Error: {e}")
            messagebox.showerror("Error", f"Validation Error: {e}")
        except NotFoundError as e:
            print(f"Error: {e}")
            messagebox.show_error("Error", f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            messagebox.show_error("Error", f"Unexpected error occurred: {e}")
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
            self.input_schedule.configure(values=slot_values)

            # Manually select the first value to trigger the callback
            if slot_values:
                self.input_schedule.set(slot_values[0])  # Set the first value
                self.after(100, lambda: self.on_slot_selected(slot_values[0]))  # Trigger the callback manually
        except NotFoundError as e:
            messagebox.showerror("Error", str(e))

    def on_slot_selected(self, selected_value=None):
        """Update the input fields based on the selected schedule slot."""
        selected_slot = selected_value if selected_value else self.input_schedule.get()
        print("Selected slot:", selected_slot)  # Debugging

        if selected_slot:
            try:
                # Retrieve the slot ID using the selected slot
                slot_id = self.slot_map.get(selected_slot, None)
                print("Selected slot ID:", slot_id)  # Debugging

                
                # Store the selected slot ID for later use (e.g., when submitting changes)
                self.selected_slot_id = slot_id
            except ValueError:
                messagebox.showerror(f"Error: Could not parse the selected slot '{selected_slot}'. Ensure it's in 'Day StartTime - EndTime' format.")
        else:
            print("No slot selected.")
