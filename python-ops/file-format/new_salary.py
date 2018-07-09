import re
f = open("sal1")


counter = 0
for line in f:
    if counter > 0:

        match = re.match(r'(\w+)\s+(\d+)\s+(\d+)',line.strip())
        matched_elements = match.groups()
        


        name,mobile,salary = matched_elements
        changed_line = "%s    %s" % (name, salary)
    else: 

        changed_line = "%s    %s" % ("name","salary")


    print changed_line
    counter += 1


f.close()