import matplotlib.pyplot as plt
import numpy as np


def generate_stock_price(num_iterations):
    prices = []
    num = 1  # Starting value
    for _ in range(num_iterations):
        num_zeros = len(str(int(num)))
        if num_zeros == 1:
            multiplier = 1.1  # Minimum multiplier to avoid constant value
        elif num_zeros >= 2:
            multiplier = 1
            for _ in range(num_zeros):
                multiplier = str(multiplier) + '0' 
            multiplier = insert_decimal(multiplier)
        num *= multiplier
        prices.append(num)

    return prices


def insert_decimal(num):
    num_str = num
    result = num_str[:1] + '.' + num_str[1:]
    result += '1'
    return float(result)  # Convert back to float if needed

# Parameters
num_iterations = 18420690  # Number of iterations (time steps)

# Generate stock prices
stock_prices = generate_stock_price(num_iterations)

# Plotting
plt.plot(np.arange(num_iterations), stock_prices, marker='o', linestyle='-')
plt.title("Stock Price Curve")
plt.xlabel("Time Steps")
plt.ylabel("Stock Price")
plt.grid(True)
plt.show()
