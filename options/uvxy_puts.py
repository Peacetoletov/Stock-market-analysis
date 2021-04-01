"""
Simulate monthly atm puts on uvxy.
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
        prices.append(float(line.rstrip('\n').split(',')[1]))
    return prices


def get_put_value(put_relative_price, prev_price, cur_price):
    # returns a number greater than or equal to 0

    put_price = prev_price * put_relative_price
    breakeven_price = prev_price - put_price
    excess_value = breakeven_price - cur_price
    put_value = max(excess_value / put_price + 1, 0)

    print("\nPrice 1 =", prev_price, "Price 2 =", cur_price)
    print("Breakeven price =", round(breakeven_price * 1000) / 1000,
          "Put value =", put_value)

    return put_value


def simulate(put_relative_price=0.14, year_start=None, year_end=None):
    prices = get_prices("prices/monthly/UVXY.csv",year_start, year_end)

    for i in range(1, len(prices)):
        prev_price = prices[i - 1]
        cur_price = prices[i]

        put_return = get_put_value(put_relative_price, prev_price, cur_price)


def main():
    simulate()


main()
