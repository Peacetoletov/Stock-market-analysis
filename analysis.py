import math
from decimal import *


class Hypothesis:
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
        self.test = "hello"
        self.period = period
        self.lower_change_limit = lower_change_limit
        self.upper_change_limit = upper_change_limit


class Record:
    def __init__(self, year, month, day, price):
        self.year = year
        self.month = month
        self.day = day
        self.price = price  # closing price


def read_data(symbol):
    # returns lines
    file = open("company_data_filtered/" + symbol + ".csv", "r")
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
        price = float(line.split(',')[4])
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
    symbols_file = open("symbols.txt", "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


def test_hypothesis(hypothesis: Hypothesis):
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
        for i in range(4):      # for each quarter
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
                if hypothesis.lower_change_limit < change < \
                        hypothesis.upper_change_limit:
                    streak += 1
                else:
                    streak = 0

                if streak >= hypothesis.period:
                    if j != len(price_in_years) - 1 and \
                            price_in_years[j + 1] is not None:
                        next_change = price_in_years[j + 1] / price_in_years[j]

                        price_change_next_year.append(next_change)

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

    getcontext().prec = 100
    total_change = Decimal(1)
    i = 0
    for change in price_change_next_year:
        i += 1
        if i % 10000 == 0:
            print(i, "/", sample_size, "(calculating average)")
        total_change *= Decimal(change)
    average = total_change ** (1 / Decimal(sample_size))

    print("Average price change =", str(float(average)) + ". Median =",
          float(median))
    print("The scenario in this hypothesis happened",
          sample_size, "times in history.")


def main():
    # Found a way to simply reproduce a bug.
    # Symbols = ["MSFT"]
    # hypothesis = Hypothesis(1, -math.inf, math.inf)
    # hypothesis = Hypothesis(1, 1, math.inf)
    # hypothesis = Hypothesis(1, -math.inf, 1)
    # the ones with bounds have way too many occurrences

    hypothesis = Hypothesis(10, 0.9, math.inf)
    test_hypothesis(hypothesis)


main()
