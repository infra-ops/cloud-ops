import BeautifulSoup as bs
import urllib2
import xlwt
import datetime
import sys
import os
import re

current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

f = "flip_status" + current_time_string  + ".xls"

workbook = xlwt.Workbook()


#############all###################


sheet = workbook.add_sheet('all')

sheet.write(0, 0, 'PRODUCTS')
sheet.write(0, 1, 'PRODUCT URLS')
sheet.write(0, 2, 'PRODUCT NAME')
sheet.write(0, 3, 'PRICE')
sheet.write(0, 4, 'IMAGE URLS')


###############6k-10k######################
some = workbook.add_sheet('some')

some.write(0, 0, 'PRODUCTS')
some.write(0, 1, 'PRODUCT URLS')
some.write(0, 2, 'PRODUCT NAME')
some.write(0, 3, 'PRICE')
some.write(0, 4, 'IMAGE URLS')


###############lowest####################

lowest = workbook.add_sheet('lowest')

lowest.write(0, 0, 'PRODUCTS')
lowest.write(0, 1, 'PRODUCT URLS')
lowest.write(0, 2, 'PRODUCT NAME')
lowest.write(0, 3, 'PRICE')
lowest.write(0, 4, 'IMAGE URLS')

##############highest######################

high = workbook.add_sheet('highest')

high.write(0, 0, 'PRODUCTS')
high.write(0, 1, 'PRODUCT URLS')
high.write(0, 2, 'PRODUCT NAME')
high.write(0, 3, 'PRICE')
high.write(0, 4, 'IMAGE URLS')



####################################################





url = 'http://www.flipkart.com/search?q=lenovo+mobile&otracker=start&as-show=on&as=off'

a = urllib2.urlopen(url)
source = a.read()
soup = bs.BeautifulSoup(source)

#product-unit unit-4 browse-product new-design
div = []
for i in soup.findAll('div', attrs={'class':'pu-details lastUnit'}):
    div.append(i)


product = soup.find('div', attrs={'class':'query-group fk-inline-block'})
sp = bs.BeautifulSoup(str(product))
product = sp.find('a').getText()
product = product.replace('&nbsp;', '')

sheet.write(1, 0, product)
sheet.write(1, 1, url)

#print len(div)
url = []
price = []
title = []
for j in div:
    s = bs.BeautifulSoup(str(j))
    try:
        l = s.find('a', attrs={'class':'fk-display-block'}).get('href')
        t = s.find('a', attrs={'class':'fk-display-block'}).getText()
    except:
        l = ''
    url.append('http://www.flipkart.com'+l)
    title.append(t)
    try:
        p1 = s.find('span', attrs={'class':'fk-font-17 fk-bold'}).text
    except:
        p1= ''
    try:
        p2 = s.find('span', attrs={'class':'fk-font-17 fk-bold 11'}).text
    except:
        p2 = ''
    try:
        p3 = s.find('span', attrs={'class':'fk-bold'}).text
    except:
        p3 = ''
    if (p1):
        price.append(p1)
    elif p2:
        price.append(p2)
    elif p3:
        price.append(p3)
    else:
        price.append('')

'''
print len(url)
print len(price)
print len(title)

print url
print price
print title
'''

###################all####################


k = 1
c = 0
for i in range(len(price)):
    sheet.write(k, 2, title[c])
    sheet.write(k, 3, price[c])
    sheet.write(k, 4, url[c])
    k+=1
    c+=1


################some################################
k = 1
c = 0
pat = '\d'
for i in range(len(price)):
    l = re.findall(pat, price[c])
    pr = ''
    for j in l:
        pr+=str(j)
    if int(pr) > 6000 and int(pr) < 10000:
        print int(pr)
        some.write(k, 2, title[c])
        some.write(k, 3, price[c])
        some.write(k, 4, url[c])
    c+=1
    k+=1
    


###############lowest###########################################

c =0
pri = []
for i in range(len(price)):
    l = re.findall(pat, price[c])
    pr = ''
    for j in l:
        pr+=str(j)
    pri.append(int(pr))
    c+=1

pri.sort()
g = len(pri)
low = pri[0]
hi = pri[g-1]

k = 1
c = 0
pat = '\d'
for i in range(len(price)):
    l = re.findall(pat, price[c])
    pr = ''
    for j in l:
        pr+=str(j)
    if int(pr) == low:
        print int(pr)
        lowest.write(k, 2, title[c])
        lowest.write(k, 3, price[c])
        lowest.write(k, 4, url[c])
    c+=1
    k+=1


###############highest###########################################

k = 1
c = 0
pat = '\d'
for i in range(len(price)):
    l = re.findall(pat, price[c])
    pr = ''
    for j in l:
        pr+=str(j)
    if int(pr) == hi:
        print int(pr)
        high.write(k, 2, title[c])
        high.write(k, 3, price[c])
        high.write(k, 4, url[c])
    c+=1
    k+=1



##########################################################


workbook.save(f)
