import csv

f = open("test21.csv")

reader = csv.reader(f)

# Print only one line
counter = 0

for line in reader:

    print line[3]

    counter +=1