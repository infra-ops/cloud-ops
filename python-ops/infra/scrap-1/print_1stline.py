import csv

f = open("test.csv")

reader = csv.reader(f)

# Print only one line
counter = 0
for line in reader:
    print line
    counter +=1
    if counter == 1:
        break






















    #counter +=1
    #if counter == 1:
    #    break

#i want to print 1st row data