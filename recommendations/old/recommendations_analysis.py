
"""
Zatím nebudu řešit, jak porovnávat strategii indexu vs strategii doporučení.
Momentálně se jenom snažím zjistit průměrný zisk při použití doporučení.
Tzn. pokud splním podmínku (10 bodů), tak se podívám, jak se cena vyvinula
za 3 roky.

Update:
Ok, teď už musím vymyslet způsob, jak porovnat index vs doporučení.

Průměrný roční zisk z doporučení: u každého patternu se podívám, jak se
změnila cena po 3 letech, a zprůměruji na 1 rok (odmocninou). Z některé firmy
proto budu mít 4 hodnoty, z některé 0. Všechny tyto hodnoty zprůměruji (
normálním dělením) a tím získám průměrný roční výnos při použití doporučení.

Průměrný roční zisk z indexu: u každé firmy se podívám na změnu ceny mezi
začátkem 2012 a 2020, změnu zprůměruji na 1 rok (odmocninou). Z každé firmy
takto získám právě 1 hodnotu. Všechny hodnoty zprůměruji (dělením) a tím cca
získám průměrný roční výnos indexu.
"""

# S&P 500 měl v letech 2012 - 2020 průměrný roční výnos (včetně dividend) 14,1%
# Můj spočítaný průměrný roční výnos je 16,1% - to dává smysl, protože jsem
# nebral všech 500 firem, ale jen 337, a je zde přítomný survivorship bias,
# protože jsem bral firmy, které jsou v S&P 500 v roce 2020, nikoliv firmy,
# které tam byly v roce 2012


def get_symbols():
    symbols_file = open("s&p500_filtered.txt", "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


def get_recommendations(symbol):
    recommendations = []

    symbols_file = open("recommendations/" + symbol + ".csv", "r")
    symbols_file.readline()
    lines = symbols_file.readlines()
    symbols_file.close()

    for line in lines:
        date, rec = line.rstrip('\n').split(',')

        # Only append recommendations up to september 2017
        year = int(date[0] + date[1] + date[2] + date[3])
        month = int(date[5] + date[6])
        if year > 2017 or (year == 2017 and month > 9):
            break

        recommendations.append((date, rec))

    for rec in recommendations:
        print(rec[0], rec[1])

    return recommendations


def translate_rec_to_points(rec):
    rec = rec.lower()
    if rec == "buy" or rec == "long-term buy" or rec == "strong buy" or rec \
            == "top pick":
        return 2
    if rec == "overweight" or rec == "outperform" or rec == "positive" or \
            rec == "sector outperform" or rec == "market outperform" or rec \
            == "accumulate" or rec == "outperformer" or rec == "add" or rec \
            == "above average":
        return 1
    if rec == "perform" or rec == "sector perform" or rec == "neutral" or \
            rec == "hold" or rec == "equal-weight" or rec == "in-line" or \
            rec == "" or rec == "market perform" or rec == "equal-weight" or \
            rec == "sector weight" or rec == "speculative buy" or rec == \
            "conviction buy" or rec == "mixed" or rec == "peer perform" or \
            rec == "fair value" or rec == "market weight" or rec == "average":
        return 0
    if rec == "underweight" or rec == "underperform" or rec == "negative" or \
            rec == "reduce" or rec == "market underperform" or rec == \
            "cautious" or rec == "sector underperform" or rec == \
            "underperformer" or rec == "below average":
        return -1
    if rec == "sell":
        return -2
    print("Cannot translate unknown recommendation!", rec)
    exit(1)


def follows_pattern(recommendations, start, end, pattern_strength):
    points = 0
    for i in range(start, end + 1):
        rec = recommendations[i][1]
        points += translate_rec_to_points(rec)
    return points >= pattern_strength


def get_dates_of_patterns(recommendations, pattern_length=7,
                          pattern_strength=10):
    # Finds all recommendation patterns (but doesn't use the same
    # recommendation in multiple patterns) and returns the (newest) date of
    # each pattern in an array
    dates = []
    i = pattern_length - 1
    while i < len(recommendations):     # can't use for loop because python
        date, rec = recommendations[i]
        if follows_pattern(recommendations, i - pattern_length + 1, i,
                           pattern_strength):
            dates.append(date)
            i += pattern_length - 1
        i += 1
    return dates


def get_average_yearly_firm_return(symbol):
    symbols_file = open("prices/" + symbol + ".csv", "r")
    symbols_file.readline()
    lines = symbols_file.readlines()
    symbols_file.close()

    price_2012 = None
    price_2020 = None
    for line in lines:
        date, price = line.rstrip('\n').split(',')
        year = int(date[0] + date[1] + date[2] + date[3])
        month = int(date[5] + date[6])

        if price_2012 is None and year == 2012 and month == 1:
            price_2012 = float(price)

        if price_2020 is None and year == 2020 and month == 1:
            price_2020 = float(price)

    if price_2012 is None or price_2020 is None:
        # print(symbol, "doesn't have price records in the required period!")
        return None
    average_yearly_return = (price_2020 / price_2012) ** (1 / 8)
    # print("price_2012 =", price_2012)
    # print("price_2020 =", price_2020)
    # print("average_yearly_return =", average_yearly_return)
    return average_yearly_return


def get_average_yearly_index_return(symbols):
    # For each firm, calculates the average yearly return. Then return the
    # average of these averages.
    total_average_firm_returns = 0
    samples = 0
    for symbol in symbols:
        average_yearly_return = get_average_yearly_firm_return(symbol)
        if average_yearly_return is None:
            continue

        total_average_firm_returns += average_yearly_return
        samples += 1

    average_yearly_index_return = total_average_firm_returns / samples
    print("average_yearly_index_return =", average_yearly_index_return)
    return average_yearly_index_return


def get_average_yearly_return_after_n_years(symbol, date_old, n):
    symbols_file = open("prices/" + symbol + ".csv", "r")
    symbols_file.readline()
    lines = symbols_file.readlines()
    symbols_file.close()

    year_old = int(date_old[0] + date_old[1] + date_old[2] + date_old[3])
    month_old = int(date_old[5] + date_old[6])
    day_old = int(date_old[8] + date_old[9])

    price_old = None
    price_new = None
    for line in lines:
        date, price = line.rstrip('\n').split(',')
        year = int(date[0] + date[1] + date[2] + date[3])
        month = int(date[5] + date[6])
        day = int(date[8] + date[9])

        if price_old is None and year == year_old and month == month_old and \
                abs(day_old - day) < 6:
            price_old = float(price)

        if price_new is None and year == year_old + n and month == month_old \
                and abs(day_old - day) < 6:
            price_new = float(price)

    if price_old is None or price_new is None:
        return None
    average_yearly_return = (price_new / price_old) ** (1 / n)
    print(date_old, price_old, "->", price_new,
          str(round((average_yearly_return - 1) * 10000) / 100) + "%")
    return average_yearly_return


def get_average_yearly_return_on_recommendations(symbols):
    total_ayr = 0     # total average yearly return after 3 years
    samples = 0
    for symbol in symbols:
        print(symbol)
        recommendations = get_recommendations(symbol)
        pattern_dates = \
            get_dates_of_patterns(recommendations, pattern_strength=9)
        for date in pattern_dates:
            ayr = get_average_yearly_return_after_n_years(symbol, date, 1)
            if ayr is None:
                continue
            total_ayr += ayr
            samples += 1
    average_yearly_recommendation_return = total_ayr / samples
    print("average_yearly_recommendation_return =",
          average_yearly_recommendation_return, "samples size =", samples)
    return average_yearly_recommendation_return


def main():
    symbols = get_symbols()
    symbols = ["MSFT"]

    ayror = get_average_yearly_return_on_recommendations(symbols)
    # ayir = get_average_yearly_index_return(symbols)


main()
