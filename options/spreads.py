from random import random

def get_symbols():
    symbols_file = open("s&p500.txt", "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


def get_prices(symbol, year_start=None, year_end=None):
    symbols_file = open("prices/monthly" + symbol + ".csv", "r")
    symbols_file.readline()
    lines = symbols_file.readlines()
    symbols_file.close()

    prices = []
    for line in lines:
        year = int(line[0] + line[1] + line[2] + line[3])
        if (year_start is not None and year < year_start) or \
                (year_end is not None and year > year_end):
            continue
        prices.append(float(line.rstrip('\n').split(',')[2]))
    return prices


def get_color(price, prev_price):
    return "green" if price >= prev_price else "red"


def analyze_binary_change():
    symbols = get_symbols()
    green_to_green = 0
    green_to_red = 0
    red_to_green = 0
    red_to_red = 0
    for symbol in symbols:
        prices = get_prices(symbol)

        prev_price = None
        prev_color = None
        for price in prices:
            # first iteration
            if prev_price is None:
                prev_price = price
                continue
            # second iteration
            if prev_color is None:
                prev_color = get_color(price, prev_price)
                prev_price = price
                continue

            # other iterations
            color = get_color(price, prev_price)
            if prev_color == "green" and color == "green":
                green_to_green += 1
            if prev_color == "green" and color == "red":
                green_to_red += 1
            if prev_color == "red" and color == "green":
                red_to_green += 1
            if prev_color == "red" and color == "red":
                red_to_red += 1

            prev_price = price
            prev_color = color

    total_green = green_to_green + green_to_red
    total_red = red_to_green + red_to_red
    print("total_green =", total_green)
    print("total_red =", total_red)
    print("green_to_green =", green_to_green)
    print("green_to_red =", green_to_red)
    print("red_to_green =", red_to_green)
    print("red_to_red =", red_to_red)

    red_chance_if_prev_green = \
        round(10000 * green_to_red / (green_to_green + green_to_red)) / 100
    red_chance_if_prev_red = \
        round(10000 * red_to_red / (red_to_green + red_to_red)) / 100
    print("green -> red ", red_chance_if_prev_green)
    print("red -> red ", red_chance_if_prev_red)


def analyze_change():
    symbols = get_symbols()
    change_after_green = []
    change_after_red = []
    for symbol in symbols:
        prices = get_prices(symbol)

        prev_price = None
        prev_color = None
        for price in prices:
            # first iteration
            if prev_price is None:
                prev_price = price
                continue
            # second iteration
            if prev_color is None:
                prev_color = get_color(price, prev_price)
                prev_price = price
                continue

            # other iterations
            color = get_color(price, prev_price)
            price_change = price / prev_price
            if prev_color == "green":
                change_after_green.append(price_change)
            else:
                change_after_red.append(price_change)

            prev_price = price
            prev_color = color

    change_after_green.sort()
    change_after_red.sort()

    fractions = 99
    for i in range(1, fractions + 1):
        fraction_size_green = len(change_after_green) / (fractions + 1)
        fraction_size_red = len(change_after_red) / (fractions + 1)

        percentile = round(10000 * i / (fractions + 1)) / 100
        price_after_green = round(10000 * change_after_green[round(i * fraction_size_green)]) / 100
        price_after_red = round(10000 * change_after_red[round(i * fraction_size_red)]) / 100
        print("Top", percentile, "percentile. After green:", price_after_green,
              "After red:", price_after_red)

    print("green sample size:", len(change_after_green))
    print("red sample size:", len(change_after_red))


def evaluate_spread(price_change, upper, lower, max_gain, max_loss):
    if price_change >= upper:
        return max_gain
    if price_change <= lower:
        return max_loss

    interval_length = upper - lower
    from_lower = price_change - lower
    ratio = from_lower / interval_length
    gain_loss_interval = max_gain - max_loss
    spread_value = max_loss + ratio * gain_loss_interval
    return spread_value


def backtest_spread_strategy(upper, lower, max_gain, max_loss,
                             required_color="green"):
    symbols = get_symbols()
    total_gain = 0
    sample_size = 0

    full_gains = 0
    full_losses = 0
    middles = 0
    total_middle = 0

    for symbol in symbols:
        prices = get_prices(symbol)
        # prices = get_prices(symbol, year_start=2010)
        # prices = get_prices(symbol, year_start=2005, year_end=2015)

        prev_price = None
        prev_color = None
        for price in prices:
            # first iteration
            if prev_price is None:
                prev_price = price
                continue
            # second iteration
            if prev_color is None:
                prev_color = get_color(price, prev_price)
                prev_price = price
                continue

            # other iterations
            color = get_color(price, prev_price)
            price_change = price / prev_price
            if prev_color == required_color:
                spread_value = evaluate_spread(price_change, upper, lower,
                                               max_gain, max_loss)
                # print("prev price =", round(100 * prev_price) / 100,
                #       "value =", spread_value)
                total_gain += spread_value
                sample_size += 1

                if spread_value == max_gain:
                    full_gains += 1
                elif spread_value == max_loss:
                    full_losses += 1
                else:
                    middles += 1
                    total_middle += spread_value

            prev_price = price
            prev_color = color

    print("total gain =", total_gain, "sample_size =", sample_size, "EV =",
          total_gain / sample_size)
    print("Wins =", full_gains, "Losses =", full_losses, "Middles =",
          middles, "Average middle =", total_middle / middles)


def simulate_trading(starting_capital, max_risk=0.5):
    # win_chance = 80.53
    win_value = 100
    loss_chance = 12.13
    loss_value = -400
    middle_chance = 7.34
    middle_value = -135

    months_trading = 24
    outcomes = []
    for i in range(100000):
        money = starting_capital
        # print("new simulation")
        for j in range(months_trading):
            trades = round(money * max_risk) // abs(loss_value)
            # print("money =", money, "trades =", trades)
            if trades == 0:
                break

            for k in range(trades):
                rng = random() * 100
                if rng < loss_chance:
                    money += loss_value
                elif rng < loss_chance + middle_chance:
                    money += middle_value
                else:
                    money += win_value
        outcomes.append(money)

    outcomes.sort()

    fractions = 99
    for i in range(1, fractions + 1):
        fraction_size = len(outcomes) / (fractions + 1)
        percentile = round(10000 * i / (fractions + 1)) / 100
        money = outcomes[round(i * fraction_size)]
        print("Top", percentile, "percentile. Money:", money)


def main():
    # analyze_binary_change()
    # analyze_change()
    # backtest_spread_strategy(0.95, 0.925, 100, -400)
    backtest_spread_strategy(0.927, 0.618, 272, -9728, "green")
    # simulate_trading(5000)


main()
