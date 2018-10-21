from bs4 import BeautifulSoup

f1 = open(‘t1.html’,’r’)
f2 = open(‘image_result.txt’, ‘w’)

html_doc = f1.read()

soup = BeautifulSoup(html_doc)

image_list = soup.find_all(‘img’)
for images in image_list:

print images.get(‘src’)
f2.write(images.get(‘src’)+”\n”)

f1.close()
f2.close()
