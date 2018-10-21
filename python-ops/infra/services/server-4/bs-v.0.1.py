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


just = workbook.add_sheet('just')

just.write(0, 0, 'WEBSITE URL')
just.write(0, 1, 'CLINIC NAME')
just.write(0, 2, 'PHONE NO')
just.write(0, 3, 'CLINIC URLS')


###############yellow######################
#yellow = workbook.add_sheet('yellow')
#
#yellow.write(0, 0, 'WEBSITE URL')
#yellow.write(0, 1, 'CLINIC NAME')
#yellow.write(0, 2, 'PHONE NO')
#yellow.write(0, 3, 'CLINIC URLS')


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
    just.write(k, 2, title[c])
    just.write(k, 3, price[c])
    just.write(k, 4, url[c])
    k+=1
    c+=1


################yellow################################
#k = 1
#c = 0
#for i in range(len(price)):
#    yellow.write(k, 2, title[c])
#    yellow.write(k, 3, price[c])
#    yellow.write(k, 4, url[c])
#    k+=1
#    c+=1
    

########################################################
workbook.save(f)


#python i4.py urls2
    






