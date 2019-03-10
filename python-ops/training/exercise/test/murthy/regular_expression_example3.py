import re



f = open('test3', 'r')
strings = re.findall(r'\d\d\d\d', f.read())
print strings
f.close()

#string = "Once you have accomplished small things, you may attempt great ones safely."

# Return all words beginning with character 'a', as a list of strings

#print re.findall(r"\ba[\w]*", string)
#print re.split("\W+", string)
#print re.sub("[ ,.]", ":", string)