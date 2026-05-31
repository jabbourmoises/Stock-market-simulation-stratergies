import numpy as np
import random
import sys

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

def score_end(monkey_money, amount_of_stock, stock_price, initial_worth):
    current_worth = amount_of_stock*stock_price + monkey_money
    return current_worth/initial_worth

def max_step(current_stock_price, history_of_stock_prices, history_of_change, monkey_money, amount_of_stock, round, no_rounds, depth,a,b, initial_worth, monkey_numbers, prev_total):
    if round >= no_rounds+1:
        return score_end(monkey_money, amount_of_stock, current_stock_price, initial_worth)
    if depth == 0:
        return score_end(monkey_money, amount_of_stock, current_stock_price, initial_worth)

    results = []
    new_total = prev_total
    change = random_number(-0.1, 0.1)
    for moves in [1,0,-1]: 
        if monkey_money < current_stock_price and moves == 1:
            continue
        new_prices = history_of_stock_prices.copy()
        new_changes = history_of_change.copy()
        if moves == 1:
            monkey_money -= current_stock_price
            amount_of_stock += 1
            new_total = prev_total + 1 
        if moves == -1:
            monkey_money += current_stock_price
            amount_of_stock -= 1
            change = random_number(-0.1, 0.1)
            new_total = prev_total - 1 
        current_stock_price *= (1+change)
        new_prices.append(current_stock_price)
        new_changes.append(change)

        result = min_step(current_stock_price, new_prices, new_changes, monkey_money, amount_of_stock, round+1, no_rounds, depth-1,a,b, initial_worth, monkey_numbers, new_total)
        results.append(result)
        if result >= a:
            a = result
        if b <= a:
            break
    return max(results)

def min_step(current_stock_price, history_of_stock_prices, history_of_change, monkey_money, amount_of_stock, round, no_rounds, depth,a,b, initial_worth, monkey_numbers, prev_total):
    if round >= no_rounds+1:
        return score_end(monkey_money, amount_of_stock, current_stock_price, initial_worth)
    if depth == 0:
        return score_end(monkey_money, amount_of_stock, current_stock_price, initial_worth)

    results = []
    no_bought = 0
    no_sold = 0
    new_total = prev_total
    change = 0
    for i,n in enumerate(monkey_numbers):
        if i == len(monkey_numbers)-1:
            break
        action = strategies[i](current_stock_price ,history_of_stock_prices,history_of_change,monkey_money,amount_of_stock)
        if action == 1:
            no_bought += 1
            new_total += 1
        elif action == -1:
            no_sold += 1
            new_total -= 1
    if new_total > 0:
        change = ((no_bought - no_sold) /(new_total+no_sold)) + random_number(-0.1, 0.1)
    else:
        change = random_number(-0.1, 0.1)    
    current_stock_price *= (1+change)
    new_prices = history_of_stock_prices.copy()
    new_changes = history_of_change.copy()
    new_prices.append(current_stock_price)
    new_changes.append(change)
       
    result = max_step(current_stock_price, new_prices, new_changes, monkey_money, amount_of_stock, round+1, no_rounds, depth-1, a, b, initial_worth, monkey_numbers, new_total)
    results.append(result)

    return min(results)

import numpy as np

def create_stock_array(current_stock_price, history_of_stock_prices, history_of_change, monkey_money):
    history_of_stock_prices_array = np.pad(
        np.array(history_of_stock_prices[-20:][::-1]), 
        (0, max(0, 20 - len(history_of_stock_prices))), 
        'constant'
    )
    
    history_of_change_array = np.pad(
        np.array(history_of_change[-20:][::-1]), 
        (0, max(0, 20 - len(history_of_change))), 
        'constant'
    )
    
    current_stock_price_array = np.array([current_stock_price])
    monkey_money_array = np.array([monkey_money])
    
    combined_array = np.concatenate((
        history_of_stock_prices_array,
        history_of_change_array,
        current_stock_price_array,
        monkey_money_array
    ))
    
    result_array = np.pad(
        combined_array,
        (0, max(0, 42 - len(combined_array))),
        'constant'
    ).reshape(42, 1)
    
    return result_array

    
    return result_array
def find_next_move(current_stock_price, history_of_stock_prices, history_of_change, monkey_money, amount_of_stock, monkey_numbers, depth, round, no_rounds, prev_total):
    global weights, biases
    res = {}
    a = -999999999999999
    b = 9999999999999999
    change = random_number(-0.1, 0.1)

    initial_worth = monkey_money + amount_of_stock*current_stock_price
    new_total = prev_total
    for moves in [1,0,-1]:
        if monkey_money < current_stock_price and moves == 1:
            continue
        new_prices = history_of_stock_prices.copy()
        new_changes = history_of_change.copy()
        if moves == 1:
            monkey_money -= current_stock_price
            amount_of_stock += 1
            new_total = prev_total + 1 
        if moves == -1:
            monkey_money += current_stock_price
            amount_of_stock -= 1
            change = random_number(-0.1, 0.1)
            new_total = prev_total - 1 
        current_stock_price *= (1+change)
        new_prices.append(current_stock_price)
        new_changes.append(change)

        res[moves] = min_step(current_stock_price, new_prices, new_changes, monkey_money, amount_of_stock, round+1, no_rounds, depth-1,a,b, initial_worth, monkey_numbers, new_total)

    weights, biases = back_propagation(sigmoid, sigmoid_prime, weights, biases, create_stock_array(current_stock_price, history_of_stock_prices, history_of_change, monkey_money), np.array([[max(list(res))]]), 0.04 )
    r = max(zip(res.values(), res.keys()))[1]
    return r


def nn_monkey(current_stock_price, history_of_stock_prices, history_of_change, monkey_money, amount_of_stock, number_of_monkeys, percentages_of_stratergies, round, no_rounds, total):
    global weights, biases
    monkey_numbers = [number_of_monkeys*p for p in percentages_of_stratergies]
    return find_next_move(current_stock_price, history_of_stock_prices, history_of_change, monkey_money, amount_of_stock, monkey_numbers, 10, round, no_rounds, total)



# List of strategies
strategies = [random_monkey, scared_monkey, hold_monkey, threshold_monkey, buy_low_sell_high_monkey, nn_monkey]
strategie_names = ["random monkey", "scared monkey", "hold monkey", "threshold monkey", "buy low sell high monkey", "nn monkey"]

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
        if _%20 == 0:
            print("round: ", _)
        for stock_index, stock in enumerate(initial_stocks):
            no_bought, no_sold = 0, 0
            for index, monkey in enumerate(list_of_monkeys):
                name, money, owned_stocks, strategy_index = monkey
                if strategy_index != 5:
                    action = strategies[strategy_index](
                        stock_prices[stock_index],
                        history_of_stock_prices[stock_index],
                        history_of_change[stock_index],
                        money,
                        owned_stocks[stock]
                    )
                else:
                    action = strategies[strategy_index](
                        stock_prices[stock_index],
                        history_of_stock_prices[stock_index],
                        history_of_change[stock_index],
                        money,
                        owned_stocks[stock],
                        number_of_monkeys,
                        percentages_of_strategies,
                        _,
                        no_of_rounds,
                        sum(monkey[2][stock] for monkey in list_of_monkeys)
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
        #print(f"{name}: Net Worth = {net_worth:.2f}, Money = {money:.2f}, Stocks = {owned_stocks}, Strategy = {strategie_names[strategy_index]}")

    # Aggregate strategy performance
    strategy_performance = {name: 0 for name in strategie_names}
    for monkey in list_of_monkeys:
        strategy_index = monkey[3]
        net_worth = calculate_net_worth(monkey)
        strategy_performance[strategie_names[strategy_index]] += net_worth

    print("\nStrategy Performance Summary:")
    for strategy, total_net_worth in strategy_performance.items():
        print(f"{strategy}: Total Net Worth = {total_net_worth:.2f}")


def sigmoid(X):
   return 1/(1+np.exp(-X))

def sigmoid_prime(x):
    return sigmoid(x)*(1-sigmoid(x))

def step(X):
    return np.heaviside(X, 0)

def network(A, weights, biases, input):
    a = []
    a.append(input)
    n = len(weights)
    for i in range(1,n):
        a.append(A(np.add(np.dot(weights[i], a[i-1]), biases[i])))
    return a[n-1]

def error(true, predicted):
    return np.sum(np.square(np.subtract(true, predicted)))/2

def calc_r(prev_layer_size, curr_layer_size, rnn):
    if rnn == False:
        temp = (prev_layer_size+curr_layer_size)/2
    else:
        temp = (prev_layer_size+2*curr_layer_size)/2
    return (3/temp)**0.5



def create_initial_conditions(layer_size, rnn):
    layer_weights = [None]
    step_weights = [None]
    biases = [None]

    for i, size in enumerate(layer_size):
        if i == 0:
            continue
        r = calc_r(layer_size[i-1],size, rnn[i])
        layer_weights.append(2*r*np.random.rand(size, layer_size[i-1])-r)
        biases.append(2 *r*np.random.rand(size, 1)-r)

    return layer_weights, step_weights, biases

def back_propagation(A, A_prime, weights, biases, inputs, expected_output, gama):
    n = len(weights)
    a = [inputs]
    dot = [None]
    delta = [None for i in range(n)]

    for i in range(1, n):
        s = np.dot(weights[i], a[i-1])
        s = np.add(s,biases[i])
        dot.append(s)
        if i == n-1:
            temp = np.exp(s)
            a.append(np.multiply(temp,1/np.sum(temp)))
        else:
            a.append(A(dot[i]))
    delta[-1] = np.dot(np.identity(expected_output.shape[0]) + (-1*a[-1]), expected_output)
    for i in range(n-2,0,-1):
        delta[i] = np.multiply(A_prime(dot[i]), np.dot(np.transpose(weights[i+1]), delta[i+1]) )

    for i in range(1,n):
        biases[i] = biases[i] + delta[i]*gama
        weights[i] = weights[i] + gama*np.dot(delta[i], np.transpose(a[i-1]))
    return weights, biases

inputs1 = []
test = []

def num_to_expected(num):
    return np.array([[1] if i == num else [0] for i in range(10)])

weights, _ , biases = create_initial_conditions([42,20,10,1],[False, False, False, False])

ep = 90
weights_file = np.load("neural_network" + str(ep) + "_Weights" + ".npz", allow_pickle=True)
weights = [weights_file[key] for key in weights_file]  # Extract all arrays

# Load biases
biases_file = np.load("neural_network" + str(ep) + "_Biases" + ".npz", allow_pickle=True)
biases = [biases_file[key] for key in biases_file]  # Extract all arrays

play_simulation(100, [0.16, 0.17, 0.17, 0.17, 0.17, 0.16], 100, ["bananas", "apples", "grapes"], 400, monkey_names)

# ep = 0
# while ep < 100:
#     if ep%10 == 0:
#         np.savez("neural_network" + str(ep) + "_Weights" + ".npz", *weights)
#         np.savez("neural_network" + str(ep) + "_Biases" + ".npz", *biases)
#     play_simulation(100, [0.16, 0.17, 0.17, 0.17, 0.17, 0.16], 100, ["bananas", "apples", "grapes"], 400, monkey_names)
#     ep += 1



