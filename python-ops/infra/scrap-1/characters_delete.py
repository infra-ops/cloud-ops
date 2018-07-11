import re

"""""
f = open('test2').read()
new_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', f)
open('test2_new.txt', 'w').write(new_str)


"""""


f = open('test2')
new_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', f)
print new_str
f.close()



