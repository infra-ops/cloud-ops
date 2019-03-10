from bs4 import BeautifulSoup

f = open("chennai.html")
html_doc = f.read()
#print html_doc

soup = BeautifulSoup(html_doc)

#print(soup.prettify())

#print soup.title.text

#print soup.p.text

"""
paras_list = soup.find_all('p')
for para in paras_list:
    print para.text
"""

#print soup.find_all('p', {"class":'normal_content'})

#print soup.find('h2', {"id":'geo_section_heading'}).text

image_node = soup.find('img')

image_src =  image_node.attrs['src']