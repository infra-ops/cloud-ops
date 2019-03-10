import re
f = open("sal1")
fw = open("target_file.txt",'w')

counter = 0
for line in f:
    if counter > 0:
        #Regex match - 3 columns of text, 
        #numbers, numbers seperated by        
        #certain number of spaces
        #Each match is placed into a 
        #group by using brackets

        match = re.match(r'(\w+)\s+(\d+)\s+(\d+)',line.strip())
        matched_elements = match.groups()
        
        #matched_elements is now a tuple with 3 elements.
        #Assign the tuple to 3 variables - name, mobile, salary

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
