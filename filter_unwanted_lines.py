from os import path

"""
Filter this

Date,Open,High,Low,Close,Volume
2014-03-01,-6.684004654462127e-07,-8.322184841382872e-07,-6.518931740442218e-07,-7.9123981322482e-07,5934.0
2014-03-04,,,,,
2014-05-19,,,,,
2014-06-01,-1.3247221387453882e-06,-1.5860164968392877e-06,-1.3132252152052002e-06,-1.390889906360826e-06,41374.0
2014-08-19,,,,,
2014-09-01,-2.2067463027946927e-06,-2.2629287585084352e-06,-1.2050182783265027e-06,-1.2571970273711486e-06,205396.0
2014-11-18,,,,,
2014-12-01,-3.359129447742496e-06,-4.114039534318747e-06,-2.671022687573679e-06,-3.1747824777994538e-06,102872.0


into this


Date,Open,High,Low,Close,Volume
2014-03-01,-6.684004654462127e-07,-8.322184841382872e-07,-6.518931740442218e-07,-7.9123981322482e-07,5934.0
2014-06-01,-1.3247221387453882e-06,-1.5860164968392877e-06,-1.3132252152052002e-06,-1.390889906360826e-06,41374.0
2014-09-01,-2.2067463027946927e-06,-2.2629287585084352e-06,-1.2050182783265027e-06,-1.2571970273711486e-06,205396.0
2014-12-01,-3.359129447742496e-06,-4.114039534318747e-06,-2.671022687573679e-06,-3.1747824777994538e-06,102872.0
"""


def get_symbols():
    symbols_file = open("No longer needed files/symbols.txt", "r")
    lines = symbols_file.readlines()
    symbols_file.close()

    symbols = []
    for line in lines:
        no_newline = line.rstrip('\n')
        symbols.append(no_newline)

    return symbols


def filter_data(symbol, data):
    filtered_file_name = "company_data_filtered/" + symbol + ".csv"
    filtered_file = open(filtered_file_name, "a")
    for line in data:
        words = line.split(',')
        if words[1] != "":
            filtered_file.write(line)

    filtered_file.close()


def filter_empty_lines():
    symbols = get_symbols()

    # symbols = ["AUX.BE"]

    last_successful_write = 0
    for i in range(last_successful_write, len(symbols)):
        symbol = symbols[last_successful_write]
        print(last_successful_write, "Company symbol =", symbol)

        company_file_name = "company_data_unfiltered/" + symbol + ".csv"
        company_file = open(company_file_name, "r")
        data = company_file.readlines()
        company_file.close()
        filter_data(symbol, data)

        last_successful_write += 1


def main():
    # Závěr - většina dat bude končit na 01, může se ale občas objevit i
    # jiné datum. Rovněž nemusí být v každém roce 4 data - může jich být
    # více nebo i méně.
    # Rozumný způsob, jak data analyzovat, bude, že se podívám na první
    # záznam a zkusím, jestli existuje záznam se stejným datem, ale o 1
    # vyšším rokem. Pokud ne, tak se posunu na další záznam, a od něho se
    # zase dívám, jestli existuje záznam se stejným datem, ale rokem o 1
    # vyšším.

    # check how many lines there are with a different day than 01
    symbols = get_symbols()
    # symbols = ["ACR.DU"]
    for symbol in symbols:
        filtered_file_name = "company_data_filtered/" + symbol + ".csv"
        filtered_file = open(filtered_file_name, "r")
        data = filtered_file.readlines()

        non_01 = 0
        for line in data:
            if line == "Date,Open,High,Low,Close,Volume\n":
                continue
            # 2014-03-01    # 8. a 9. pozice mě zajímá
            if line[8] != "0" or line[9] != "1":
                """
                print("The non01 line is", line)
                print("line[8] =", line[8], "line[9] =", line[9])
                """
                non_01 += 1

        if non_01 > 1:
            print("Company", symbol, "has more than 1 non01 line")
        filtered_file.close()


main()
