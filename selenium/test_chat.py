from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Foo2(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8001"
        self.verificationErrors = []
    
    def test_foo2(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("author").clear()
        time.sleep(1)
        driver.find_element_by_id("author").send_keys("titus")
        time.sleep(1)
        driver.find_element_by_id("message").clear()
        time.sleep(1)
        driver.find_element_by_id("message").send_keys("this is a test")
        time.sleep(1)
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        time.sleep(1)
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
