f1 = open('test3', 'r')
for line in f1:
match = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )

print match
f1.close()




f1 = open('test3', 'r')
f2 = open('test04.txt','w')
for line in f1:
  date_matches = re.findall(r'\[(.*)\s\+0000\]', line)
  #print date_matches

  # If you want to print only one element of this list

  #print date_matches[0]
  f2.write(date_matches[0])
f1.close()
f2.close()

f2.write(date_matches[0] + "\n") 