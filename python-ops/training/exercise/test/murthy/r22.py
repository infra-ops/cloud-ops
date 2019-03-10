import re

f = open('test3', 'r')
strings = re.findall(r'\d\d\d\d', f.read())
print strings
f.close()