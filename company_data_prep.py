import yfinance as yf

# This script is one-time only


symbols_file = open("No longer needed files/unfiltered_symbols.txt", "r")
lines = symbols_file.readlines()
symbols_file.close()

symbols = []
for line in lines:
    no_newline = line.rstrip('\n')
    symbols.append(no_newline)

# print(symbols[0:20])
# stock_set = symbols[0:20]
stock_set = symbols

# 105727 symbols in total
# print(len(stock_set))

# All downloadable files are downloaded - over 49 600 files

for i in range(23000, 25000):
    print("i =", i)

    file_name = "company_data_unfiltered/" + stock_set[i] + ".csv"
    data = yf.download(
        tickers=stock_set[i],
        period="max",
        interval="3mo",
        group_by='column',
        auto_adjust=True,
    )
    # ^ What the arguments mean: https://pypi.org/project/yfinance/

    if len(data.index) > 2:
        data.to_csv(file_name)
