import os

# this script does what remove_nonpositive_price_files does, but better


def get_symbols():
    symbols_file = open("symbols/s&p500.txt", "r")
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
        my_path = "company_data/" + symbol + ".csv"
        file = open(my_path, "r")
        file.readline()
        lines = file.readlines()
        file.close()

        contains_low_price = False
        for line in lines:
            price = float(line.split(',')[4])   # closing price
            if price <= 0.01:
                contains_low_price = True
                garbage_files += 1
                print(symbol, "is a garbage file!")
                break

        #if contains_low_price:
        #    os.remove(my_path)

    print(garbage_files, "garbage files in total")


main()
