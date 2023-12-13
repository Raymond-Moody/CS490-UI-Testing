import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pages
from locators import *

SITE_URL = "http://localhost:3000/"

class HomeTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(SITE_URL)
        self.addCleanup(self.driver.quit)

    def test_user_registeration_login(self):
        """
        Creates a new user
        Assertions need to be added to actual test that stuff happens correctly
        """
        home = pages.HomePage(self.driver)
        assert home.is_title_matches()
        home.click_register_button()
        # Fill out first page of registration form
        self.driver.find_element(*FormLocators.TEXT_INPUT("Email Address")).send_keys("testuser@email.com")
        self.driver.find_element(*FormLocators.TEXT_INPUT("First Name")).send_keys("TestF")
        self.driver.find_element(*FormLocators.TEXT_INPUT("Last Name")).send_keys("TestL")
        self.driver.find_element(*FormLocators.SELECT_INPUT("Gender")).click()
        self.driver.find_element(*FormLocators.SELECT_OPTION("male")).click()
        # Wait for popup menu to go away since waiting for button to be clickable is inconsistent
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "menu-"))
        )
        date = self.driver.find_element(*FormLocators.TEXT_INPUT("Date of Birth"))
        date.click()
        date.send_keys("01012000")
        self.driver.find_element(*FormLocators.TEXT_INPUT("Password")).send_keys("abc123$")
        self.driver.find_element(*FormLocators.TEXT_INPUT("Repeat Password")).send_keys("abc123$")
        self.driver.find_element(*FormLocators.CHECKBOX).click()
        self.driver.find_element(*FormLocators.NEXT_BUTTON).click()

        # Fill out Initial Survey
        self.driver.find_element(*FormLocators.TEXT_INPUT("Weight (lbs)")).send_keys("150")
        self.driver.find_element(*FormLocators.TEXT_INPUT("Height (cm)")).send_keys("175")
        self.driver.find_element(*FormLocators.SELECT_INPUT("Goal")).click()
        self.driver.find_element(*FormLocators.SELECT_OPTION("2")).click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "menu-"))
        )
        self.driver.find_element(*FormLocators.NEXT_BUTTON).click()

        # Select User and submit
        self.driver.find_element(By.XPATH, "//button/div[text()='Client']").click()
        self.driver.find_element(By.XPATH, "//button[text()='Submit']").click()

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(FormLocators.ROOT)
        )
        home.login("testuser@email.com", "abc123$")
        WebDriverWait(self.driver, 10).until(
            EC.title_contains('Dashboard')
        )
        dashboard = pages.Dashboard(self.driver)
        # We reached 'FitConnect - User Dashboard' successfully -> we registered and logged in successfully
        assert dashboard.is_title_matches()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
