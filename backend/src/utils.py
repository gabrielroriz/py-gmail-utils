import datetime

def generate_csv_db_name(list_length):
    # Get current date and time
    current_time = datetime.datetime.now()

    # Format the final output with 24-hour time format
    formatted_time = current_time.strftime('%Hh%M')

    # Properly format the output
    return f"{current_time.strftime('%Y-%m-%d')}__{formatted_time}__{list_length:06d}"