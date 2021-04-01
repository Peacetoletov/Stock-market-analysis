import yfinance as yf
import os


def get_symbols():
    symbols_file = open("s&p500_filtered.txt", "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


def main():
    symbols = get_symbols()

    for i in range(0, 337):
        file_name = "prices/" + symbols[i] + ".csv"
        if os.path.exists(file_name):
            print("i =", i, "(file exists already)")
            continue

        print("i =", i)

        try:
            data = yf.download(
                tickers=symbols[i],
                period="10y",
                interval="1d",
            )
            data = data.filter(["Date", "Adj Close"])
            data.to_csv(file_name)

        except Exception:
            print("Hah caught one")
            continue


main()
