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
        self.home = pages.HomePage(self.driver)
        self.addCleanup(self.driver.quit)

    def test_registration_bad_inputs(self):
        self.home.click_register_button()
        self.home.fill_registration_form()
        assert "Please fill all the required (*) fields" in self.driver.page_source, "No error displayed for empty fields"
        self.home.fill_registration_form('test@email.net', 'testF', 'testL', 'female', '01012000', 'abc123$', 'abc123')
        assert "do not match" in self.driver.page_source, "No error displayed for mismatched passwords"
        self.home.fill_registration_form('test@', 'testF', 'testL', 'female', '01012000', 'abc123$', 'abc123$')
        # Placeholder error message expected
        assert "Please enter a valid email" in self.driver.page_source, "No error displayed for invalid email"
        self.home.fill_registration_form('test@mail.com', 'testF', 'testL', 'female', '01012000', 'abc123', 'abc123')
        # Placeholder error message expected
        assert "Password must contain" in self.driver.page_source, "No error displayed for invalid password"

    def test_user_registeration_login(self):
        """
        Creates a new user
        Assertions need to be added to actual test that stuff happens correctly
        """
        assert self.home.title_matches(), "Did not reach homepage"
        self.home.register_user('testuser@email.com', 'TestF', 'TestL', 'male', '01012000', 'abc123$', 'abc123$', '180', '180', '2')

        # Log in after user is created
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(FormLocators.ROOT)
        )
        self.home.login("testuser@email.com", "abc123$")
        WebDriverWait(self.driver, 10).until(
            EC.title_contains('Dashboard')
        )
        dashboard = pages.Dashboard(self.driver)
        # We reached 'FitConnect - User Dashboard' successfully -> we registered and logged in successfully
        assert dashboard.title_matches(), "Failed to reach the dashboard"

    def tearDown(self):
        self.driver.quit()

class DashboardTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(SITE_URL)
        home = pages.HomePage(self.driver)
        home.login("testuser123@gmail.com","password1!")
        self.dashboard = pages.Dashboard(self.driver)
        self.addCleanup(self.driver.quit)

    def test_daily_survey_and_graphs(self):
        WebDriverWait(self.driver, 10).until(
            EC.title_contains('Dashboard')
        )
        assert self.dashboard.title_matches(), "Failed to reach dashboard"
        self.driver.find_element(*DashboardLocators.DAILY_SURVEY_BUTTON).click()
        self.dashboard.fill_daily_survey('200','1500','2300','Neutral')
        assert self.dashboard.latest_weight_is('200'), "New weight was not graphed."
        assert self.dashboard.latest_water_is('1500'), "New water was not graphed"
        assert self.dashboard.latest_calorie_is('2300'), "New calorie was not graphed"
        assert self.dashboard.latest_mood_is('0'), "New mood was not graphed"
        
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
