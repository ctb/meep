from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Foo(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000"
        self.verificationErrors = []
    
    def test_foo(self):
        driver = self.driver
        driver.get(self.base_url + "/quotes-2.html")
        driver.find_element_by_id("generate").click()
        time.sleep(1)
        driver.find_element_by_id("generate").click()
        time.sleep(1)
        driver.find_element_by_id("generate").click()
        time.sleep(1)
        driver.find_element_by_id("generate").click()
        time.sleep(1)
        driver.find_element_by_id("generate").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
