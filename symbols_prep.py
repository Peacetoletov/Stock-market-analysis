from os import path

# This script is one-time only

if path.exists("No longer needed files/unfiltered_symbols.txt"):
	print("Symbol file already exists!")
	exit(1)


csv_file = open('Yahoo Ticker Symbols.txt', 'r')
symbols_file = open("No longer needed files/unfiltered_symbols.txt", "a")
while True:
	try:
		line = csv_file.readline()
		if line == "":
			break
	except:
		print("Cannot decode, but it's fine")
		continue
	symbol = ""
	for char in line:
		if char == ';':
			break
		symbol += char
	symbols_file.write(symbol + "\n")

symbols_file.close()
csv_file.close()
