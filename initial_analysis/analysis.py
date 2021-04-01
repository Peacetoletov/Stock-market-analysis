import math
from decimal import *

# TODO - momentálně mám podmínky takové, že "alespoň 3 roky x", což může být
#  ale zkreslené kvůli takovým společnostem, které danou podmínku splňují
#  třeba 7 let. Užitečnější by bylo, kdybych to změnil na "právě 3 roky x"

# TODO - zkusit počítat průměr jiným způsobem (změna 0.5 a 1.5 bude v
#  průměru 1) to z toho sůvodu, že se nejedná o změnu jedné akcie v sérii,
#  ale dvě akcie v paralele - strategie přece je, že koupím a po roce prodán.


class Conditions:
    """
    Period - the number of years for which the conditions must hold
    Lower change limit - how much at least the price must change from year
        to year for the condition to hold
    Upper change limit - how much at most the price must change from year
        to year for the condition to hold

    If a limit is math.inf (or -math.inf), there is no bound to the price
    change from that side.

    Lower change limit must be a smaller number than upper change limit.

    Example 1:
    Period = 3, lower_change_limit = 1.05, upper_change_limit = math.inf.
    For 3 consecutive years, the price must increase at least by 5 %
    compared to last year.

    Example 2:
    Period = 1, lower_change_limit = 0.8, upper_change_limit = 0.95
    The price must drop by 5-20 % compared to last year.

    Example 3:
    Period = 5, lower_change_limit = 0,95, upper_change_limit = 1,5.
    For 5 consecutive years, the price mustn't decrease by more than 5 % or
    increase by more than 50 %.

    Example 4:
    Period = 1, lower_change_limit = -math.inf, upper_change_limit = math.inf
    No bounds. As if a monkey were picking stocks.
    """
    def __init__(self, period, lower_change_limit, upper_change_limit):
        self.period = period
        self.lower_change_limit = lower_change_limit
        self.upper_change_limit = upper_change_limit


class Record:
    def __init__(self, year, month, day, price):
        self.year = year
        self.month = month
        self.day = day
        self.price = price


def read_data(symbol):
    # returns lines
    file = open("company_data/" + symbol + ".csv", "r")
    file.readline()     # discard the first line
    lines = file.readlines()
    file.close()
    return lines


def group_records_by_years(symbol):
    # returns a 2D array
    data = read_data(symbol)
    records_by_years = []      # contains arrays of records with the same year
    for line in data:
        year = int(line[0] + line[1] + line[2] + line[3])
        month = int(line[5] + line[6])
        day = int(line[8] + line[9])
        price = float(line.split(',')[4])   # closing price
        record = Record(year, month, day, price)

        # Error catching
        if len(records_by_years) != 0:
            last_recorded_year = records_by_years[-1][0].year
            if year < last_recorded_year:
                print("A weird sequence of years occurred for symbol",
                      symbol, "year", year)

        # Append a new empty array to records_by_years if the current
        # year is new
        if len(records_by_years) == 0:
            records_by_years.append([])
        else:
            last_recorded_year = records_by_years[-1][0].year

            while year != last_recorded_year:
                records_by_years.append([])
                last_recorded_year += 1
            
        # Append the current record to the newest year array
        records_by_years[-1].append(record)

    return records_by_years


def get_symbols():
    symbols_file = open("symbols/s&p500.txt", "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


def get_average(price_change_next_year):
    # OLD WAY
    """
    sample_size = len(price_change_next_year)
    getcontext().prec = 100
    total_change = Decimal(1)
    i = 0
    for change in price_change_next_year:
        i += 1
        if i % 10000==0:
            print(i, "/", sample_size, "(calculating average)")
        total_change *= Decimal(change)
    average = total_change ** (1 / Decimal(sample_size))
    return average
    """

    # new way
    sample_size_total = len(price_change_next_year)
    # getcontext().prec = 100
    total_change = 0

    # Some values may be too high because of scuffed data. I can get around
    # this by ignoring the highest and lowest x %

    bound_low = sample_size_total // 10
    bound_high = sample_size_total - sample_size_total // 10
    # bound_low = 0
    # bound_high = sample_size_total
    sample_size_adjusted = bound_high - bound_low
    for i in range(bound_low, bound_high):
        # print("change =", change)
        total_change += price_change_next_year[i]
    average = total_change / sample_size_adjusted
    print("Adjusted sample size =", sample_size_adjusted)
    return average


def test_hypothesis(conditions: Conditions, years_to_hold=1):
    # tests the hypothesis on the data and prints result
    symbols = get_symbols()

    # symbols = ["0A3.FAtest_purpose_only", "MSFT", "AAPL"] # only a test
    # symbols = ["MSFT"]

    # Supposing the conditions are met and I buy a stock, the price will
    # change next year. This array contains all such changes on historical
    # data, therefore the average or median can be compared to other
    # hypothesises.
    price_change_next_year = []

    time = 0
    for symbol in symbols:
        time += 1
        if time % 100 == 0:
            print(time)
        records_by_years = group_records_by_years(symbol)
        # for each quarter - essentially using each year 4 times to increase
        # sample size and decrease the impact of short term volatility
        for i in range(4):
            years_series = []
            for year in records_by_years:
                # If no data is available in a given year, append None
                if len(year) == 0:
                    years_series.append(None)
                    continue
                # If this quarter is unavailable in this year, use the
                # latest available quarter
                if i >= len(year):
                    years_series.append(year[-1])
                else:
                    # the wanted quarter is available => append it
                    years_series.append(year[i])

            streak = 0
            for j in range(1, len(years_series)):
                if years_series[j] is None or years_series[j - 1] is None:
                    streak = 0
                    continue

                change = years_series[j].price / years_series[j - 1].price
                if conditions.lower_change_limit < change < \
                        conditions.upper_change_limit:
                    streak += 1
                else:
                    streak = 0

                # idk if this should be here but I want to avoid penny stocks
                if years_series[j].price < 1:
                    streak = 0
                    break

                if streak >= conditions.period:
                    """
                    if j != len(years_series) - 1 and \
                            years_series[j + 1] is not None:
                        next_change = \
                            years_series[j + 1].price / years_series[j].price
                        price_change_next_year.append(next_change)

                        print(symbol, years_series[j].year,
                            str(round(next_change * 10000) / 100) + "%")
                    """

                    if j < len(years_series) - years_to_hold and \
                            years_series[j + years_to_hold] is not None:
                        next_change = years_series[j + years_to_hold].price / years_series[j].price
                        price_change_next_year.append(next_change)

                        print(symbol, years_series[j].year,
                            str(round(next_change * 10000) / 100) + "%")


    print("Data collected!")

    sample_size = len(price_change_next_year)

    if sample_size == 0:
        print("The scenario in this hypothesis has never happened.")
        return

    # print out average and median
    price_change_next_year.sort()
    median = price_change_next_year[sample_size // 2]

    counter = 0
    for test in price_change_next_year:
        if test == 1:
            counter += 1
    print("cases of zero change:", counter)

    average = get_average(price_change_next_year)

    print("Average price change =", str(float(average)) + ". Median =",
          float(median))
    # print("Total of", unique_symbols, "companies contributed to the "
    #                                  "statistics.")
    # this last line doesn't take into account that 10 % best and worst
    # aren't counted


def print_companies_currently_meeting_conditions(conditions: Conditions):
    symbols = get_symbols()
    for symbol in symbols:
        was_already_printed = False
        records_by_years = group_records_by_years(symbol)
        for i in range(4):
            price_in_years = []
            for year in records_by_years:
                # If no data is available in a given year, append None
                if len(year) == 0:
                    price_in_years.append(None)
                    continue
                # If this quarter is unavailable in this year, use the
                # latest available quarter
                if i >= len(year):
                    price_in_years.append(year[-1].price)
                else:
                    # the wanted quarter is available => append it
                    price_in_years.append(year[i].price)

            streak = 0
            for j in range(1, len(price_in_years)):
                if price_in_years[j] is None or price_in_years[j - 1] is \
                        None or price_in_years[j - 1] == 0:
                    streak = 0
                    continue

                change = price_in_years[j] / price_in_years[j - 1]
                if conditions.lower_change_limit < change < \
                        conditions.upper_change_limit:
                    streak += 1
                else:
                    streak = 0

                if streak >= conditions.period and not was_already_printed:
                    if records_by_years[j][0].year == 2020: # current year
                        print(symbol)
                        was_already_printed = True


def main():
    # Found a way to simply reproduce a bug.
    # Symbols = ["MSFT"]
    # hypothesis = Hypothesis(1, -math.inf, math.inf)
    # hypothesis = Hypothesis(1, 1, math.inf)
    # hypothesis = Hypothesis(1, -math.inf, 1)
    # the ones with bounds have way too many occurrences

    conditions = Conditions(3, -math.inf, 0.95)
    test_hypothesis(conditions, years_to_hold=3)

    # print_companies_currently_meeting_conditions(conditions)


main()
