from os import path

# This script is one-time only

csv_file_name = "s&p500.csv"
symbol_file_name = "symbols/s&p500.txt"

if path.exists(symbol_file_name):
	print("Symbol file already exists!")
	exit(1)


csv_file = open(csv_file_name, 'r')
symbols_file = open(symbol_file_name, "a")
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
