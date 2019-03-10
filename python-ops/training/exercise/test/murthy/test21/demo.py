name = "Murthy Raju"
house_number = "3/3"
city = "Chennai"
age = 50
weight = 72.5

print name[0:2]
print name.replace("Raju", 'raju')
print name.lower()
print name.upper()


#print "%s lives in house number %s in %s. He is %d years old and \n his weight is %.2f kgs" % ( name, house_number, city, age, weight)

s = "{} lives in {}".format(name, city)
#print s

s = "{0} lives in {1} and weighs {2:.3f} kgs".format(name, city, weight)
#print s

s = "{n} lives in {c} and weighs {w:.3f} kgs".format(c = city, 
                                                    n = name, w = weight)
print s

# Regular Expressions
# https://docs.python.org/2/library/re.html
import re

s = "Murthy Raju lives in Chennai and his email Ids are murthyraju@gmail.com and murthyraju123@gmail.com"

r'.*'


match = re.search("Raju", s)
match.group()
match.group(0)

match = re.search(r'\w+@\w+', s)
match.group()

match = re.search(r'\w+@[\w.]+', s)
match.group()

match = re.search(r'\S+@\S+\.\S+',s)
match.group()

matches = re.findall(r'\S+@\S+\.\S+',s)
print matches


s = "Murthy Raju"
import re
match = re.search(r'.*', s)
match.group()

match.group(0)

type(match)

match.group()

match = re.search(r'Mur...\s', s)
match.group()

match = re.search(r'Mur...', s)
match.group()

match = re.search(r'Mur...\s', s)
match.group()

match = re.search(r'(Mur...\s)(.*)', s)
match.group()

match.group(0)

match.group(1)

match.group(2)

match = re.search(r'(Mur.+)', s)
match.group(0)

match.group(1)

s = "Murthyraju's phne numbers are 123 and 789"
match = re.findall(r'[0-9]+',s)

match = re.findall(r'[0-9]+',s)
print match

print match[0]

print match[1]

print match[1], match[0]

 



#----
# Patterns
# a A 8 - alpha numerical literals
#. - any char except new line
#\w -   word char
#\W - non-word char
#\b - boundary between word and non-word
#\s - white space 
# \t
#\n
#\r
#\d
# ^
# $
#\ - escape
#------

#---
# Repetitions
# + - one or more occurance
# * - 0 or more occurances
# ? 0 or 1 occurances
#---

# Square brackets for range, collection etc.
# Group Extraction

# data1.txt
"""
one
two
three
four
five
"""

# data2.txt

"""
one
twenty
three
forty
five

"""

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
      
#status_file.write("Same Lines: %d and Diff Lines: %d" % ( same_lines, diff_lines))

