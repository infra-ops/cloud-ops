import csv

f = open("test.csv")

reader = csv.reader(f)

counter = 0
for line in reader:
    counter += 1    
    
line_count = counter

print "Number of lines is " + str(line_count)

f.close()


f = open("test.csv")

reader = csv.reader(f)

first_line_to_print = line_count - 4
counter = 0

line_f = 1
line_l = 5

for line in reader:

    #counter += 1

    """
    if counter < first_line_to_print:
        continue
    else:
        print line

    """
    if counter >= line_f and counter <= line_l:

          print line[0]
          #print "#" + line[0]
          counter += 1
    else:

          counter += 1
          continue

    #    continue
    #else:
    #    print line
















