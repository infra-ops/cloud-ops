import csv

f = open("test.csv")

reader = csv.reader(f)

counter = 0
for line in reader:
    counter += 1
    if counter % 2 == 0:
        print line


