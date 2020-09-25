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


def filter_lines(lines, name):
    filtered_file = open(name, "a")
    for line in lines:
        day = line[8] + line[9]
        if day == "01" or line == "Date,Open,Close\n":
            filtered_file.write(line)

    filtered_file.close()


def main():
    symbols = get_symbols()

    for symbol in symbols:
        print(symbol)

        tmp_name = "prices/" + symbol + "_tmp.csv"
        name = "prices/" + symbol + ".csv"

        if os.path.exists(tmp_name):
            print("Tmp file name exists!", tmp_name)
            exit(1)
        os.rename(name, tmp_name)

        file = open(tmp_name, "r")
        lines = file.readlines()
        file.close()
        filter_lines(lines, name)

        os.remove(tmp_name)


main()
