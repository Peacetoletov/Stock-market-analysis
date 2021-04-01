"""
This script simulates the returns of this strategy:
1. Use daily close price.
2. If the current price is All Time High or highest in the last year,
   buy.
3. Look at the lowest price of the last month. If the current price is
   lower at any point in the day, sell.
4. Repeat steps 2 and 3.

Also simulate how different levels of leverage (1-20) affect the returns. Use
S&P500 data going back to 1928.
"""

# TODO: continue


def get_low_and_close_prices(file, year_start=None, year_end=None):
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

        date = line.rstrip('\n').split(',')[0]
        low = float(line.rstrip('\n').split(',')[1])
        close = float(line.rstrip('\n').split(',')[2])
        prices.append((low, close, date))
    return prices


def get_last_years_highest_price(prices, i):
    # Returns the highest close price from the last 253 trading days
    # Beginning index: i - 253 (or 0 if there aren't enough prices)
    # Ending index: i - 1

    beginning_index = max(i - 253, 0)
    highest = prices[beginning_index][1]
    for j in range(beginning_index, i):
        close = prices[j][1]
        if close > highest:
            highest = close

    return highest


def get_recent_lowest_price(prices, i, lookback_size):
    # Returns the lowest close price from this interval:
    # Beginning index: i - lookback_size + 1
    # Ending index: i - 1
    # Interval length: lookback_size - 1

    lowest = prices[i - lookback_size + 1][1]
    for j in range(i - lookback_size + 2, i):
        close = prices[j][1]
        if close < lowest:
            lowest = close

    return lowest


def simulate(file="data_daily/^GSPC.csv", leverage=1, year_start=None,
             year_end=None):
    prices = get_low_and_close_prices(file, year_start, year_end)

    # look at the lowest price in the last 20 trading days (28 normal days)
    lookback_size = 20      # original was 20

    total_return = 1
    holding = False
    buy_price = None

    for i in range(lookback_size - 1, len(prices)):
        low, price, date = prices[i]
        last_highest = get_last_years_highest_price(prices, i)
        recent_lowest = get_recent_lowest_price(prices, i, lookback_size)

        if not holding:
            if price > last_highest:
                buy_price = price
                print("Buying at", round(buy_price * 1000) / 1000, '\t', date)
                holding = True
        else:
            if low < recent_lowest:
                sell_price = recent_lowest
                print("Selling at", round(sell_price * 1000) / 1000, '\t', date)
                total_return *= sell_price / buy_price
                holding = False

    if holding:
        sell_price = prices[-1][1]
        print("Selling at", round(sell_price * 1000) / 1000)
        total_return *= sell_price / buy_price

    print("Total return", round(total_return * 1000) / 1000)


def main():
    simulate()


main()
