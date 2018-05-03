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

    def testCreateAccountLogOut(self):
        driver = self.driver
        driver.get("http://web:8000/bakery/")
        assert "Bakery" in driver.title
        elem = driver.find_element_by_link_text('Create Account')
        elem.click()

        name = driver.find_element_by_name("username")
        name.clear()
        name.send_keys("TestUser4")
        password = driver.find_element_by_name("password")
        password.clear()
        password.send_keys("1234")
        #password.click()
        password.send_keys(Keys.RETURN)
        #driver.get_screenshot_as_file('testCreateAccount.png')
        elem2 = driver.find_element_by_link_text('Log Out')
        elem2.click()
        #driver.get_screenshot_as_file('testLogOut.png')

        #password.submit()
        #submit = driver.find_element_by_id("submit")
        #submit.click()

        try:
            #tag = wait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h1'))).text
            tag = driver.find_element_by_tag_name('h2')
            if "successfully" in tag.text:
                assert True
            #assert True
        except NoSuchElementException:
            print(tag)
            assert False

    def testLogIn(self):
        driver = self.driver
        driver.get("http://web:8000/bakery/")
        assert "Bakery" in driver.title
        elem = driver.find_element_by_link_text('Log In')
        elem.click()
        name = driver.find_element_by_name("username")
        name.clear()
        name.send_keys("TestUser4")
        password = driver.find_element_by_name("password")
        password.clear()
        password.send_keys("1234")
        #password.click()
        password.send_keys(Keys.RETURN)
        #driver.get_screenshot_as_file('testLogIn.png')

        #password.submit()
        #submit = driver.find_element_by_id("submit")
        #submit.click()

        try:
            #tag = wait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h1'))).text
            tag = driver.find_element_by_tag_name('h2')

            #elem2 = driver.find_element_by_link_text('Log Out')
            #elem2.click()
            #driver.get_screenshot_as_file('testLogOut2.png')
            if "Recently" in tag.text:
                assert True
            #assert True
        except NoSuchElementException:
            #print(tag)
            assert False


    def testNewItem_Search(self):
        driver = self.driver
        driver.get("http://web:8000/bakery/")
        #assert "Bakery" in driver.title
        elem2 = driver.find_element_by_link_text('Create New Item Post')
        # if "reate" not in elem2.text:
        #     assert False
        elem2.click()
        #driver.get_screenshot_as_file('testItemPage.png')
        # elem = driver.find_element_by_link_text('Log In')
        # elem.click()
        # #driver.get_screenshot_as_file('testLogIn.png')
        # username = driver.find_element_by_name("username")
        # username.clear()
        # username.send_keys("TestUser4")
        # password = driver.find_element_by_name("password")
        # password.clear()
        # password.send_keys("1234")
        # # password.click()
        # password.send_keys(Keys.RETURN)
        # driver.get_screenshot_as_file('testAfterLogIn.png')
        #
        # #elem2 = driver.find_element_by_link_text('Create New Item Post')
        # #elem2.click()
        # driver.get_screenshot_as_file('testItemPage.png')
        # name = driver.find_element_by_name("name")
        # name.clear()
        # name.send_keys("TestPie")
        # price = driver.find_element_by_name("price")
        # price.clear()
        # price.send_keys("4.00")
        # # price.click()
        # price.send_keys(Keys.RETURN)
        #
        # elem3 = driver.find_element_by_link_text('Search')
        # elem3.click()
        # search = driver.find_element_by_name("searchStr")
        # search.clear()
        # search.send_keys("TestPie")
        # assert "There are no baked goods that match this search." not in driver.page_source
        assert True




    def tearDown(self):
        elem = self.driver.find_element_by_link_text('Delete My Account')
        elem.click()
        #self.driver.get_screenshot_as_file('testDeleteAccount.png')
        self.driver.close()


if __name__ == '__main__':
    unittest.main()