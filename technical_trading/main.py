

def get_daily_data(file):
    # Returns data from one day of normal trading hours (9:35 - 16:00) in a
    # 2D array [day][data]
    file = open(file, "r")
    file.readline()
    lines = file.readlines()
    file.close()

    prev_date = lines[0].split(" ")[0]
    days = []               # 2D array, contains data_in_day
    data_in_day = []        # 1D array, contains data

    for line in lines:
        date = line.split(" ")[0]
        if date != prev_date:
            data_in_day.reverse()
            # for test in data_in_day:
            #     print(test, end="")
            days.append(data_in_day)
            data_in_day = []
            prev_date = date

        # 15:25:00 gets stored as 152500 in time_batch, 04:15:00 as 41500
        time_batch = int(line[11] + line[12] + line[14] + line[15] + line[17]
                         + line[18])
        if time_batch <= 93000 or time_batch > 160000:
            continue

        data_in_day.append(line)

    """
    for day in days:
        for data in day:
            print(data, end="")
            """

    return days


def get_close_price(data: str):
    return float(data.split(',')[4])


def get_moving_average(cur_candle, cur_day, prev_day, period=10):
    # cur_candle describes the index of the candle in the given day
    #   (cur_candle = 0 ... time 9:35, cur_candle = 1 ... time 9:40)
    # period must not be too large (it must fit into 1 day)

    if cur_candle >= len(cur_day) or period >= len(cur_day):
        print("Cur_candle or period too large!")
        return None

    days_combined = prev_day + cur_day
    candle_index = len(prev_day) + cur_candle
    start_index = candle_index - period + 1

    total = 0
    for i in range(start_index, candle_index + 1):
        # close = float(days_combined[i].split(',')[4])
        close = get_close_price(days_combined[i])
        # print(days_combined[i], "close:", close)
        total += close

    average = total / (candle_index + 1 - start_index)
    return average


def is_average_ascending(cur_day, prev_day, candles=10, avg_period=10):
    prev_avg = get_moving_average(-1, cur_day, prev_day)
    for j in range(candles):
        avg = get_moving_average(j, cur_day, prev_day, avg_period)
        if avg <= prev_avg:
            # print("Not ascending.")
            return False
        prev_avg = avg
    # print("Ascending.")
    return True


def simulate_strategy_using_averages(leverage=5):
    leverage_fee = 0
    if leverage > 1:
        leverage_fee = 0.000173 if leverage <= 5 else 0.0007

    daily_data = get_daily_data("data_5min/MCD.csv")

    total_profit = 1
    trades = 0

    for i in range(len(daily_data) - 1):
        cur_day = daily_data[i]
        prev_day = daily_data[i + 1]
        date = cur_day[0].split(" ")[0]

        print("\n" + str(date))
        if not is_average_ascending(cur_day, prev_day, candles=5,
                                    avg_period=5):
            print("Skipping")
            continue

        buy_price = get_close_price(cur_day[4])
        sell_price = get_close_price(cur_day[-1])
        profit = sell_price / buy_price
        leveraged_profit = (profit - 1) * leverage + 1 - leverage_fee
        total_profit *= leveraged_profit
        trades += 1
        print("Profit:", round((profit - 1) * 100000) / 1000, "%. Leveraged "
              "profit:", round((leveraged_profit - 1) * 100000) / 1000,
              "%. Total profit:", round((total_profit - 1) * 100000) / 1000,
              "%")

    print("Total profit =", total_profit, "Trades:", trades)


def simulate_day(day, stop_loss=0.02, take_profit=0.01):
    init_open = float(day[0].split(',')[1])
    init_close = float(day[0].split(',')[4])
    trade = "long" if init_open < init_close else "short"
    print("Opening", trade, "position.")

    for i in range(1, len(day)):
        columns = day[i].split(',')
        time = columns[0].split(' ')[1]
        high = float(columns[2])
        low = float(columns[3])

        if trade == "long":
            if high > init_close * (1 + take_profit) and \
                    low < init_close * (1 - stop_loss):
                # both stop loss and take profit were hit; with no way to
                # know which came first, this trade doesn't count
                return None
            if high > init_close * (1 + take_profit):
                print("Taking profit.", time)
                return take_profit + 1
            if low < init_close * (1 - stop_loss):
                print("Stopping loss.", time)
                return 1 - stop_loss
        else:
            if low < init_close * (1 - take_profit) and \
                    high > init_close * (1 + stop_loss):
                return None
            if low < init_close * (1 - take_profit):
                print("Taking profit.", time)
                return take_profit + 1
            if high > init_close * (1 + stop_loss):
                print("Stopping loss.", time)
                return 1 - stop_loss

    # If neither stop loss nor take profit was hit during the day, close the
    # trade just before market hours end
    price_near_end = float(day[-1].split(',')[1])      # open price in last 5
    # minutes

    if trade == "long":
        print("Closing trade at market hours end. Profit:",
              price_near_end / init_close)
        return price_near_end / init_close
    print("Closing trade at market hours end. Profit:",
          init_close / price_near_end)
    return init_close / price_near_end


def simulate_strategy_using_trend_at_open(leverage=5):
    leverage_fee = 0
    if leverage > 1:
        leverage_fee = 0.000173 if leverage <= 5 else 0.0007

    daily_data = get_daily_data("data_5min/SPY.csv")

    positive_trades = 0
    negative_trades = 0
    total_profit = 1

    for day in daily_data:
        date = day[0].split(" ")[0]
        print('\n' + str(date))

        profit = simulate_day(day, stop_loss=0.005, take_profit=0.005)
        if profit is None:
            # ignore this trade
            print("Skipping")
            continue

        leveraged_profit = (profit - 1) * leverage + 1

        # total_profit *= profit
        total_profit *= leveraged_profit - leverage_fee

        if profit > 1:
            positive_trades += 1
        else:
            negative_trades += 1

        print("Leveraged profit:", round((leveraged_profit - 1) * 10000) /
              100, "%. Total profit:",
              round((total_profit - 1) * 10000) /
              100, "%")

    print("Positive trades:", positive_trades, "Negative trades:",
          negative_trades, "Total profit:", total_profit)


def main():
    # simulate_strategy_using_averages(5)
    simulate_strategy_using_trend_at_open(5)


main()
