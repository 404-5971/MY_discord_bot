import random
import matplotlib.pyplot as plt
import numpy as np
import json

from const import STOCK_HISTORY_FILE

from stocks.write_file import write_to_file

try:
    with open(STOCK_HISTORY_FILE, 'r') as file:
        stock_history = json.load(file)
        stock_price = stock_history['DOWN'][-1]
except:
    stock_price = 10000

count = 0

def DOWN():
    global count, stock_price, count, it_happened
    rand = random.randint(1, 525600)
    if rand == 1:
        if stock_price > 0:
            stock_price *= 100
        else:
            stock_price /= 100
        it_happened = True
        count += 1
        write_to_file("DOWN", stock_price)
    else:
        if stock_price <= 0:
            stock_price = 1
        else:
            stock_price -= 0.1 #random.randint(1, 5)
        #print(stock_price)
        #count += 1
        write_to_file("DOWN", stock_price)

if __name__ == '__main__':
    prices = []
    it_happened = False
    while it_happened == False:
        DOWN()
        stock_price = round(stock_price, 2) 
        prices.append(stock_price)
        if count > 525600:
            it_happened = True
            print("FALSE")
    print(count)
    print(f"Stock price: ${stock_price}")

    # Plotting
    plt.plot(np.arange(count), prices, marker='o', linestyle='-')
    plt.title("Stock Price Curve")
    plt.xlabel("Time Steps")
    plt.ylabel("Stock Price")
    plt.grid(True)
    plt.show()
