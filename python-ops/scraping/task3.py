from bs4 import BeautifulSoup as bs
import requests
import sys,re
import xlwt
arg = sys.argv[1]

regex_email = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
regex_phone = '\d{9}'
workbook = xlwt.Workbook()

def createEmailWorkBook(result):
        sheet = workbook.add_sheet("justdail")
        sheet.write(0, 0, 'WEBSITE URL')
        sheet.write(0, 4, 'CLINIC NAME')
        sheet.write(0, 5, 'PHONE NO')
        sheet.write(0, 6, 'CLINIC URLS')
        i = 1;
        for url in result:
            sheet.write(i,0,url)
            for res in result[url]:
                sheet.write(i,4,res["name"])
                sheet.write(i,5,res["phone"])
                sheet.write(i,6,res["hosp_url"])
                i += 1

def getEmail(main_urls):
    output = {}
    for main_url in main_urls:
        output[main_url] = []
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        html = requests.get(main_url,headers=headers).text
        soup_main = bs(html,'html.parser')
        for script in soup_main(["script", "style"]): 
            script.extract()
        url_list = soup_main.find_all('h4',class_='store-name')
        for url in url_list:
            link = url.find_next('a')
            name = link.text
            link = link['href']
            phone = url.find_next('p',class_="contact-info").text
            output[main_url].append({"hosp_url":link,"name":name,"phone":phone})   
    return output


def runfile(arg):
    try:
        f1 = open(arg, 'r')
        a = f1.readlines()
        urls = [url.strip() for url in a ]
        result = getEmail(urls)
        print result
        createEmailWorkBook(result)
        f1.close()
    except Exception,e:
        print e

runfile(arg)
workbook.save("doctor4.xls")

    






