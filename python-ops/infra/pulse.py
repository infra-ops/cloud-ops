import unittest
from selenium import webdriver
import requests
import datetime
import base_test
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning, SNIMissingWarning
# silence warnings in urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)


GECKO_EXECUTABLE_PATH = "/opt/scripts/testcases/geckodriver/bin/geckodriver"


class SearchTestCase(base_test.WebDriverTestCase):

    def getCookiedSession(self):
        ''' pass cookies from selenium to requests session
        headers: headers for session.
                 User-Agent used to avoid bot detection
        s: the requests session object that will be returned. '''

        headers = {  # spoof request headers
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "authority": "app.searchstax.com",
            "method": "POST",
            "path": "/admin/deployment/pulse/deployment/ss276718/graph/",
            "scheme": "https",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        s = requests.session()
        s.headers.update(headers)
        for cookie in self.driver.get_cookies():
            c = {cookie['name']: cookie['value']}
            s.cookies.update(c)
        return s

    def makeDates(self):
        ''' makes a dict with start and end time
        start_time: now - 1 hour
        end_time: now '''

        now = datetime.datetime.now()
        dates = {
            'start_time': str(now - datetime.timedelta(hours=1)),
            'end_time': str(now)
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
        s = self.getCookiedSession()
        r = s.post(url, data={})
        if r.status_code == 200:
            # if success, start test
            content = r.json()
            print "this is the content" # remove after dev
            print content  #  remove after dev
           
            # pass the data from the chart to isChartActive
            # json data can be found by inspecting the network
            # traffic in your browser when page loads
            chart_data_list = content['items'][0]['data']
            print "this is the chart data"  # remove after development
            print chart_data_list # remove after dev
            is_active = self.isChartActive(chart_data_list)

            return is_active
            
        # for all other cases the test test fails
        return False

    def testPageTitle(self):
        self.driver.get('https://app.searchstax.com')
        self.assertIn('SearchStax', self.driver.title)

    def testSystemLoad(self):
        # hostname%5B%5D=ss276718-1&precision=&collection=&metricname%5B%5=os.SystemLoadAverage&startDate=1533126862&endDate=1533130462&daterangepicker=Last+1+hour

        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=&collection=&metricname%5B%5D=os.SystemLoadAverage&startDate=" +dates['start_time']+ "&endDate="+dates['end_time']+"&daterangepicker=Last+1+hour"

        self.checkChartActivity(url)

    def testMemory(self):
        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=GB&collection=&metricname%5B%5D=os.TotalPhysicalMemorySize&metricname%5B%5D=os.TotalPhysicalMemorySize-os.FreePhysicalMemorySize&startDate=" + dates['start_time'] + "&endDate=" + dates['end_time'] + "&daterangepicker=Last+1+hour"
        self.checkChartActivity(url)

    def testThreadCount(self):
        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=int&collection=&metricname%5B%5D=jvm.ThreadCount&startDate=" + dates['start_time'] + "&endDate=" + dates['end_time'] + "&daterangepicker=Last+1+hour"
        self.checkChartActivity(url)

    def testSwap(self):
        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=GB&collection=&metricname%5B%5D=os.TotalSwapSpaceSize&metricname%5B%5D=os.TotalSwapSpaceSize-os.FreeSwapSpaceSize&startDate=" + dates['start_time'] + "&endDate=" + dates['end_time'] + "&daterangepicker=Last+1+hour"
        self.checkChartActivity(url)

    def testHeapMemory(self):
        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=GB&collection=&metricname%5B%5D=jvm.heapMemoryUsage.committed&metricname%5B%5D=jvm.heapMemoryUsage.used&startDate=" + dates['start_time'] + "&endDate=" + dates['end_time'] + "&daterangepicker=Last+1+hour"
        self.checkChartActivity(url)

    def testNonHeapMemory(self):
        dates = self.makeDates()
        url = "https://app.searchstax.com/admin/deployment/pulse/deployment/ss276718/graph/hostname%5B%5D=ss276718-1&precision=GB&collection=&metricname%5B%5D=jvm.nonHeapMemoryUsage.committed&metricname%5B%5D=jvm.nonHeapMemoryUsage.used&startDate=" + dates['start_time'] + "&endDate=" + dates['end_time'] + "&daterangepicker=Last+1+hour"
        self.checkChartActivity(url)

if __name__ == '__main__':
    unittest.main(verbosity=2)

