import yfinance as yf


def get_symbols():
    symbols_file = open("s&p500_unsorted.txt", "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


# Successful recommendations: 337
# Failed recommendations: 165

def main():
    symbols = get_symbols()

    failed = 0
    not_failed = 0
    for symbol in symbols:
        print("Symbol =", symbol)
        stock = yf.Ticker(symbol)
        try:
            dataframe = stock.recommendations.filter(["Date", "To Grade"])
            dataframe.to_csv("recommendations/" + symbol + ".csv")
            not_failed += 1
        except:
            failed += 1
        print("Failed:", failed, "Not failed:", not_failed)


main()
