import yfinance as yf
import os


symbols_file = open("symbols/s&p500.txt", "r")
lines = symbols_file.readlines()
symbols_file.close()

symbols = []
for line in lines:
    no_newline = line.rstrip('\n')
    symbols.append(no_newline)


# Unfiltered_symbols stáhnuto: 105727 (max)
# more_symbols stáhnuto: 5389 (max)

for i in range(0, 510):
    file_name = "company_data/" + symbols[i] + ".csv"
    if os.path.exists(file_name):
        print("i =", i, "(file exists already)")
        continue

    print("i =", i)

    try:
        data = yf.download(
            tickers=symbols[i],
            period="max",
            interval="3mo",
            # Auto adjust must be False! (default)
        )
        # ^ What the arguments mean: https://pypi.org/project/yfinance/

        if len(data.index) > 2:
            data.to_csv(file_name)
    except Exception:
        print("Hah caught one")
        continue
