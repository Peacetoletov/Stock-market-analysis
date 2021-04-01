"""
Strategy - short UVXY at the end of the day, if the day was red and the
previous day was also red. Exit trade at the end of the first green day.
"""


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


def is_sublist_descending(arr, lowest_index, length):
    # print("Comparing.")
    for i in range(lowest_index, lowest_index + length):
        # print("arr[i] =", arr[i], "arr[i + 1] =", arr[i + 1])
        if arr[i] < arr[i + 1]:
            return False
    return True


def simulate(year_start=None, year_end=None, red_days_required=2):
    prices = get_prices("data_daily/uvxy.csv", year_start, year_end)

    total_gain = 1
    total_trades = 0
    sold_at = None      # float if a position is open, None otherwise

    for i in range(red_days_required, len(prices)):
        price_today = prices[i]
        price_yesterday = prices[i - 1]
        print("Price 1 =", round(price_yesterday * 1000) / 1000, "price 2 =",
            round(price_today * 1000) / 1000)

        if price_today > price_yesterday and sold_at is not None:
            # exit the trade
            gain = max(2 - price_today / sold_at, 0)
            print("Closing position. Price 1 =", round(price_yesterday *
                  1000) / 1000, "price 2 =", round(price_today * 1000) / 1000,
                  "gain =", round(gain * 1000) / 1000)
            total_gain *= gain
            total_trades += 1
            sold_at = None

        if not is_sublist_descending(prices, i - red_days_required,
                                     red_days_required):
            print("Continuing.")
            continue

        if sold_at is None:
            print("Selling at", round(price_today * 1000) / 1000)
            sold_at = price_today

    print("total gain =", total_gain, "total trades =", total_trades)


def main():
    simulate(year_start=2011, year_end=2020, red_days_required=3)


main()
