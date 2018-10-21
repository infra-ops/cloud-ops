import BeautifulSoup as bs
import urllib2
import xlwt
import datetime
import sys
import os
import re

current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

f = "url_status" + current_time_string  + ".xls"

workbook = xlwt.Workbook()



#############just###################


first = workbook.add_sheet('all')

first.write(0, 0, 'WEBSITE')
first.write(0, 1, 'EMAIL')
first.write(0, 2, 'PHONE NO')




	


###############yellow######################
second = workbook.add_sheet('all')

second.write(0, 0, 'WEBSITE')
second.write(0, 1, 'EMAIL')
second.write(0, 2, 'PHONE NO')
################logic############################





arg = sys.argv[1]

def runfile(arg):
    f1 = open(arg, 'r')

    a = f1.readlines()
    urls = [url.strip() for url in a ]

    for i in urls:
        try:
            a = urllib2.urlopen(i)
            source = a.read()
            pat = '\d{9}'
            phone = re.findall(pat, source)
            print phone
        except:
            pass

    f1.close()


runfile(arg)

###################write###################
###################just####################


k = 1
c = 0
for i in range(len(price)):
    first.write(k, 2, title[c])
    first.write(k, 3, price[c])
    first.write(k, 4, url[c])
    k+=1
    c+=1


################yellow################################
k = 1
c = 0
for i in range(len(price)):
    second.write(k, 2, title[c])
    second.write(k, 3, price[c])
    second.write(k, 4, url[c])
    k+=1
    c+=1
    

########################################################
workbook.save(f)


#python i5.py urls3
    






