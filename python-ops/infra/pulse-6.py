import requests
import urllib
import json
import time
import base_test
import logging

from selenium import webdriver

class TestPulseAWS(base_test.WebDriverTestCaseAWS):

    def setUp(self):
        super(TestPulseAWS, self).setUp()
        self.login()
        driver = self.driver
        driver.find_element_by_link_text(
            self.env_config.get_value("deploymentNameAWS")).click()
        driver.find_element_by_link_text("Pulse").click()
        self.assertIn('System Monitoring', self.driver.title)
        self.url = self.driver.current_url.split('/')

        pulse_metrics_end_timestamp = int(time.time())
        pulse_metrics_start_timestamp = end - 60 * 60

        self.pulse_graph_query_common_request_params = {
            "hostname[]": self.url[-3] + "-1",
            "startDate": str(pulse_metrics_start_timestamp),
            "endDate": str(pulse_metrics_end_timestamp),
            "daterangepicker": "Last 1 hour"
        }

    def tearDown(self):
        self.logout()

    def isChartActive(self, chart_data_list):
        return any(float(data_point[1]) > 0.0
                   for data_point in chart_data_list)

    def checkChartActivity(self, dataT):
        ''' checks chart data
            if chart shows activity, test passes
            else if chart shows no activity, test fails
        '''

        s = requests.session()
        token = ""
        for cookie in self.driver.get_cookies():
            if cookie['name'] == "csrftoken":
                token = cookie['value']
        headers = {
            "referer":"https://%s/admin/deployment/pulse/deployment/%s/system/" % (self.url[-8], self.url[-3]),
            "x-csrftoken":token,
        }
        s.headers.update(headers)

        test = s.post("https://%s/admin/deployment/pulse/deployment/%s/graph/"
            % (self.url[-8], self.url[-3]), data=dataT)
        content = json.loads(test.text)

        return (self.isChartActive(item['data']) for item in content['items'])

    def testPageTitle(self):
        self.driver.get('https://%s' % self.url[-8])
        self.assertIn('SearchStax', self.driver.title)

    def testSystemLoad(self):
        dataT = {
            "metricname[]": "os.SystemLoadAverage",
        }.update(self.pulse_graph_query_common_request_params)
        chart_has_data= self.checkChartActivity(dataT)
        self.assertTrue(all(chart_has_data))

    def testMemory(self):
        dataT = {
            "precision": "GB",
            "metricname[]": [{
                "0": "os.TotalPhysicalMemorySize",
                "1": "os.TotalPhysicalMemorySize-os.FreePhysicalMemorySize"
            }],
        }.update(self.pulse_graph_query_common_request_params)
        chart_has_data = self.checkChartActivity(dataT)
        self.assertTrue(all(chart_has_data))

    def testThreadCount(self):
        dataT = {
            "metricname[]": "jvm.ThreadCount",
        }.update(self.pulse_graph_query_common_request_params)
        chart_has_data = self.checkChartActivity(dataT)
        self.assertTrue(all(chart_has_data))

    def testSwap(self):
        dataT = {
            "metricname[]": [{
                "0": "os.TotalSwapSpaceSize",
                "1": "os.TotalSwapSpaceSize-os.FreeSwapSpaceSize"
            }],
        }.update(self.pulse_graph_query_common_request_params)
        chart_has_data = self.checkChartActivity(dataT)
        self.assertTrue(all(chart_has_data))

    def testHeapMemory(self):
        dataT = {
            "metricname[]": [{
                "0": "jvm.heapMemoryUsage.commited",
                "1": "jvm.heapMemoryUsage.used"
            }],
        }.update(self.pulse_graph_query_common_request_params)
        chart_has_data = self.checkChartActivity(dataT)
        self.assertTrue(all(chart_has_data))

    def testNonHeapMemory(self):
        dataT = {
            "metricname[]": [{
                "0": "jvm.nonHeapMemoryUsage.committed",
                "1": "jvm.nonHeapMemoryUsage.used"
            }],
        }.update(self.pulse_graph_query_common_request_params)
        chart_has_data = self.checkChartActivity(dataT)
self.assertTrue(all(chart_has_data))
