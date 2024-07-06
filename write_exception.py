import csv
import datetime
import os

from const import EXCEPTION_FILE

def write_exception(traceback):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")
    current_date = datetime.date.today()

    file_exists = os.path.exists(EXCEPTION_FILE)
    with open(EXCEPTION_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['time', 'date', 'file', 'line', 'exception'])  # Write header only if the file is newly created

        writer.writerow([traceback])

if __name__ == '__main__':
    try:
        my_string = '1sfjalj'
        my_int = int(my_string)
    except Exception as e:
        write_exception(e, 'write_exception.py', 14)
