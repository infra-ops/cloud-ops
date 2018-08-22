import unittest
from selenium import webdriver
import requests
import os
import urllib
import json
import datetime
import subprocess
import time
import base_test
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning, SNIMissingWarning
# silence warnings in urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)
logging.basicConfig(filename='SearchTestCase.log', level=logging.INFO)

GECKO_EXECUTABLE_PATH = "/opt/scripts/testcases/geckodriver/bin/geckodriver"
end = int(time.time())
start_date = end - 60*60
start = str(int(start_date))
dates ={'start_time': start,'end_time': str(end)}
cwd= os.getcwd()
def tokenv():
 with requests.session() as q:
  if os.path.exists("%s/temp.txt"%cwd) and os.path.getsize("%s/temp.txt"%cwd) > 0:
	fox=open("temp.txt","r+")
	apk= "%s"%fox.readline().rstrip(" ")
	log = q.get("https://app.searchstax.co/api/rest/v2/account/TDQ53Q02KT/deployment/",headers={"Authorization":apk})
	if "expired" or "invalid" not in log.text:
		return log.text
		all=json.loads(log.text)
	else:
		fox.close()
		subprocess.Popen("rm temp.txt", shell=True, stdout=subprocess.PIPE)
        	foo= open("temp.txt","w+")
        	da={"username":"xxxxxxx","password":"xxxxxx"}
        	fl = q.post("https://app.searchstax.co/api/rest/v1/obtain-auth-token/",data=da)
       		tok = json.loads(fl.text)
 	        apk= "Token %s"%tok["token"]
        	log = q.get("https://app.searchstax.co/api/rest/v2/account/TDQ53Q02KT/deployment/",headers={"Authorization":apk})
     		if "expired" not in log.text:
                	foo.write(apk)
                	foo.close()
			tokenv()
       		else:
	                print "EXIT CODE 2"
  else:
	foo= open("temp.txt","w+")
        da={"username":"xxxxxxxx","password":"xxxxxx"}
        fl = q.post("https://app.searchstax.co/api/rest/v1/obtain-auth-token/",data=da)
        tok = json.loads(fl.text)
        apk= "Token %s"%tok["token"]
        log = q.get("https://app.searchstax.co/api/rest/v2/account/TDQ53Q02KT/deployment/",headers={"Authorization":apk})
        if "expired" not in log.text:
		foo.write(apk)
		foo.close()
		tokenv()
	else:
		print "EXIT CODE 2"

all=json.loads(tokenv())
host=str(all["results"][0]["uid"])
servs=all["results"][0]["servers"]
class SearchTestCase(base_test.WebDriverTestCase):
    def login_for_chart(self):
        ''' Logs into searchstax '''
        self.driver.get("https://app.searchstax.co/login")
        username_element = self.driver.find_elements_by_name("email")[0]
        password_element = self.driver.find_elements_by_name("password")[0]
        submit_button = self.driver.find_element_by_css_selector("button.fright.button.blue_button.small_button")
        username_element.clear()
        password_element.clear()
        username_element.send_keys("xxxxxxx")
        password_element.send_keys("xxxxxxx")
        submit_button.click()
    def getCookiedSession(self):
        ''' pass cookies from selenium to requests session
        headers: headers for session.
                 User-Agent used to avoid bot detection
        '''
        current_url = self.driver.current_url
        logging.info("current url selenium is at: %s", current_url)
        s = requests.session()
        token = ""
        for cookie in self.driver.get_cookies():
            c = {cookie['name']: cookie['value']}
            logging.info("cookie: %s:%s", cookie['name'], cookie['value'])
            if cookie['name'] == "csrftoken":
                token = cookie['value']
            s.cookies.update(c)
        logging.info("the token is: %s", token)
        logging.info("cookies are: %s", str(s.cookies)) 
        headers = {
            "authority":"app.searchstax.co",
            "method":"POST",
            "path":"/admin/deployment/pulse/deployment/ss220736/graph/",
            "scheme":"https",
            "accept":"application/json, text/javascript, */*; q=0.01",
            "accept-encoding":"gzip, deflate, br",
            "accept-language":"en-GB,en-US;q=0.9,en;q=0.8",
            #"content-length":"154"
            "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
            "origin":"https://app.searchstax.co",
            "referer":"https://app.searchstax.co/admin/deployment/pulse/deployment/ss220736/system/",
            "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "x-csrftoken":token,
            "x-requested-with":"XMLHttpRequest"
        }
        s.headers.update(headers)
        return s
    def makeDates(self):
        ''' makes a dict with start and end time
        start_time: now - 1 hour
        end_time: now '''
        end = int(time.time())
        start_date = end - 60*60
        start = str(int(start_date))
        dates = {
            'start_time': start,
            'end_time': str(end)
        }
    def isChartActive(self, chart_data_list):
        is_active = any([float(data_point[1]) > 0.0 for data_point in chart_data_list])
        return is_active
    def checkChartActivity(self, url,dataT):
        ''' checks chart data 
            if chart shows activity test passes
            else if chart shows no activity test fails
        '''
        self.login_for_chart()
        # can you go back to the chart website
        s = self.getCookiedSession()
        logging.info("url used for request is: %s"%url)
	#da={"username":"xxxxxxx","password":"xxxxxx"}
        #fl = s.post("https://app.searchstax.co/api/rest/v1/obtain-auth-token/",data=da)
	#tok = json.loads(fl.text)
	#log = s.get("https://app.searchstax.co/api/rest/v2/account/TDQ53Q02KT/deployment/")
	r = s.post(url, cookies=s.cookies, allow_redirects=True)
        logging.info("status code from response is: %s"%str(r.status_code))
        if r.status_code in [200, 300, 301, 302]:
            # if success, start test
            
            content = r.headers['content-type']
            logging.info("this is the content") # remove after dev
            logging.info(content)  #  remove after dev
            logging.info("this is the response object: %s"%str(dir(r)))
	    test = s.post("https://app.searchstax.co/admin/deployment/pulse/deployment/%s/graph/"%host,cookies=s.cookies,data=dataT) 
	    logging.info("content x:%s"%test.text)
	    Ncontent = json.loads(test.text)
            logging.info("URL returned is: %s", str(r.url))
            # pass the data from the chart to isChartActive
            # json data can be found by inspecting the network
            # traffic in your browser when page loads
            
            is_active_list = []
            for item in Ncontent["items"]:
                chart_data_list = item['data']
                logging.info("Chart data: %s", str(chart_data_list))
                is_active = self.isChartActive(chart_data_list)
                is_active_list.append(is_active)
            return is_active_list 
        # for all other cases the test test fails
        return False
    def testPageTitle(self):
        self.driver.get('https://app.searchstax.co')
        self.assertIn('SearchStax', self.driver.title)
    def testSystemLoad(self):
        # hostname%5B%5D=ss276718-1&precision=&collection=&metricname%5B%5=os.SystemLoadAverage&startDate=1533126862&endDate=1533130462&daterangepicker=Last+
	for gg in range(0,len(servs)):
		print "SERVER: %s\r"%str(servs[gg])
		dataT={"hostname[]":"%s"%str(servs[gg]),"metricname[]":"os.SystemLoadAverage","startDate":"%s"%dates['start_time'],"endDate":"%s"%dates['end_time'],"daterangepicker":"Last 1 hour"}
		url = "https://app.searchstax.co/admin/deployment/pulse/deployment/%s/graph/%s"%(host,str(urllib.urlencode(dataT)))
		chart_has_data= self.checkChartActivity(url,dataT)
		logging.info("ChartActivity is: %s", str(chart_has_data))
        	self.assertTrue(chart_has_data)
    def testMemory(self):
	for gg in range(0,len(servs)):
		print "SERVER: %s\r"%str(servs[gg])
		dataT={"hostname[]":"%s"%str(servs[gg]),"precision":"GB","metricname[]":[{"0":"os.TotalPhysicalMemorySize","1":"os.TotalPhysicalMemorySize-os.FreePhysicalMemorySize"}],"startDate":"%s"%dates['start_time'],"endDate":"%s"%dates['end_time'],"daterangepicker":"Last 1 hour"}
        	url = "https://app.searchstax.co/admin/deployment/pulse/deployment/%s/graph/%s"%(host,str(urllib.urlencode(dataT)))
        	chart_has_data = self.checkChartActivity(url,dataT)
        	self.assertTrue(chart_has_data)
    def testThreadCount(self):
	for gg in range(0,len(servs)):
		print "SERVER: %s\r"%str(servs[gg])
		dataT={"hostname[]":"%s"%str(servs[gg]),"metricname[]":"jvm.ThreadCount","startDate":"%s"%dates['start_time'],"endDate":"%s"%dates['end_time'],"daterangepicker":"Last 1 hour"}
        	url = "https://app.searchstax.co/admin/deployment/pulse/deployment/%s/graph/%s"%(host,str(urllib.urlencode(dataT)))
        	chart_has_data = self.checkChartActivity(url,dataT)
        	self.assertTrue(chart_has_data)
    def testSwap(self):
        for gg in range(0,len(servs)):
		print "SERVER: %s\r"%str(servs[gg])
		dataT={"hostname[]":"%s"%str(servs[gg]),"metricname[]":[{"0":"os.TotalSwapSpaceSize","1":"os.TotalSwapSpaceSize-os.FreeSwapSpaceSize"}],"startDate":"%s"%dates['start_time'],"endDate":"%s"%dates['end_time'],"daterangepicker":"Last 1 hour"}
		url = "https://app.searchstax.co/admin/deployment/pulse/deployment/%s/graph/%s"%(host,str(urllib.urlencode(dataT)))
		chart_has_data = self.checkChartActivity(url,dataT)
        	self.assertTrue(chart_has_data)
    def testHeapMemory(self):
        for gg in range(0,len(servs)):
		print "SERVER: %s\r"%str(servs[gg])
		dataT={"hostname[]":"%s"%str(servs[gg]),"metricname[]":[{"0":"jvm.heapMemoryUsage.commited","1":"jvm.heapMemoryUsage.used"}],"startDate":"%s"%dates['start_time'],"endDate":"%s"%dates['end_time'],"daterangepicker":"Last 1 hour"}
		url = "https://app.searchstax.co/admin/deployment/pulse/deployment/%s/graph/%s"%(host,str(urllib.urlencode(dataT)))
        	chart_has_data = self.checkChartActivity(url,dataT)
        	self.assertTrue(chart_has_data)
    def testNonHeapMemory(self):
        for gg in range(0,len(servs)):
		print "SERVER: %s\r"%str(servs[gg])
		dataT={"hostname[]":"%s"%str(servs[gg]),"metricname[]":[{"0":"jvm.nonHeapMemoryUsage.committed","1":"jvm.nonHeapMemoryUsage.used"}],"startDate":"%s"%dates['start_time'],"endDate":"%s"%dates['end_time'],"daterangepicker":"Last 1 hour"}
		url = "https://app.searchstax.co/admin/deployment/pulse/deployment/%s/graph/%s"%(host,str(urllib.urlencode(dataT)))
        	chart_has_data = self.checkChartActivity(url,dataT)
        	self.assertTrue(chart_has_data)
if __name__ == '__main__':
    #unittest.main(verbosity=2)
	unittest.main()
#graph 1
