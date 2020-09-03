import os

# one time only


def get_symbols():
    symbols_file = open("No longer needed files/symbols.txt", "r")
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
    new_symbols_file = open("symbols.txt", "a")
    for symbol in symbols:
        my_path = "company_data_filtered/" + symbol + ".csv"
        file = open(my_path, "r")
        file.readline()
        lines = file.readlines()
        file.close()

        contains_negative_price = False
        for line in lines:
            price = float(line.split(',')[4])
            if price < 0:
                contains_negative_price = True
                garbage_files += 1
                print(symbol, "is a garbage file!")
                break

        if contains_negative_price:
            os.remove(my_path)
        else:
            new_symbols_file.write(symbol + '\n')

    print(garbage_files, "garbage files in total")

    new_symbols_file.close()


main()
