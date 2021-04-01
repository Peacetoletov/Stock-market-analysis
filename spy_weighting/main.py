"""
Myšlenka - nasimuluji portfolio, které se bude skládat ze stejných firem
jako SPY. Rozdíl bude v tom, že nebudu mít market cap weight, ale weight
budu mít podle toho, jak se změnila cena dané akcie za poslední rok. Zkusím
dvě varianty - v jedné budu dávat největší váhu akciím, které nejvíce
vzrostly - momentum strategy. Druhá varianta bude naopak dávat největší váhu
akciím, které nejvíce klesly - value strategy.
"""


import math
from typing import List, Optional


def get_symbols():
    symbols_file = open("s&p500.txt", "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


def get_oldest_year(symbols):
    oldest_year = math.inf
    for symbol in symbols:
        price_file = open("yearly_prices/" + symbol + ".csv", "r")
        price_file.readline()
        first_line = price_file.readline()
        price_file.close()

        year = int(first_line.split('-')[0])
        if year < oldest_year:
            oldest_year = year
            # print("oldest year:", symbol)

    return oldest_year


def get_prices_in_years():
    symbols = get_symbols()
    oldest_year = get_oldest_year(symbols)
    prices_in_years: List[List[Optional[float]]] = []

    for year in range(oldest_year, 2021 + 1):
        prices_in_years.append([None] * len(symbols))

    for i in range(len(symbols)):
        price_file = open("yearly_prices/" + symbols[i] + ".csv", "r")
        price_file.readline()
        lines = price_file.readlines()
        price_file.close()

        for line in lines:
            price = float(line.rstrip('\n').split(',')[1])
            year = int(line.split('-')[0])
            index = year - oldest_year
            prices_in_years[index][i] = price

    return prices_in_years


def test_prices_in_years():
    symbols = get_symbols()
    oldest_year = get_oldest_year(symbols)
    prices_in_years = get_prices_in_years()

    for i in range(len(symbols)):
        price = prices_in_years[0][i]
        print(symbols[i], "in", str(oldest_year) + ":", price)

    # yep, works as expected


def main():
    # 1. načíst data
    # 2. zjistit, jaký rok je nejstarší
    # 3. vytvořit seznam seznamů, kde vnější seznam reprezentuje rok (první
    # položka seznamu reprezentuje nejstarší rok, druhá položka následující
    # rok apod.) a vnitřní seznam reprezentuje cenu firmy v daném roce,
    # tzn. vnitřní seznam bude mít délku 500.
    # 4. firma, která v daném roce neexistovala, bude mít hodnotu None.
    # 5. firma má pevně daný index, pod kterým ji lze najít ve vnitřním seznamu
    """ ^ done """
    # 6. budu loopovat přes vnější seznam, v každé iteraci budu loopovat
    # přes vnitřní seznam. Pokud příliš mnoho firem bude mít hodnotu None,
    # pak tento rok přeskočím.
    # 7. podívám se, jak se změna akcie změnila vůči minulému roku. Podle
    # toho rozdělím váhy.
    # 8. podívám se, jak se změní cena příští rok. Zaznamenám celkový zisk.

    # get_prices_in_years()
    # test_prices_in_years()

    symbols = get_symbols()
    oldest_year = get_oldest_year(symbols)
    prices_in_years = get_prices_in_years()

    for i in range(1, len(prices_in_years) - 1):
        print("year =", oldest_year + i)
        year = prices_in_years[i]

        for j in range(len(year)):
            company = symbols[j]
            price_last_year = prices_in_years[i - 1][j]
            price_cur = prices_in_years[i][j]
            price_next_year = prices_in_years[i + 1][j]
            

main()
