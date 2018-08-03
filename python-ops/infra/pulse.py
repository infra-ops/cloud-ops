import unittest
from selenium import webdriver
import requests
import json
import datetime
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
class SearchTestCase(base_test.WebDriverTestCase):
    def login_for_chart(self):
        ''' Logs into searchstax '''
        self.driver.get("https://app.searchstax.com/login")
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
            "authority":"app.searchstax.com",
            "method":"POST",
            "path":"/admin/deployment/pulse/deployment/ss276718/graph/",
            "scheme":"https",
            "accept":"application/json, text/javascript, */*; q=0.01",
            "accept-encoding":"gzip, deflate, br",
            "accept-language":"en-GB,en-US;q=0.9,en;q=0.8",
            #"content-length":"154"
            "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
            "origin":"https://app.searchstax.com",
            "referer":"https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/system/",
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
        end = str(1533199768)# str(int(time.time()))
        start_date = time.time() - 60*60
        start = str(1533203368)#str(int(start_date))
        dates = {
            'start_time': start,
            'end_time': end
        }
        return dates
    def isChartActive(self, chart_data_list):
        is_active = any([float(data_point[1]) > 0.0 for data_point in chart_data_list])
        return is_active
    def checkChartActivity(self, url):
        ''' checks chart data 
            if chart shows activity test passes
            else if chart shows no activity test fails
        '''
        self.login_for_chart()
        # can you go back to the chart website
        s = self.getCookiedSession()
        logging.info("url used for request is: %s", url)
        r = s.post(url, cookies=s.cookies, allow_redirects=True)
        logging.info("status code from response is: %s", str(r.status_code))
        if r.status_code in [200, 300, 301, 302]:
            # if success, start test
            
            content = r.headers['content-type']
            logging.info("this is the content") # remove after dev
            logging.info(content)  #  remove after dev
            logging.info("this is the response object: %s", str(dir(r)))
            dataT={"hostname[]":"ss276718-1","metricname[]":"os.SystemLoadAverage","startDate":"1533199768","endDate":"1533203368","daterangepicker":"Last 1 hour"}
	    test = s.post("https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/",cookies=s.cookies,data=dataT) 
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
            return all(is_active_list)   
        # for all other cases the test test fails
        return False
    def testPageTitle(self):
        self.driver.get('https://app.searchstax.com')
        self.assertIn('SearchStax', self.driver.title)
    def testSystemLoad(self):
        # hostname%5B%5D=ss276718-1&precision=&collection=&metricname%5B%5=os.SystemLoadAverage&startDate=1533126862&endDate=1533130462&daterangepicker=Last+1+hour
        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=&collection=&metricname%5B%5D=os.SystemLoadAverage&startDate=" +dates['start_time']+ "&endDate="+dates['end_time']+"&daterangepicker=Last+1+hour"
        chart_has_data = self.checkChartActivity(url)
        logging.info("ChartActivity is: %s", str(chart_has_data))
        self.assertTrue(chart_has_data)

    def testMemory(self):
        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=GB&collection=&metricname%5B%5D=os.TotalPhysicalMemorySize&metricname%5B%5D=os.TotalPhysicalMemorySize-os.FreePhysicalMemorySize&startDate=" + dates['start_time'] + "&endDate=" + dates['end_time'] + "&daterangepicker=Last+1+hour"
        chart_has_data = self.checkChartActivity(url)
        self.assertTrue(chart_has_data)
    def testThreadCount(self):
        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=int&collection=&metricname%5B%5D=jvm.ThreadCount&startDate=" + dates['start_time'] + "&endDate=" + dates['end_time'] + "&daterangepicker=Last+1+hour"
        chart_has_data = self.checkChartActivity(url)
        self.assertTrue(chart_has_data)
    def testSwap(self):
        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=GB&collection=&metricname%5B%5D=os.TotalSwapSpaceSize&metricname%5B%5D=os.TotalSwapSpaceSize-os.FreeSwapSpaceSize&startDate=" + dates['start_time'] + "&endDate=" + dates['end_time'] + "&daterangepicker=Last+1+hour"
        chart_has_data = self.checkChartActivity(url)
        self.assertTrue(chart_has_data)
    def testHeapMemory(self):
        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=GB&collection=&metricname%5B%5D=jvm.heapMemoryUsage.committed&metricname%5B%5D=jvm.heapMemoryUsage.used&startDate=" + dates['start_time'] + "&endDate=" + dates['end_time'] + "&daterangepicker=Last+1+hour"
        chart_has_data = self.checkChartActivity(url)
        self.assertTrue(chart_has_data)
    def testNonHeapMemory(self):
        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=GB&collection=&metricname%5B%5D=jvm.nonHeapMemoryUsage.committed&metricname%5B%5D=jvm.nonHeapMemoryUsage.used&startDate=" + dates['start_time'] + "&endDate=" + dates['end_time'] + "&daterangepicker=Last+1+hour"
        chart_has_data = self.checkChartActivity(url)
        self.assertTrue(chart_has_data)


if __name__ == '__main__':
    #unittest.main(verbosity=2)
    unittest.main()
#graph 1
