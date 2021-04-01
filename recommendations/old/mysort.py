import os

if os.path.exists("s&p500.txt"):
    print("Path already exists!")
    exit(1)


symbols_file = open("s&p500_unsorted.txt", "r")
lines = symbols_file.readlines()
symbols_file.close()

lines.sort()

sorted_file = open("s&p500.txt", "a")
for line in lines:
    sorted_file.write(line)
sorted_file.close()