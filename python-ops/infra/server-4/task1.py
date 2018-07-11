from bs4 import BeautifulSoup as bs
import requests
import sys,os

url = sys.argv[1]
try:
	filename = sys.argv[2]
except:
	filename = "" 

def removeStyle(html):
	#To remove all inline style & script
    soup = bs(html,'html.parser')
    for script in soup(["script","style","link"]): # remove all javascript and stylesheet code
        script.extract()
    return soup

def removeParticularCSS(html,css_file_name):
	soup = bs(html,'html.parser')
	links = soup.find_all("link",rel="stylesheet")
	for link in links:
		if css_file_name == os.path.basename(link['href']):
			link.replaceWith('')
	return soup

def runfile(url,filename):
	output = ""
	try:
		if filename:
			output = removeParticularCSS(requests.get(url).text,filename)
		else:
			output = removeStyle(requests.get(url).text)
		with open(filename+"_css_removed.html","w") as f:
			f.write(str(output))
		print "Successful"
	except Exception,e:
		print e		
runfile(url,filename)


    






