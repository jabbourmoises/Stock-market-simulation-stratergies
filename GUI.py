import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Load monkey names from a file
monkey_names = []
with open("monkey_names.txt") as monkey_names_file:
    for name in monkey_names_file:
        monkey_names.append(name.strip())

# Utility to generate a random number between min_val and max_val
def random_number(min_val, max_val):
    return min_val + (max_val - min_val) * random.random()

# Define your strategies (same as in the original code)...

# Simulation function
def play_simulation_gui(number_of_monkeys, percentages_of_strategies, initial_capital, initial_stocks, no_of_rounds, monkey_names):
    stock_prices = [initial_capital * random_number(0.01, 0.2) for _ in initial_stocks]
    selected_monkey_names = random.sample(monkey_names, number_of_monkeys)
    list_of_monkeys = []
    history_of_stock_prices = [[price] for price in stock_prices]
    history_of_change = [[0] for _ in stock_prices]

    # Initialize monkeys
    for monkey_name in selected_monkey_names:
        money = initial_capital
        owned_stocks = {stock: 0 for stock in initial_stocks}
        strategy_index = random.choices(
            range(len(percentages_of_strategies)),
            weights=percentages_of_strategies,
            k=1
        )[0]
        list_of_monkeys.append((monkey_name, money, owned_stocks, strategy_index))

    # Play the game
    for _ in range(no_of_rounds):
        for stock_index, stock in enumerate(initial_stocks):
            no_bought, no_sold = 0, 0
            for index, monkey in enumerate(list_of_monkeys):
                name, money, owned_stocks, strategy_index = monkey
                action = strategies[strategy_index](
                    stock_prices[stock_index],
                    history_of_stock_prices[stock_index],
                    history_of_change[stock_index],
                    money,
                    owned_stocks[stock]
                )
                if action == 1 and money >= stock_prices[stock_index]:
                    money -= stock_prices[stock_index]
                    owned_stocks[stock] += 1
                    no_bought += 1
                elif action == -1 and owned_stocks[stock] > 0:
                    money += stock_prices[stock_index]
                    owned_stocks[stock] -= 1
                    no_sold += 1
                list_of_monkeys[index] = (name, money, owned_stocks, strategy_index)

            total_inventory = sum(monkey[2][stock] for monkey in list_of_monkeys)
            total = total_inventory + no_sold
            if total > 0:
                change = ((no_bought - no_sold) / total) + random_number(-0.1, 0.1)
            else:
                change = random_number(-0.1, 0.1)
            stock_prices[stock_index] *= (1 + change)
            history_of_change[stock_index].append(change)
            history_of_stock_prices[stock_index].append(stock_prices[stock_index])

    # Calculate net worth and sort monkeys
    def calculate_net_worth(monkey):
        name, money, owned_stocks, _ = monkey
        stock_value = sum(owned_stocks[stock] * stock_prices[initial_stocks.index(stock)] for stock in owned_stocks)
        return money + stock_value

    sorted_monkeys = sorted(list_of_monkeys, key=calculate_net_worth, reverse=True)

    # Update the graph and rankings
    update_graph(history_of_stock_prices, initial_stocks)
    update_rankings(sorted_monkeys, calculate_net_worth)

# Function to update the graph
def update_graph(history_of_stock_prices, stocks):
    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)
    for stock_index, stock in enumerate(stocks):
        ax.plot(history_of_stock_prices[stock_index], label=stock)
    ax.legend()
    ax.set_title("Stock Price Trends")
    ax.set_xlabel("Rounds")
    ax.set_ylabel("Price")

    # Update the canvas
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()

# Function to update rankings
def update_rankings(sorted_monkeys, calculate_net_worth):
    for widget in rankings_frame.winfo_children():
        widget.destroy()

    ttk.Label(rankings_frame, text="Rankings", font=("Arial", 14)).pack(anchor="w")
    for rank, monkey in enumerate(sorted_monkeys, start=1):
        name, money, owned_stocks, strategy_index = monkey
        net_worth = calculate_net_worth(monkey)
        ttk.Label(
            rankings_frame,
            text=f"{rank}. {name}: Net Worth = {net_worth:.2f}, Strategy = {strategie_names[strategy_index]}",
        ).pack(anchor="w")

# Setup the GUI
window = tk.Tk()
window.title("Monkey Stock Simulation")
window.geometry("1000x700")

# Title
title_label = tk.Label(window, text="Monkey Stock Simulation", font=("Arial", 24))
title_label.pack()

# Frame for rankings
rankings_frame = tk.Frame(window)
rankings_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

# Run Simulation Button
start_button = ttk.Button(window, text="Run Simulation", command=lambda: play_simulation_gui(100, [0.20] * 5, 100, ["bananas", "apples", "grapes"], 2000, monkey_names))
start_button.pack(side=tk.BOTTOM, pady=10)

# Start the Tkinter event loop
window.mainloop()
