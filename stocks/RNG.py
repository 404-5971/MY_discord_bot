import random

from stocks.write_file import write_to_file

last_number = 500

def stock1():
    global last_number
    change = random.uniform(-0.01, 0.01)  # Random change within +/- 1%
    change_amount = last_number * change
    new_number = max(0, min(1000, last_number + change_amount))  # Bound between 0 and 1000
    last_number = int(new_number)
    
    write_to_file("RNG", last_number)

    return last_number
