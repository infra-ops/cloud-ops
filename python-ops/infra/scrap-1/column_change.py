import csv

#print 2nd and 3rd coulmn data with delimeter

#test_file = 'test.csv'
#csv_file = csv.DictReader(open(test_file, 'rb'), delimiter=',', quotechar='"')
#for line in csv_file:
#     print line['title'] + " : " +  line["price"]



f = open("test.csv")

reader = csv.reader(f)

counter = 0
for line in reader:
    counter += 1

#line_count = counter

print "Number of lines is " + str(line_count)

f.close()