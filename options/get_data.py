import yfinance as yf
import os


def get_symbols():
    symbols_file = open("s&p500.txt", "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


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


def download(symbols, frequency):
    if frequency == "weekly":
        _interval = "1wk"
    elif frequency == "monthly":
        _interval = "1mo"
    else:
        print("Unrecognized frequency!")
        return

    for i in range(len(symbols)):
        file_name = "prices/" + frequency + "/" + symbols[i] + ".csv"
        if os.path.exists(file_name):
            print("i =", i, "(file exists already)")
            continue

        print("i =", i, symbols[i])

        try:
            data = yf.download(
                tickers=symbols[i],
                period="max",
                interval=_interval
            )
            data = data.filter(["Date", "Open", "Close"])

            file_name_tmp = "prices/" + frequency + "/" + symbols[i] + \
                            "_tmp.csv"
            data.to_csv(file_name_tmp)
            filter_lines(file_name_tmp, file_name)

        except Exception:
            print("Hah caught one")
            continue


def main():
    symbols = get_symbols()
    symbols = ["GLD"]

    frequency = "weekly"
    download(symbols, frequency)


main()
