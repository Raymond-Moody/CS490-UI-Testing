import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pages
from locators import *

SITE_URL = "http://localhost:3000"

class HomeTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(SITE_URL)
        self.addCleanup(self.driver.quit)

    def test_registration_bad_inputs(self):
        home = pages.HomePage(self.driver)
        home.click_register_button()
        home.fill_registration_form()
        assert "Please fill all the required (*) fields" in self.driver.page_source, "No error displayed for empty fields"
        home.fill_registration_form('test@email.net', 'testF', 'testL', 'female', '01012000', 'abc123$', 'abc123')
        assert "do not match" in self.driver.page_source, "No error displayed for mismatched passwords"
        home.fill_registration_form('test@', 'testF', 'testL', 'female', '01012000', 'abc123$', 'abc123$')
        # Placeholder error message expected
        assert "Please enter a valid email" in self.driver.page_source, "No error displayed for invalid email"
        home.fill_registration_form('test@', 'testF', 'testL', 'female', '01012000', 'abc123$', 'abc123$')
        # Placeholder error message expected
        assert "Password must contain" in self.driver.page_source, "No error displayed for invalid password"

    def test_user_registeration_login(self):
        """
        Creates a new user
        Assertions need to be added to actual test that stuff happens correctly
        """
        home = pages.HomePage(self.driver)
        assert home.is_title_matches(), "Did not reach homepage"
        home.register_user('testuser@email.com', 'TestF', 'TestL', 'male', '01012000', 'abc123$', 'abc123$', '180', '180', '2')

        # Log in after user is created
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(FormLocators.ROOT)
        )
        home.login("testuser@email.com", "abc123$")
        WebDriverWait(self.driver, 10).until(
            EC.title_contains('Dashboard')
        )
        dashboard = pages.Dashboard(self.driver)
        # We reached 'FitConnect - User Dashboard' successfully -> we registered and logged in successfully
        assert dashboard.is_title_matches(), "Failed to reach the dashboard"

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
