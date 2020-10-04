
# TODO: zjistit, zda by se dalo nějak využít 3x leverage pomocí
#  rebalancingu, tzn. když se daří, budu si brát výdělky, a když se nedaří,
#  tak budu dotovat, abych při zpětném vyhoupnutí měl obrovské zisky


def get_prices_in_year(symbol, year_start=None, year_end=None):
    # returns a list of tuples (price, year)
    symbols_file = open("prices/" + symbol + ".csv", "r")
    symbols_file.readline()
    lines = symbols_file.readlines()
    symbols_file.close()

    prices_in_year = []
    for line in lines:
        year = int(line[0] + line[1] + line[2] + line[3])
        if (year_start is not None and year < year_start) or \
                (year_end is not None and year > year_end):
            continue
        price = float(line.rstrip('\n').split(',')[1])
        prices_in_year.append((price, year))
    return prices_in_year


def simulate_yearly_return(symbol, leverage=2, year_start=None, year_end=None):
    prices_in_year = get_prices_in_year(symbol, year_start, year_end)

    last_year = prices_in_year[0][1]
    total_benchmark_change = 1
    yearly_benchmark_change = 1
    total_leverage_change = 1
    yearly_leverage_change = 1
    annual_leverage_fee = 0.99      # 1% fee
    for i in range(1, len(prices_in_year)):
        prev_price, _ = prices_in_year[i - 1]
        price, year = prices_in_year[i]
        if year > last_year or i == len(prices_in_year) - 1:
            total_leverage_change *= annual_leverage_fee
            yearly_leverage_change *= annual_leverage_fee
            print(last_year if year > last_year else year, "normal:",
                  yearly_benchmark_change, "leveraged:",
                  yearly_leverage_change)
            print("Total. normal:", total_benchmark_change, "leveraged:",
                  total_leverage_change)
            print()
            last_year = year
            yearly_benchmark_change = 1
            yearly_leverage_change = 1

        price_change = price / prev_price
        leveraged_price_change = (prev_price + leverage *
                                  (price - prev_price)) / prev_price
        # print("Real:", (price_change - 1) * 100, "Leveraged:",
        #      (leveraged_price_change - 1) * 100)

        total_benchmark_change *= price_change
        yearly_benchmark_change *= price_change
        total_leverage_change *= leveraged_price_change
        yearly_leverage_change *= leveraged_price_change


def main():
    simulate_yearly_return("SPY", leverage=2)


main()
