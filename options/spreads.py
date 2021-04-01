from random import random
from os import listdir
from math import floor


class Spread:

    def __init__(self, price, strike1, premium1, strike2, premium2):
        # Selling option1, buying option2
        self.price = price
        self.strike1 = strike1
        self.premium1 = premium1
        self.strike2 = strike2
        self.premium2 = premium2
        self.type = "put" if strike1 > strike2 else "call"


def get_symbols():
    symbols_file = open("s&p500.txt", "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


def get_prices(file, year_start=None, year_end=None):
    price_file = open(file, "r")
    price_file.readline()
    lines = price_file.readlines()
    price_file.close()

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


def analyze_binary_change_monthly():
    # This hypothesis states that if a given month is green, the next month
    # is likely to be green as well. In other words, the likelihood of a
    # green month is higher if the previous month was also green.
    # This hypothesis was disproved.
    price_files = listdir("prices/monthly")
    green_to_green = 0
    green_to_red = 0
    red_to_green = 0
    red_to_red = 0
    for file in price_files:
        prices = get_prices("prices/monthly/" + file)

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


def analyze_binary_change_weekly():
    """
    If 2 weeks are green, will the next week be likely green too?

    No.
    """
    price_files = listdir("prices/weekly")
    print(price_files)

    # How many green and red weeks there are in total
    total_green = 0
    total_red = 0

    # How many green and red weeks there are after 2 green weeks
    hypothesis_green = 0
    hypothesis_red = 0

    for file in price_files:
        prices = get_prices("prices/weekly/" + file)
        if len(prices) < 4:
            continue

        for i in range(2, len(prices) - 1):
            prev_prev_price = prices[i - 2]
            prev_price = prices[i - 1]
            cur_price = prices[i]
            next_price = prices[i + 1]

            week1 = get_color(prev_price, prev_prev_price)
            week2 = get_color(cur_price, prev_price)
            week3 = get_color(next_price, cur_price)
            if week1 == "green" and week2 == "green":
                if week3 == "green":
                    hypothesis_green += 1
                else:
                    hypothesis_red += 1

            if week3 == "green":
                total_green += 1
            else:
                total_red += 1

    print("Hypothesis green:", hypothesis_green)
    print("Hypothesis red:", hypothesis_red)
    print("Hypothesis win rate:", hypothesis_green / (hypothesis_green + hypothesis_red))
    print("Total green:", total_green)
    print("Total red:", total_red)
    print("Total win rate:", total_green / (total_green + total_red))


def print_percentiles(arr1, arr1name, arr2, arr2name, fractions=100):
    arr1.sort()
    arr2.sort()

    for i in range(0, fractions):
        fraction_size_arr1 = len(arr1) / fractions
        fraction_size_arr2 = len(arr2) / fractions

        percentile = round(10000 * i / fractions) / 100

        arr1value = round(10000 * arr1[floor(i * fraction_size_arr1)]) / 100
        arr2value = round(10000 * arr2[floor(i * fraction_size_arr2)]) / 100
        print("Top", percentile, "percentile.",  arr1name + ":", arr1value,
              arr2name + ":", arr2value)

    print("Top 100.0 percentile.",  arr1name + ":",
          round(10000 * arr1[-1]) / 100, arr2name + ":",
          round(10000 * arr2[-1]) / 100)

    print(arr1name, "sample size:", len(arr1))
    print(arr2name, "sample size:", len(arr2))

    total1 = 0
    for i in arr1:
        total1 += i
    avg1 = total1 / len(arr1)

    total2 = 0
    for i in arr2:
        total2 += i
    avg2 = total2 / len(arr2)

    print(arr1name, "average:", avg1)
    print(arr2name, "average:", avg2)


def analyze_change_monthly():
    price_files = listdir("prices/monthly")
    change_after_green = []
    change_after_red = []
    for file in price_files:
        prices = get_prices("prices/monthly/" + file)

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

    print_percentiles(change_after_green, "Green", change_after_red, "Red")


def analyze_change_weekly():
    price_files = listdir("prices/weekly")
    price_files = ["SPY.csv"]

    change_random = []
    change_hypothesis = []
    for file in price_files:
        print(file)

        prices = get_prices("prices/weekly/" + file)
        if len(prices) < 4:
            continue

        for i in range(2, len(prices) - 1):
            prev_prev_price = prices[i - 2]
            prev_price = prices[i - 1]
            cur_price = prices[i]
            next_price = prices[i + 1]

            change = next_price / cur_price

            week1 = get_color(prev_price, prev_prev_price)
            week2 = get_color(cur_price, prev_price)
            if week1 == "green" and week2 == "green":
                change_hypothesis.append(change)

            change_random.append(change)
            # print("change =", change, "cur =", cur_price, "next =",
            # next_price)

    print_percentiles(change_random, "Random", change_hypothesis,
                      "Hypothesis")


def is_fully_otm(price_change, closer, option_type):
    if option_type == "put" and price_change >= closer:
        return True
    if option_type == "call" and price_change <= closer:
        return True
    return False


def is_fully_itm(price_change, further, option_type):
    if option_type == "put" and price_change <= further:
        return True
    if option_type == "call" and price_change >= further:
        return True
    return False


def evaluate_spread(price_change, spread: Spread):
    closer = spread.strike1 / spread.price
    further = spread.strike2 / spread.price
    max_gain = (spread.premium1 - spread.premium2) * 100
    max_loss = abs(spread.strike1 - spread.strike2) * -100 + max_gain

    print("Price change =", round(price_change * 1000) / 1000, end="; ")

    if is_fully_otm(price_change, closer, spread.type):
        print("Max gain.", round(max_gain * 1000) / 1000)
        return max_gain, "max_gain"
    if is_fully_itm(price_change, further, spread.type):
        print("Max loss.", round(max_loss * 1000) / 1000)
        return max_loss, "max_loss"

    interval_length = abs(closer - further)
    from_further = abs(price_change - further)
    ratio = from_further / interval_length
    gain_loss_interval = max_gain - max_loss
    spread_value = max_loss + ratio * gain_loss_interval
    print("Middle.", round(spread_value * 1000) / 1000)
    return spread_value, "middle"


def is_sublist_ascending(arr, lowest_index, length):
    for i in range(lowest_index, length):
        if arr[i] > arr[i + 1]:
            return False
    return True


def does_condition_hold(condition, arr, lowest_index, length):
    for i in range(lowest_index, length):
        if condition == "green" and arr[i] > arr[i + 1]:
            return False
        if condition == "red" and arr[i] < arr[i + 1]:
            return False
    return True


def backtest_spread_strategy(file, spread: Spread, condition=None,
                             weeks_required=0):
    total_gain = 0
    sample_size = 0
    skipped = 0

    full_gains = 0
    full_losses = 0
    middles = 0
    total_middle = 0

    prices = get_prices(file)
    for i in range(weeks_required, len(prices) - 1):
        # Ignore the current week if there aren't enough green weeks before
        # (as specified by green_weeks_required, with 0 being no condition
        # at all)
        if not does_condition_hold(condition, prices, i - weeks_required, i):
            skipped += 1
            continue

        price_change = prices[i + 1] / prices[i]
        spread_value, result = evaluate_spread(price_change, spread)
        # print("prev_price =", prices[i - 1], "cur_price =", prices[i],
        #       "price change =", round(100 * price_change) / 100)
        total_gain += spread_value
        sample_size += 1

        if result == "max_gain":
            full_gains += 1
        elif result == "max_loss":
            full_losses += 1
        else:
            middles += 1
            total_middle += spread_value

    average_middle = None if middles == 0 else total_middle / middles
    ev = total_gain / sample_size
    collateral = 100 * (abs(spread.strike1 - spread.strike2) -
                        spread.premium1 + spread.premium2)
    print("Collateral =", collateral)
    yearly_ev = 52 * ev * sample_size / (sample_size + skipped)

    print("total gain =", total_gain, "sample_size =", sample_size,
          "skipped:", skipped, "EV =", ev)
    print("Wins =", full_gains, "Losses =", full_losses, "Middles =",
          middles, "Average middle =", average_middle)
    print("yearly_EV =", yearly_ev, "Yearly return:",
          round(yearly_ev / collateral * 10000) / 100, "%")


def backtest_condor(file, put_spread: Spread,
                    call_spread: Spread, green_weeks_required=0):
    total_gain = 0
    sample_size = 0
    skipped = 0

    full_losses = 0
    partial_losses = 0
    gains = 0

    loss_sum = 0
    gain_sum = 0

    prices = get_prices(file, 2017, 2020)
    # prices = get_prices(file)
    for i in range(green_weeks_required, len(prices) - 1):
        # Ignore the current week if there aren't enough green weeks before
        # (as specified by green_weeks_required, with 0 being no condition
        # at all)
        if not is_sublist_ascending(prices, i - green_weeks_required, i):
            skipped += 1
            continue

        print("current price:", prices[i])

        price_change = prices[i + 1] / prices[i]
        put_spread_value, put_result = evaluate_spread(price_change, put_spread)
        call_spread_value, call_result = evaluate_spread(price_change, call_spread)

        value = put_spread_value + call_spread_value
        total_gain += value
        sample_size += 1

        if put_result == "max_loss" or call_result == "max_loss":
            print("Max loss.", round(value * 1000) / 1000)
            loss_sum += value
            full_losses += 1
        elif value < 0:
            print("Partial loss.", round(value * 1000) / 1000)
            loss_sum += value
            partial_losses += 1
        else:
            print("Gain.", round(value * 1000) / 1000)
            gain_sum += value
            gains += 1

    losses = full_losses + partial_losses
    average_gain = None if gains == 0 else gain_sum / gains
    average_loss = None if losses == 0 else loss_sum / losses
    ev = total_gain / sample_size
    # collateral = (spread.strike1 - spread.strike2) * 100
    # yearly_ev = 52 * ev * sample_size / (sample_size + skipped)

    print("total gain =", total_gain, "sample_size =", sample_size,
          "skipped:", skipped, "EV =", ev)
    print("Wins =", gains, "Full losses =", full_losses, "Partial losses =",
          partial_losses, "Average gain =", average_gain, "Average loss =",
          average_loss)
    #print("yearly_EV =", yearly_ev, "Yearly return:",
    #    round(yearly_ev / collateral * 10000) / 100, "%")


def simulate_trading(starting_capital, max_risk=0.5):
    # TODO: needs major changes
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


def random_numbers():
    file_spy = "prices/weekly/SPY.csv"
    file_amd = "prices/weekly/AMD.csv"
    file_gld = "prices/weekly/GLD.csv"
    file_adm = "prices/weekly/ADM.csv"
    file_cl = "prices/weekly/CL.csv"
    file_abbv = "prices/weekly/ABBV.csv"
    spread1 = Spread(175.20, 175, 1.53, 165, 0.10)
    spread2 = Spread(175.20, 167.5, 0.15, 140, 0.01)
    spread3 = Spread(174.87, 174, 1.24, 169, 0.29)
    spread4 = Spread(174.87, 172.5, 0.79, 162.50, 0.07)
    spread_amd = Spread(78.06, 78, 2.01, 72, 0.35)
    # backtest_spread_strategy(file_spy, spread3, 1)

    # GLD, cca 18.5% IV (nadprůměr)
    condor_put1 = Spread(174.94, 174, 1.34, 169, 0.33)
    condor_call1 = Spread(174.94, 176, 1.27, 181, 0.26)

    # AMD, cca 48% IV (podprůměr)
    condor_put2 = Spread(78.05, 78, 2.01, 73, 0.48)
    condor_call2 = Spread(78.05, 78.5, 1.81, 83.5, 0.51)

    condor_put2_2 = Spread(78.05, 78, 2.01, 68, 0.12)
    condor_call2_2 = Spread(78.05, 78.5, 1.81, 88.5, 0.09)

    # SPY, cca 8% IV (velký podprůměr)
    condor_put3 = Spread(236.29, 236, 0.91, 231, 0.16)
    condor_call3 = Spread(236.29, 237, 0.75, 242, 0.04)

    # Další GLD
    condor_put4 = Spread(174.94, 174, 1.34, 160, 0.06)
    condor_call4 = Spread(174.94, 176, 1.27, 190, 0.04)

    # ADM
    condor_put5 = Spread(46.08, 46, 0.59, 41, 0.06)
    condor_call5 = Spread(46.08, 46.5, 0.42, 51.5, 0.06)

    # CL
    condor_put6 = Spread(75.95, 75.50, 0.6, 70, 0.04)
    condor_call6 = Spread(75.95, 76.50, 0.54, 82, 0.05)

    # ABBV
    condor_put7 = Spread(86.23, 86, 1.03, 80, 0.19)
    condor_call7 = Spread(86.23, 87, 0.75, 93, 0.04)

    # GLD, cca 18.5% IV (nadprůměr), více otm
    condor_put8 = Spread(174.94, 172.5, 0.86, 162.5, 0.09)
    condor_call8 = Spread(174.94, 178, 0.65, 188, 0.06)

    backtest_condor(file_spy, condor_put1, condor_call1, 2)


def main():
    # analyze_change_weekly()
    # analyze_change_monthly()
    # analyze_binary_change_monthly()

    spread1 = Spread(367.86, 366, 7.39, 200, 0.01)
    spread2 = Spread(367.86, 368, 8.15, 450, 0.01)
    backtest_condor("prices/monthly/SPY.csv", spread1, spread2)


main()
