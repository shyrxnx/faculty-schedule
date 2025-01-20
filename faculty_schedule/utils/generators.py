import uuid
import time

def generate_id():
    # Generate a timestamp-based ID between 1000 and 9999999999
    timestamp = int(time.time() * 1000)
    return timestamp % 9999999999 + 1000