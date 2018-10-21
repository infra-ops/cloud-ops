from bs4 import BeautifulSoup as bs
import requests
import sys,re
import xlwt
arg = sys.argv[1]

regex_email = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
regex_phone = '\d{9}'


def createWorkBook(result):
    workbook = xlwt.Workbook() 
    sheet = workbook.add_sheet("ins")
    sheet.write(0, 0, 'WEBSITE')
    sheet.write(0, 1, 'EMAIL')
    sheet.write(0, 2, 'PHONE')
    i = 1;
    for url in result:
        print i
        sheet.write(i,0,url)
        sheet.write(i,1,result[url]["email"])
        for phone in result[url]["phone"]:
            sheet.write(i,2,phone)
            i += 1
        i += 1
    workbook.save("ins3.xls")
    
def getEmail(html):
    soup = bs(html,'html.parser')
    for script in soup(["script", "style"]): # remove all javascript and stylesheet code
        script.extract()
    words = soup.get_text()
    email = list((email[0] for email in re.findall(regex_email, words) if not email[0].startswith('//')))
    if len(email[0].split('|')) == 2:
        email[0] = email[0].split('|')[1]
    phone = re.findall(regex_phone, words)
    return email[0],phone

def runfile(arg):
    result = {}
    try:
        f1 = open(arg, 'r')
        a = f1.readlines()
        urls = [url.strip() for url in a ]
        for i in urls:
            if i.strip():
                mail,phone_nos = getEmail(requests.get(i).text)
                result[i] = {"email":mail,"phone":phone_nos}                                                              
        createWorkBook(result)
        f1.close()
    except Exception,e:
        print e

runfile(arg)


    






