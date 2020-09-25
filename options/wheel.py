"""
Parametry, které chci využít při simulaci:
- 7 dnů do expirace
- 330.65 aktuální cena akcie (SPY)
- 330 strike putu
- 3.26 cena putu
- 331 strike callu
- 4.24 cena callu
"""

"""
Poznatky:
ATM wheel má větší EV než OTM wheel.
Velice mírně ITM wheel má zanedbatelně větší EV než ATM wheel.
Více ITM wheel má menší EV než ATM wheel.
=> optimální wheel je ATM

Vysoce volatilní akcie (TSLA, NKLA) nejsou vhodné pro wheel, přestože nabízí 
vysoký premium.
=> vyhýbat se high volatility akciím

Samotné covered cally nebo naked puty mají podstatně nižší EV než buy and 
hold a mírně nižší EV než wheel. Wheel má ale pořád podstatně nižší EV než 
buy and hold.
"""

# TODO: otestovat následující strategii: 1týdenní candle. Jakmile 2 po sobě
#  budou zelené, prodávám ATM cash secured put. Pokud je následující týden
#  zelený, opakuji postup. Pokud je následující týden červený (tzn. musím
#  koupit 100 akcií) (ve skutečnosti budu prodávat malinko OTM put,
#  takže se musím dívat na to, jestli jsem dostal akcie, ne na to, zda je
#  týden červený. Pro jednoduchost ale tento stav beru shodný s červeným
#  týdnem), potom si akcie nějakou dobu nechávám. V moment, kdy jsou 2 týdny
#  po sobě zelené, prodávám své akcie a celý postup opakuji (začnu prodáním
#  putu...).

import yfinance as yf


def get_prices(symbol=None, year_start=None, year_end=None):
    if symbol is None:
        symbols_file = open("wheel_prices/spy.csv", "r")
    else:
        symbols_file = open("wheel_prices/" + symbol + ".csv", "r")
    symbols_file.readline()
    lines = symbols_file.readlines()
    symbols_file.close()

    prices = []
    for line in lines:
        year = int(line[0] + line[1] + line[2] + line[3])
        if (year_start is not None and year < year_start) or \
                (year_end is not None and year > year_end):
            continue
        prices.append(float(line.rstrip('\n').split(',')[2]))
    return prices


def sell_call(cur_price, next_price, strike, premium, capital):
    """
    cur_price - cena akcie v moment, kdy prodávám put
    next_price - cena akcie v moment expirace putu
    strike - strike vyjádřen jako procentuální část z cur_price
    premium - premium vyjádřeno jako procentuální část z cur_price
    capital - hodnota kapitálu (pro jednoduchost předpokládám, že můžu v
        každý moment investovat 100 % kapitálu)
    """
    print("Selling call")
    # shares kept
    if next_price < cur_price * strike:
        new_capital = capital + premium * cur_price * 100
        print("Keeping shares. Cash gained:", round((premium * cur_price *
                                                     100) * 100) / 100,
              "New capital =", round(new_capital * 100) / 100)
        return new_capital, True

    # shares sold
    new_capital = capital + 100 * cur_price * (strike + premium)
    print("Selling shares. New capital =", round(new_capital * 100) / 100)
    return new_capital, False


def sell_put(cur_price, next_price, strike, premium, capital):
    """
    cur_price - cena akcie v moment, kdy prodávám put
    next_price - cena akcie v moment expirace putu
    strike - strike vyjádřen jako procentuální část z cur_price
    premium - premium vyjádřeno jako procentuální část z cur_price
    capital - hodnota kapitálu (pro jednoduchost předpokládám, že můžu v
        každý moment investovat 100 % kapitálu)
    """
    print("Selling put.")
    # not assigned
    if next_price > cur_price * strike:
        new_capital = capital + premium * cur_price * 100
        print("Keeping cash. Cash gained:", round((premium * cur_price *
                                                   100) * 100) / 100,
              "New capital =", round(new_capital * 100) / 100)
        return new_capital, False

    # assigned
    #print("Capital to start with:", capital)
    #print("Buying 100 shares for:", 100 * strike * cur_price)
    #print("Premium gained:", 100 * premium * cur_price)
    new_capital = capital - 100 * cur_price * (strike - premium)
    print("Buying shares. New capital =", round(new_capital * 100) / 100)
    return new_capital, True


def simulate_wheel(symbol=None):
    prices = get_prices(symbol)
    """
    call_strike = 331 / reference_price
    put_strike = 330 / reference_price
    call_premium = 4.24 / reference_price     
    put_premium = 3.26 / reference_price
    
    # call premium cca 3.1 při průměrné IV, put premium 2.13
    """
    """
    call_strike = 331 / reference_price
    put_strike = 330 / reference_price
    call_premium = 3.1 / reference_price
    put_premium = 2.13 / reference_price
    """
    reference_price = 326.97
    put_strike = 326 / reference_price
    put_premium = 3.66 / reference_price
    call_strike = 327 / reference_price
    call_premium = 4.52 / reference_price

    capital = prices[0] * 100
    holding_shares = False
    print("Starting capital =", capital)
    for i in range(len(prices) - 1):
        cur_price = prices[i]
        next_price = prices[i + 1]
        print("Current price =", cur_price, ". Next price =", next_price)
        if holding_shares:
            capital, holding_shares = sell_call(cur_price, next_price, call_strike, call_premium, capital)
        else:
            capital, holding_shares = sell_put(cur_price, next_price, put_strike, put_premium, capital)

    if holding_shares:
        capital += 100 * prices[-1]
        holding_shares = False

    alternative_capital = 100 * prices[-1]

    print("Final capital:", capital, ". Capital if I bought and held:",
          alternative_capital)


def simulate_covered_calls(symbol=None):
    prices = get_prices(symbol, 2000, 2011)

    reference_price = 270.01
    call_strike = 270 / reference_price
    call_premium = 2.1 / reference_price

    capital = 0
    holding_shares = True
    print("Starting share value =", 100 * prices[0])
    for i in range(len(prices) - 1):
        cur_price = prices[i]
        next_price = prices[i + 1]
        print("Current price =", cur_price, ". Next price =", next_price)
        capital, holding_shares = sell_call(cur_price, next_price, call_strike,
                                            call_premium, capital)
        if not holding_shares:
            capital -= 100 * next_price
            holding_shares = True
            print("Need to buy shares back. New capital:", capital)

    alternative_capital = 100 * prices[-1]

    print("Final capital:", capital, ". Capital if I bought and held:",
          alternative_capital)


def simulate_naked_puts(symbol=None):
    prices = get_prices(symbol, 2000, 2011)

    """
    put_strike = 330 / reference_price 
    put_premium = 3.26 / reference_price
    """

    reference_price = 270.01
    put_strike = 270 / reference_price
    put_premium = 2.35 / reference_price

    capital = 100 * prices[0]
    holding_shares = False
    print("Starting capital =", capital)
    for i in range(len(prices) - 1):
        cur_price = prices[i]
        next_price = prices[i + 1]
        print("Current price =", cur_price, ". Next price =", next_price)
        capital, holding_shares = sell_put(cur_price, next_price, put_strike,
                                           put_premium, capital)
        if holding_shares:
            capital += 100 * next_price
            holding_shares = False
            print("Need to sell shares. New capital:", capital)

    alternative_capital = 100 * prices[-1]

    print("Final capital:", capital, ". Capital if I bought and held:",
          alternative_capital)


def simulate_custom_strategy(symbol=None):
    prices = get_prices(symbol)
    if len(prices) < 3:
        print("Price list too small!")
        return
    """
    # SPY
    reference_price = 330.65
    put_strike = 330 / reference_price
    put_premium = 2.13 / reference_price
    """

    """
    # 28. 6. 2018 https://www.youtube.com/watch?v=IaacSxpN-Ik
    reference_price = 270.01
    put_strike = 270 / reference_price
    put_premium = 2.35 / reference_price
    """
    reference_price = 326.97
    put_strike = 326 / reference_price
    put_premium = 3.66 / reference_price

    capital = 0
    holding_shares = True
    print("Starting shares value =", round((100 * prices[0]) * 100) / 100)
    for i in range(2, len(prices) - 1):
        prev_prev_price = prices[i - 2]
        prev_price = prices[i - 1]
        cur_price = prices[i]
        next_price = prices[i + 1]
        print("Current price =", round(cur_price * 100) / 100,
              ". Next price =", round(next_price * 100) / 100)
        if prev_prev_price * put_strike < prev_price and \
                prev_price * put_strike < cur_price:
            print("Price increased 2 weeks in a row.")
            if holding_shares:
                capital += 100 * cur_price
                print("Selling shares. New capital:",
                      round(capital * 100) / 100)
            capital, holding_shares = sell_put(cur_price, next_price,
                put_strike, put_premium, capital)
        else:
            print("Price did not increase 2 weeks in a row. Keeping shares.")

    if holding_shares:
        capital += 100 * prices[-1]
        holding_shares = False
        print("Need to sell shares. New capital:", capital)

    alternative_capital = 100 * prices[-1]

    print("Final capital:", capital, ". Capital if I bought and held:",
          alternative_capital)


def main():
    simulate_wheel()
    #simulate_covered_calls("APA")
    #simulate_naked_puts("APA")
    #simulate_custom_strategy()


main()
