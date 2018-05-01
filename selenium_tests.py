from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

class testFrontEnd(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
		   command_executor='http://selenium-chrome:4444/wd/hub',
		   desired_capabilities=DesiredCapabilities.CHROME
        )

    def testCreateAccount(self):
        driver = self.driver
        driver.get("http://web:8000/bakery/")
        assert "Bakery" in driver.title
        elem = driver.find_element_by_link_text('Create Account')
        elem.click()
        name = driver.find_element_by_name("username")
        name.clear()
        name.send_keys("TestUser")
        password = driver.find_element_by_name("password")
        password.clear()
        password.send_keys("1234")
        #password.click()
        #password.send_keys(Keys.RETURN)

        #password.submit()
        submit = driver.find_element_by_id("submit")
        submit.click()

        try:
            tag = wait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h1'))).text
            tag = driver.find_element_by_tag_name('h2')
            print(tag)
            if "Sign" in tag.text:
                assert True
            #assert True
        except NoSuchElementException:
            print(tag)
            assert False


    # def testCreateItem_Search(self):
    #     driver = self.driver
    #     driver.get("http://web:8000/bakery/search")
    #     #assert "Bakery" in driver.title
    #
    #     elem = driver.find_element_by_name("Search:")
    #     elem.clear()
    #     elem.send_keys("Cake")
    #     assert "No results found." not in driver.page_source
    #     driver.close()
    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()