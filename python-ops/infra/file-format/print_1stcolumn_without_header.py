import csv

f = open("test.csv")

reader = csv.reader(f)

# Print only one line
counter = 0

for line in reader:

    if counter > 0 :

       print line[0]

    counter +=1
