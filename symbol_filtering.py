from os import path

# This script is one-time only

if path.exists("No longer needed files/symbols.txt"):
    print("Filtered symbol file already exists!")
    exit(1)

symbols_file = open("No longer needed files/symbols.txt", "r")
lines = symbols_file.readlines()
symbols_file.close()

print("Creating symbols array")

symbols = []
for line in lines:
    no_newline = line.rstrip('\n')
    symbols.append(no_newline)

print("Sorting symbols")

symbols.sort()

print("Creating the filtered symbols file")

filtered_symbols_file = open("No longer needed files/symbols.txt", "a")
for symbol in symbols:
    file_name = "company_data_unfiltered/" + symbol + ".csv"
    if path.exists(file_name):
        filtered_symbols_file.write(symbol + "\n")
filtered_symbols_file.close()


"""
symbols_file = open("company_data_unfiltered/000040.KS.csv", "r")
lines = symbols_file.readlines()
symbols_file.close()

for line in lines:
    print(line)
"""