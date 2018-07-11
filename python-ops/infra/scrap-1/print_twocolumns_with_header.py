import re
f = open("sal1")
fw = open("target_file.txt",'w')

counter = 0
for line in f:
    if counter > 0:


        match = re.match(r'(\w+)\s+(\d+)\s+(\d+)',line.strip())
        matched_elements = match.groups()



        name,mobile,salary = matched_elements
        changed_line = "%s    %s" % (name, salary)
    else:
        # Header Row. So, do not attempt any regex matching
        changed_line = "%s    %s" % ("name","salary")

    #Write the changed_line to the file
    fw.write(changed_line)
    fw.write("\n")

    counter += 1

fw.close()
f.close()
