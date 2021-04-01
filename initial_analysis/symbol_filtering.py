import os

# Removes all symbols that don't point to a file name

name = "recommendations/s&p500.txt"
tmp_name = "recommendations/s&p500_tmp_name.txt"
if os.path.exists(tmp_name):
    print("Error: temporary file already exists!")
    exit(1)

os.rename(name, tmp_name)
symbols_file = open(tmp_name, "r")
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
filtered_symbols_file = open(name, "a")
for symbol in symbols:
    file_name = "recommendations/recommendations/" + symbol + ".csv"
    if os.path.exists(file_name):
        filtered_symbols_file.write(symbol + "\n")
filtered_symbols_file.close()

os.remove(tmp_name)


"""
symbols_file = open("company_data_unfiltered/000040.KS.csv", "r")
lines = symbols_file.readlines()
symbols_file.close()

for line in lines:
    print(line)
"""