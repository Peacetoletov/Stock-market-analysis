import os

# remove shit like "g AG.csv" based on the header

# update: "g AG.csv" was literally the only file with a scuffed header
# ¯\_(ツ)_/¯

def get_symbols():
    symbols_file = open("symbols/symbols.txt", "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


def main():
    symbols = get_symbols()
    garbage_files = 0
    for symbol in symbols:
        path = "company_data/" + symbol + ".csv"
        file = open(path, "r")
        header = file.readline()
        file.close()

        if header != "Date,Open,High,Low,Close,Adj Close,Volume\n":
            garbage_files += 1
            print(symbol, "is a garbage file!")
            os.remove(path)

    print(garbage_files, "garbage files in total")


main()
