import os

# Takes 2 symbol files and creates a file containing symbols from both,
# while removing duplicates.

name1 = "unfiltered_symbols.txt"
name2 = "more_symbols.txt"

if os.path.exists("symbols/symbols_unified.txt"):
    print("Unified symbol file already exists!")
    exit(1)

symbols_file1 = open(name1, "r")
lines1 = symbols_file1.readlines()
symbols_file1.close()

symbols_file2 = open(name2, "r")
lines2 = symbols_file2.readlines()
symbols_file2.close()


symbols = []
for line in lines1:
    no_newline = line.rstrip('\n')
    symbols.append(no_newline)

for line in lines2:
    no_newline = line.rstrip('\n')
    symbols.append(no_newline)


print("Removing duplicates")
symbols = list(dict.fromkeys(symbols))

print("Sorting symbols")
symbols.sort()

print("Creating the unified symbols file")
symbols_file = open("symbols/symbols_unified.txt", "a")
for symbol in symbols:
    symbols_file.write(symbol + "\n")
symbols_file.close()