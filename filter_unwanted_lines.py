import os

"""
Filter this

Date,Open,High,Low,Close,Adj Close,Volume
2014-03-01,-6.684004654462127e-07,-8.322184841382872e-07,-6.518931740442218e-07,-7.9123981322482e-07,5934.0
2014-03-04,,,,,
2014-05-19,,,,,
2014-06-01,-1.3247221387453882e-06,-1.5860164968392877e-06,-1.3132252152052002e-06,-1.390889906360826e-06,41374.0
2014-08-19,,,,,
2014-09-01,-2.2067463027946927e-06,-2.2629287585084352e-06,-1.2050182783265027e-06,-1.2571970273711486e-06,205396.0
2014-11-18,,,,,
2014-12-01,-3.359129447742496e-06,-4.114039534318747e-06,-2.671022687573679e-06,-3.1747824777994538e-06,102872.0


into this


Date,Open,High,Low,Close,Adj Close,Volume
2014-03-01,-6.684004654462127e-07,-8.322184841382872e-07,-6.518931740442218e-07,-7.9123981322482e-07,5934.0
2014-06-01,-1.3247221387453882e-06,-1.5860164968392877e-06,-1.3132252152052002e-06,-1.390889906360826e-06,41374.0
2014-09-01,-2.2067463027946927e-06,-2.2629287585084352e-06,-1.2050182783265027e-06,-1.2571970273711486e-06,205396.0
2014-12-01,-3.359129447742496e-06,-4.114039534318747e-06,-2.671022687573679e-06,-3.1747824777994538e-06,102872.0
"""


def get_symbols():
    symbols_file = open("symbols/s&p500.txt", "r")
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
        words = line.split(',')
        if words[1] != "":
            filtered_file.write(line)

    filtered_file.close()


def main():
    symbols = get_symbols()

    for symbol in symbols:
        print(symbol)

        tmp_name = "company_data/" + symbol + "_tmp.csv"
        name = "company_data/" + symbol + ".csv"

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
