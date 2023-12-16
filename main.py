import os
import sys
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import pages
from locators import *

SITE_URL = "http://localhost:3000"
DB_PASSWORD = sys.argv[1]

def clean_db():
    os.system("mysql --user=root --password={} < clean_db.sql".format(DB_PASSWORD))

class HomeTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(SITE_URL)
        self.home = pages.HomePage(self.driver)
        self.wait = WebDriverWait(self.driver, 10)
        self.addCleanup(self.driver.quit)

    def test_registration_bad_inputs(self):
        self.home.click_register_button()
        self.home.fill_registration_form()
        assert "Please fill all the required (*) fields" in self.driver.page_source, "No error displayed for empty fields"
        self.home.fill_registration_form('testuser@email.com', 'testF', 'testL', 'female', '01012000', 'abc123$', 'abc123')
        assert "do not match" in self.driver.page_source, "No error displayed for mismatched passwords"

        """
        self.home.fill_registration_form('testuser@', 'testF', 'testL', 'female', '01012000', 'abc123$', 'abc123$')
        # Placeholder error message expected
        assert "Please enter a valid email" in self.driver.page_source, "No error displayed for invalid email"
        self.home.fill_registration_form('testuser@email.com', 'testF', 'testL', 'female', '01012000', 'abc123', 'abc123')
        # Placeholder error message expected
        assert "Password must contain" in self.driver.page_source, "No error displayed for invalid password"
        """

    def test_user_registeration_login(self):
        assert self.home.title_matches(), "Did not reach homepage"
        self.home.register_user('testuser@email.com', 'TestF', 'TestL', 'male', '01012000', 'abc123$', 'abc123$', '180', '180', '2')

        # Log in after user is created
        self.wait.until(
            EC.invisibility_of_element_located(FormLocators.ROOT)
        )
        self.home.login("testuser@email.com", "abc123$")
        self.wait.until(
            EC.title_contains('Dashboard')
        )
        dashboard = pages.Dashboard(self.driver)
        # We reached 'FitConnect - User Dashboard' successfully -> we registered and logged in successfully
        assert dashboard.title_matches(), "Failed to reach the dashboard"

    def test_coach_registration_login(self):
        assert True

    def test_exercise_bank(self):
        # Scroll to exercise bank
        exercise_search_bar = self.wait.until(
                EC.presence_of_element_located(HomePageLocators.EXERCISE_SEARCH)
        )
        self.driver.execute_script("arguments[0].scrollIntoView()", exercise_search_bar)
        # Checking that exercise bank is populated with a full page
        self.wait.until(
            EC.visibility_of_element_located(HomePageLocators.EXERCISE_RESULT)
        )
        assert len(self.home.exercise_results()) == 14, "Exercise bank was not populated"

        # Check that we can search for exercises. 
        exercise_search_bar.send_keys('Crunch')
        assert len(self.home.exercise_results()) == 2, "Search for 'crunch' returned more than expected"
        for exercise in self.home.exercise_results():
            assert 'Crunch' in exercise, "A returned exercise did not contain the search term"

    def tearDown(self):
        self.driver.quit()
        clean_db()

class UserDashboardTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(SITE_URL)
        self.wait = WebDriverWait(self.driver, 10)
        home = pages.HomePage(self.driver)
        home.login("testuser123@email.com","password1!")
        self.dashboard = pages.Dashboard(self.driver)
        self.addCleanup(self.driver.quit)

    def test_daily_survey_and_graphs(self):
        self.wait.until(
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
        clean_db()

if __name__ == "__main__":
    DB_PASSWORD = sys.argv.pop()
    unittest.main()
