import csv

test_file = 'test21.csv'
csv_file = csv.DictReader(open(test_file, 'rb'), delimiter=',', quotechar='"')
for line in csv_file:
    print line['authors'] + " \t" + line ["price"]
