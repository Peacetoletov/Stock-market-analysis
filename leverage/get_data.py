import yfinance as yf
import os


def filter_lines(tmp_name, name):
    # Filters lines with unwanted dates
    file = open(tmp_name, "r")
    lines = file.readlines()
    file.close()

    filtered_file = open(name, "a")
    for i in range(len(lines) - 1):
        words = lines[i].split(',')
        if words[1] != "":
            filtered_file.write(lines[i])

    filtered_file.close()
    os.remove(tmp_name)


def download(symbol):

    # file_name = "prices/" + symbol + ".csv"
    file_name = symbol + ".csv"
    if os.path.exists(file_name):
        print("file exists already")
        return

    try:
        data = yf.download(
            tickers=[symbol],
            period="max",
            interval="1d"
        )
        # data = data.filter(["Date", "Low", "Close"])
        data.to_csv(file_name)

    except Exception:
        print("Hah caught one")


def main():
    symbol = "SPXU"
    download(symbol)


main()
