"""
Vezme data z data_raw a vytvoří jeden datový soubor ve složce data.
1. Sloučí 24 souborů do 1.
2. Vytvoří rozumný název finálního souboru (SPY.csv)
"""


import os


def main():
    # extended_intraday_SPY_5min_year1month1_adjusted.csv

    processed_file_name = "data_5min/XOM.csv"
    if os.path.exists(processed_file_name):
        print("File already exists!")
        exit(1)

    processed_file = open(processed_file_name, 'a')
    processed_file.write("Time,Open,High,Low,Close,Volume\n")

    for year in range(1, 3):
        for month in range(1, 13):
            raw_file = open("data_5min_raw/extended_intraday_XOM_5min_year"
                            + str(year) + "month" + str(month) +
                            "_adjusted.csv", 'r')
            raw_file.readline()
            lines = raw_file.readlines()
            raw_file.close()
            for line in lines:
                processed_file.write(line)

    processed_file.close()


main()
