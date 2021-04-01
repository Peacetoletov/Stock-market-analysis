

def rebalance(in_etf, in_cash, etf_percentage):
    total = in_etf + in_cash
    in_etf = total * etf_percentage
    in_cash = total * (1 - etf_percentage)
    return in_etf, in_cash


def simulate_rebalancing(symbol, leverage=2, etf_percentage=0.5,
                         year_start=None, year_end=None):
    # etf_percentage is the fraction of portfolio invested in the etf,
    # the rest of portfolio is held in cash
    prices_in_year = get_prices_in_year(symbol, year_start, year_end)

    last_year = prices_in_year[0][1]

    total_benchmark_change = 1
    yearly_benchmark_change = 1

    in_etf = etf_percentage
    in_cash = 1 - etf_percentage
    total_leverage_change = 1
    yearly_leverage_change = 1

    # 1% fee
    annual_leverage_fee = 1 - 0.01 * etf_percentage if leverage != 1 else 1

    for i in range(1, len(prices_in_year)):
        prev_price, _ = prices_in_year[i - 1]
        price, year = prices_in_year[i]
        if year > last_year or i == len(prices_in_year) - 1:
            total_leverage_change *= annual_leverage_fee
            yearly_leverage_change *= annual_leverage_fee
            in_etf *= annual_leverage_fee
            in_cash *= annual_leverage_fee
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
        # print("Real:", (price_change - 1) * 100, "% | Leveraged:",
        #       (leveraged_price_change - 1) * 100, "%")

        total_benchmark_change *= price_change
        yearly_benchmark_change *= price_change

        old_value = in_etf + in_cash
        # print("Before. Etf:", in_etf, "Cash", in_cash)
        in_etf *= leveraged_price_change
        # print("New etf value:", in_etf)
        in_etf, in_cash = rebalance(in_etf, in_cash, etf_percentage)
        new_value = in_etf + in_cash
        value_change = new_value / old_value
        # print("After rebalancing. Etf", in_etf, "Cash", in_cash, "Value "
        #       "change:", value_change)
        # print()

        total_leverage_change *= value_change
        yearly_leverage_change *= value_change


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


def target_reached(cset, take_profit, stop_loss):
    if cset < take_profit:
        print("Taking profit!") #, cset)
        return True
    if cset > stop_loss:
        print("Stopping loss.", cset)
        return True
    return False


def simulate_shorting(symbol, leverage=-3, etf_percentage=0.5, stop_loss=2.0,
                      take_profit=0.5, year_start=None, year_end=None):
    prices_in_year = get_prices_in_year(symbol, year_start, year_end)
    last_year = prices_in_year[0][1]

    total_benchmark_change = 1
    yearly_benchmark_change = 1

    total_leverage_change = 1
    yearly_leverage_change = 1

    portfolio = 1

    # change since entering trade
    cset = 1

    annual_leverage_fee = 0.009  # 0.9% fee
    for i in range(1, len(prices_in_year)):
        prev_price, _ = prices_in_year[i - 1]
        price, year = prices_in_year[i]

        if year > last_year or i == len(prices_in_year) - 1:
            print("Benchmark:", total_benchmark_change)
            last_year = year
            yearly_benchmark_change = 1
            yearly_leverage_change = 1

        price_change = price / prev_price
        leveraged_price_change = \
            ((prev_price + leverage * (price - prev_price)) / prev_price) * \
            (1 - annual_leverage_fee / 252)

        # print("Real:", (price_change - 1) * 100, "Leveraged:",
        #       (leveraged_price_change - 1) * 100, "CSET:", cset)

        total_benchmark_change *= price_change
        yearly_benchmark_change *= price_change
        total_leverage_change *= leveraged_price_change
        yearly_leverage_change *= leveraged_price_change
        cset *= leveraged_price_change

        if target_reached(cset, take_profit, stop_loss):
            portfolio += portfolio * etf_percentage * (1 - cset)
            print(year, "Portfolio value:", portfolio, "price =", price)
            if portfolio <= 0:
                return
            cset = 1


def update_portfolio(change_in_years, breakeven, portfolio, commitment):
    leveraged_price_change = 1
    for yearly_change in change_in_years:
        leveraged_price_change *= yearly_change

    leap_value = max((leveraged_price_change - 1) / (breakeven - 1), 0)
    portfolio = portfolio * (1 - commitment * (1 - leap_value))

    print("new portfolio:", portfolio, "leap value:", leap_value, "\n")

    return portfolio


def simulate_leaps(symbol, breakeven, leverage=3, commitment=0.5,
                   yte=1, year_start=None, year_end=None):
    prices_in_year = get_prices_in_year(symbol, year_start, year_end)
    last_year = prices_in_year[0][1]

    total_benchmark_change = 1
    yearly_benchmark_change = 1

    total_leverage_change = 1
    yearly_leverage_change = 1
    annual_leverage_fee = 0.99 if leverage != 1 else 1  # 1% fee

    change_in_years = []    # for leaps longer than 1 year
    portfolio = 1

    for i in range(1, len(prices_in_year)):
        prev_price, _ = prices_in_year[i - 1]
        price, year = prices_in_year[i]
        if year > last_year or i == len(prices_in_year) - 1:
            total_leverage_change *= annual_leverage_fee
            yearly_leverage_change *= annual_leverage_fee

            change_in_years.append(yearly_leverage_change)

            print(last_year if year > last_year else year, "normal:",
                  yearly_benchmark_change, "leveraged:",
                  yearly_leverage_change)

            if len(change_in_years) == yte:
                portfolio = update_portfolio(change_in_years, breakeven,
                                             portfolio, commitment)
                change_in_years = []

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


class Portfolio:
    """
    value - the value of the portfolio in some currency
    regular_deposit - dollar cost averaging (a deposit each month)
    implicit_leverage - I approximate small cap value by taking S&P500 data
        and applying 1.25 daily implicit leverage to achieve higher
        volatility and higher expected returns.
    leverage - real leverage obtained by using margin
    interest - the annual interest of real leverage
    rebalance_point - if the portfolio value changes (up or down) by a
        percentage described by this variable , it will be rebalanced
        - if set to None, portfolio will be rebalanced daily.
    value_when_last_rebalanced - value of the portfolio when it was last
        rebalanced, used to compare later portfolio's value when deciding
        whether to rebalance yet
    """
    # TODO - make sure this is accurate (e.g. the daily rebalancing part)

    def __init__(self, value, regular_deposit, implicit_leverage, leverage,
                 interest, rebalance_point=None):
        self.value = value
        self.regular_deposit = regular_deposit
        self.implicit_leverage = implicit_leverage
        self.leverage = leverage
        self.interest = interest
        self.rebalance_point = rebalance_point
        self.value_when_last_rebalanced = value

    def deposit(self, amount=None):
        if amount is None:
            self.value += self.regular_deposit
        else:
            self.value += amount
        print("Deposited money! New portfolio value: {:.2f}".format(
              self.value))

    def update_value(self, change):
        borrowed = self.get_borrowed_amount()
        # print("borrowed: {:.2f}".format(borrowed))
        exposure = self.value + borrowed
        self.value = exposure * change - borrowed
        if self.value < 0:
            raise Exception("Guh! Portfolio value negative.")

        print("New value: {:.2f}".format(self.value),
              "index change: {:.2f}%".format((change - 1) * 100))

        if self.needs_rebalancing():
            self.rebalance()

    def get_borrowed_amount(self):
        return self.value_when_last_rebalanced * (self.leverage - 1)

    def needs_rebalancing(self):
        vwlr = self.value_when_last_rebalanced
        return self.value < vwlr * (1 - self.rebalance_point) or \
            self.value > vwlr * (1 + self.rebalance_point)

    def rebalance(self):
        self.value_when_last_rebalanced = self.value
        print("Rebalancing.")

    def deduct_interest(self):
        self.value -= self.value_when_last_rebalanced * \
                      (self.interest * (self.leverage - 1))
        print("Interest deducted. New value: {:.2f}".format(self.value))


def get_return_in_year(prices_in_year, start_index, portfolio: Portfolio):
    # Odsimuluje výkonnost portfolia v jednom roce. Podporuje dollar cost
    # averaging.
    #
    # prices_in_year - array of tuples (daily_price, year)
    # start_index - index where the first tuple with the desired year starts
    # portfolio - object with portfolio characteristics

    cur_year = prices_in_year[start_index][1]
    i = 0

    while start_index + i + 1 < len(prices_in_year):
        i += 1
        prev_price, _ = prices_in_year[start_index + i - 1]
        price, year = prices_in_year[start_index + i]

        # To simulate monthly dollar cost averaging, I will increase the
        # portfolio value every 20 trading days.
        if i % 20 == 0:
            portfolio.deposit()

        # Daily simulated implicitly leveraged index (ili) change
        change = price / prev_price
        ili_change = (change - 1) * portfolio.implicit_leverage + 1

        print(i, end=":   ")

        # print("Day:", i, "Change = {:.2f}%".format((change - 1) * 100),
        #       "ili change = {:.2f}%".format(
        #           (ili_change - 1) * 100))

        # Update the portfolio, applying actual leverage
        portfolio.update_value(ili_change)

        # Break when the year is over
        if year > cur_year:
            break

    # At the end of the year, apply leverage costs
    portfolio.deduct_interest()


def year_start_indices(prices_in_year):
    # Yields the first index of each year in prices_in_year

    cur_year = prices_in_year[0][1]
    yield 0

    for i in range(len(prices_in_year)):
        year = prices_in_year[i][1]
        if year > cur_year:
            yield i
            cur_year = year


def simulate_scv_margin(symbol="^GSPC", leverage=1.5, year_start=None,
                        year_end=None):
    # Tato funkce simuluje, co by se stalo, kdybych nepoužíval leveraged
    # etfka, ale místo toho si leverage řídil sám pomocí marginu. Zároveň
    # chci simulovat small cap value, ale protože nemám scv data (mám jen
    # spy), tak to aproximuji pomocí zvýšený bety spy (tj. budu mít nějaký
    # implicitní denní leverage, např. 1.25).
    # Rebalancovat leverage každý den by jednak bylo nákladné (poplatky za
    # trade, bid/ask spready apod.), navíc bych měl stejný problém, jako
    # leveraged etfka, tj. volatility drag. Abych předešel oběma problémům,
    # budu rebalancovat až v moment, kdy se cena dostane nad/pod určitou
    # hranici od ceny v moment posledního rebalancingu.
    # V základu budu uvažovat 50% leverage (tj. 150% exposure) a rebalancing
    # budu provádět při 20% růstu nebo poklesu. Očekávám, že toto vyústí v
    # rebalancing 2x-3x za průměrný rok.

    portfolio = Portfolio(
        value=1,                  # initial lump sum deposit
        # regular_deposit=20,         # monthly deposit
        regular_deposit=1,  # monthly deposit
        implicit_leverage=1.25,
        leverage=1.5,
        interest=0.015,            # 1.5% annual leverage interest
        # interest=0.0,  # 1.5% annual leverage interest
        rebalance_point=0.20        # rebalance after a 20% move in either
                                    # direction
    )

    prices_in_year = get_prices_in_year(symbol, year_start, year_end)

    # get_return_in_year(prices_in_year, 0, portfolio)    # remove

    for index in year_start_indices(prices_in_year):
        get_return_in_year(prices_in_year, index, portfolio)

    # TODO - nějakým způsobem implementovat dividendy... možná tak, že si z
    #  https://www.multpl.com/s-p-500-dividend-yield/table/by-year vezmu
    #  roční dividendu, podělím 4 a tuto hodnotu přidám každý 55. den?
    #  (abych do roka (cca 250 dní) vyplatil dividendy 4x)

    # TODO - compare with daily rebalancing




def main():
    # simulate_yearly_return("^GSPC")
    simulate_scv_margin()


main()
