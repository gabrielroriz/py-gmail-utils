import hashlib
import datetime

def generate_csv_db_name(list_length):
    # Get current date and time
    current_time = datetime.datetime.now()

    # Create a hash based on the current time
    time_str = current_time.strftime('%Y-%m-%d_%H_%M_%S')
    hash_object = hashlib.sha256(time_str.encode())
    hash_hex = hash_object.hexdigest()

    # Format the final output
    return f"{current_time.strftime('%Y-%m-%d')}__{list_length}__{hash_hex[:8]}"