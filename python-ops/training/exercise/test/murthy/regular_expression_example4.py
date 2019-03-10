import re

f = open('test3', 'r')
content = f.read()
f.close() 

#Note that the date string is embedded in a square brackets. So, it is good to #look for square brackets

# Step1 - Extract the date string in square brackets

 
strings = re.findall(r'\[(.*)\]', content)
print strings


# Step 2 - Extract only desired portion of the strng.
# You will notice that there is a space before +0000. You can use 
# that as an element in the pattern

strings = re.findall(r'\[(.*)\s\+0000\]', content)
print strings

# If you want to read line by line and pring the substring of the date string

f = open('test3', 'r')
for line in f:
  date_matches = re.findall(r'\[(.*)\s\+0000\]', line)
  print date_matches
  
  # If you want to print only one element of this list
  
  print date_matches[0]
f.close()


