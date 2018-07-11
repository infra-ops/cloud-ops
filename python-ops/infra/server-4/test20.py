import BeautifulSoup as bs
import urllib2
import xlwt
import datetime
import sys
import os
import re
import requests



current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

f = "url_status" + current_time_string  + ".xls"

workbook = xlwt.Workbook()

'''
#############just###################


just = workbook.add_sheet('just')

just.write(0, 0, 'WEBSITE URL')
just.write(0, 1, 'CLINIC NAME')
just.write(0, 2, 'PHONE NO')
just.write(0, 3, 'CLINIC URLS')

'''
###############yellow######################
yellow = workbook.add_sheet('yellow')

yellow.write(0, 0, 'WEBSITE URL')
yellow.write(0, 1, 'CLINIC NAME')
yellow.write(0, 2, 'PHONE NO')
yellow.write(0, 3, 'CLINIC URLS')


#url = 'http://kolkata.yellowpages.co.in/Hospitals'

url = sys.argv[1]

a = requests.get(url)

source = a.content

soup = bs.BeautifulSoup(source)


def runfile(arg):
    f1 = open(arg, 'r')

    a = f1.readlines()
    urls = [url.strip() for url in a ]

for i in urls:
        try:
            
        
            

    f1.close()


runfile(arg)





clinic = soup.findAll('h2', attrs={'class':'listingName'})
phone = soup.findAll('div', attrs={'class':'phoneDetails'})
url = soup.findAll('a', attrs={'class':'underlineNone jqPaidBusinessLink'})


print len(url)
print len(clinic)
print len(phone)

urls = []
clinics = []
phones = []

for i in range(len(url)):
    c = bs.BeautifulSoup(str(clinic[i]))
    p = bs.BeautifulSoup(str(phone[i]))
    u = bs.BeautifulSoup(str(url[i]))
    urls.append(u.find('a').get('href'))
    p = str(p.find('div').text)
    p = p.strip()
    phones.append(p)
    clinics.append(c.find('h2').text)







################yellow################################
k = 1
c = 0
for i in range(len(urls)):
    yellow.write(k, 1, clinics[c])
    yellow.write(k, 2, phones[c])
    yellow.write(k, 3, urls[c])
    k+=1
    c+=1
    

########################################################
workbook.save(f)
