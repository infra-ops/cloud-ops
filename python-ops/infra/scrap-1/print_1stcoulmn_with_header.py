import csv

f = open("test.csv")

reader = csv.reader(f)

# Print only one line
counter = 0

for line in reader:

    print line[0]

    counter +=1