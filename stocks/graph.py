import json
import matplotlib.pyplot as plt

from const import STOCK_HISTORY_FILE, STOCK_GRAPH_PIC

def draw_graph(stock_names=None):
    plt.clf()  # Clear the current plot

    def read_file(stock_name):
        try:
            with open(STOCK_HISTORY_FILE, 'r') as file:
                stock_history = json.load(file)
                stock_y_values = stock_history.get(stock_name, [])
        except (FileNotFoundError, json.JSONDecodeError):
            stock_y_values = []

        # Ensure the x values match the length of y values
        stock_x_values = list(range(len(stock_y_values)))
        return stock_x_values, stock_y_values

    all_stocks = {
        'RNG': read_file('RNG'),
        'NVDA': read_file('NVDA'),
        'DOGE': read_file('DOGE'),
        'UP': read_file('UP'),
        'DOWN': read_file('DOWN'),
        'GAY': read_file('GAY'),
        'Line 7': ([0, 1, 2, 3, 4], [2, 3, 4, 5, 6]),
        'Line 8': ([0, 1, 2, 3, 4], [3, 1, 4, 1, 5]),
        'Line 9': ([0, 1, 2, 3, 4], [4, 5, 6, 7, 8]),
        'Line 10': ([0, 1, 2, 3, 4], [5, 4, 3, 2, 1])
    }

    if stock_names is None:
        stocks_to_plot = all_stocks.keys()
    else:
        stocks_to_plot = stock_names

    def get_latest_price(y_values):
        return round(y_values[-1], 2) if y_values else 'N/A'

    for stock_name in stocks_to_plot:
        if stock_name in all_stocks:
            x_values, y_values = all_stocks[stock_name]
            label = f'{stock_name} ${get_latest_price(y_values)}' if stock_name in ['RNG', 'PXL', 'NVDA', 'DOGE', 'UP', 'DOWN', 'GAY'] else stock_name
            plt.plot(x_values, y_values, label=label)

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Stock Graph')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout(rect=[0, 0, 0.75, 1])
    plt.savefig(STOCK_GRAPH_PIC, bbox_inches='tight')


if __name__ == "__main__":
    draw_graph()
# Show the plot
    plt.show()
