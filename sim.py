import random

# Load monkey names from a file
monkey_names = []
with open("monkey_names.txt") as monkey_names_file:
    for name in monkey_names_file:
        monkey_names.append(name.strip())

# Utility to generate a random number between min_val and max_val
def random_number(min_val, max_val):
    return min_val + (max_val - min_val) * random.random()

# Strategies for monkeys to decide their actions
def random_monkey(current_stock_price, history_of_stock_prices, history_of_change, monkey_money, amount_of_stock):
    return random.choice([1, 0, -1])

def buy_low_sell_high_monkey(current_stock_price, history_of_stock_prices, history_of_change, monkey_money, amount_of_stock):
    if len(history_of_stock_prices) > 10:
        average_past_prices = sum(history_of_stock_prices[-10:]) / 10
    else:
        average_past_prices = sum(history_of_stock_prices) / len(history_of_stock_prices)
    if average_past_prices > current_stock_price:
        return random.choices([1,-1,0], weights= [0.9,0.09, 0.01], k = 1)[0]
    elif average_past_prices < current_stock_price:
        return random.choices([-1,1,0], weights= [0.9,0.09, 0.01], k = 1)[0]
    return random.choices([0,1,1], weights= [0.9,0.09, 0.01], k = 1)[0]

def threshold_monkey(current_stock_price, history_of_stock_prices, history_of_change, monkey_money, amount_of_stock):
    initial_price = history_of_stock_prices[0]
    if current_stock_price < initial_price * 1.10:
        return random.choices([1,-1,0], weights= [0.9,0.09, 0.01], k = 1)[0]
    elif current_stock_price > initial_price * 1.50:
        return random.choices([-1,1,0], weights= [0.9,0.09, 0.01], k = 1)[0]
    return random.choices([0,1,1], weights= [0.9,0.09, 0.01], k = 1)[0]

def hold_monkey(current_stock_price, history_of_stock_prices, history_of_change, monkey_money, amount_of_stock):
    if current_stock_price <= history_of_stock_prices[0]:
        return random.choices([1,-1,0], weights= [0.9,0.09, 0.01], k = 1)[0]
    return random.choices([0,1,1], weights= [0.9,0.09, 0.01], k = 1)[0]

def scared_monkey(current_stock_price, history_of_stock_prices, history_of_change, monkey_money, amount_of_stock):
    initial_price = history_of_stock_prices[0]
    if current_stock_price < initial_price * 1.10:
        return random.choices([1,-1,0], weights= [0.9,0.09, 0.01], k = 1)[0]
    if history_of_change[-1] < 0:
        return random.choices([-1,1,0], weights= [0.9,0.09, 0.01], k = 1)[0]
    return random.choices([0,1,1], weights= [0.9,0.09, 0.01], k = 1)[0]

# List of strategies
strategies = [random_monkey, scared_monkey, hold_monkey, threshold_monkey, buy_low_sell_high_monkey]
strategie_names = ["random monkey", "scared monkey", "hold monkey", "threshold monkey", "buy low sell high monkey"]

# Simulation function
def play_simulation(number_of_monkeys, percentages_of_strategies, initial_capital, initial_stocks, no_of_rounds, monkey_names):
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
    for monkey in sorted_monkeys:
        name, money, owned_stocks, strategy_index = monkey
        net_worth = calculate_net_worth(monkey)
        print(f"{name}: Net Worth = {net_worth:.2f}, Money = {money:.2f}, Stocks = {owned_stocks}, Strategy = {strategie_names[strategy_index]}")

    # Aggregate strategy performance
    strategy_performance = {name: 0 for name in strategie_names}
    for monkey in list_of_monkeys:
        strategy_index = monkey[3]
        net_worth = calculate_net_worth(monkey)
        strategy_performance[strategie_names[strategy_index]] += net_worth

    print("\nStrategy Performance Summary:")
    for strategy, total_net_worth in strategy_performance.items():
        print(f"{strategy}: Total Net Worth = {total_net_worth:.2f}")

# Example usage
play_simulation(100, [0.20, 0.20, 0.20, 0.20, 0.20], 100, ["bananas", "apples", "grapes"], 2000, monkey_names)
