
f1 = open("/home/trainer/Desktop/data1.txt")

f2 = open("/home/trainer/Desktop/data2.txt")

status_file = open("/home/trainer/Desktop/status.txt", "w")

same_lines = 0
diff_lines = 0

counter = 1
for line1 in f1:
    line2 = f2.readline()
    if line1 == line2:
        same_lines += 1
    else:
        diff_lines += 1
        #status_file.write("There are differences in %d" % (counter,))
        status_file.write(line2)
    counter += 1

