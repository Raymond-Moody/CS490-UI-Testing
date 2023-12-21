import time
import os
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import pages
from locators import *

SITE_URL = "http://localhost:3000"
DB_PASSWORD = os.environ['DB_PASSWORD'] 


def clean_db():
    os.system(f"mysql --user=root --password={DB_PASSWORD} < clean_db.sql")

class HomeTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(SITE_URL)
        self.home = pages.HomePage(self.driver)
        self.wait = WebDriverWait(self.driver, 5)
        self.addCleanup(self.driver.quit)

    def test_registration_bad_inputs(self):
        self.home.click_register_button()
        self.home.fill_registration_form()
        assert "Please fill all the required (*) fields" in self.driver.page_source, "No error displayed for empty fields"
        self.home.fill_registration_form('testuser@email.com', 'testF', 'testL', 'female', '01012000', 'abc123$', 'abc123')
        assert "do not match" in self.driver.page_source, "No error displayed for mismatched passwords"

    def test_user_registeration(self):
        assert self.home.title_matches(), "Did not reach homepage"
        self.home.register_user('testuser@email.com', 'TestF', 'TestL', 'male', '01012000', 'abc123$', 'abc123$', '180', '180', '2')

        self.wait.until(
            EC.title_contains('Dashboard')
        )
        dashboard = pages.Dashboard(self.driver)
        assert dashboard.title_matches(), "Failed to reach the dashboard"

    def test_coach_registration(self):
        self.home.register_coach('testuser@email.com', 'TestF', 'TestL', 'male', '01012000', 'abc123$', 'abc123$', '180', '180', '2', '3', 'bio', 'Novice', '123')

        #TEMP
        self.wait.until(
            EC.invisibility_of_element_located(FormLocators.ROOT)
        )
        self.home.login('testuser123@gmail.com', 'password1!')
        #ENDTEMP

        self.wait.until(
            EC.title_contains('Dashboard')
        )
        dashboard = pages.Dashboard(self.driver)
        assert dashboard.title_matches(), "Failed to reach the dashboard"

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
        exercise_search_bar.send_keys('Barbell')
        assert len(self.home.exercise_results()) == 7, "Search for 'barbell' returned more than expected"
        for exercise in self.home.exercise_results():
            assert 'Barbell' in exercise or 'Renegate Row' in exercise, "A returned exercise did not match expected results for 'barbell'"
        exercise_search_bar.clear()
        exercise_search_bar.send_keys('Abdominals')
        assert len(self.home.exercise_results()) == 6, "Search for 'Abdominals' returned more than expected"

    def tearDown(self):
        self.driver.quit()
        clean_db()

class UserTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(SITE_URL)
        self.wait = WebDriverWait(self.driver, 5)
        self.home = pages.HomePage(self.driver)
        self.home.login("testuser123@gmail.com","password1!")
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
        
    def test_search_coaches(self):
        self.dashboard.goto_coaches()
        self.driver.find_element(*CoachesLocators.FILTER_BUTTON).click()
        coach_page = pages.CoachesPage(self.driver)
        coach_page.filter(exp='2', goal='Increase Stamina')
        results = coach_page.results()
        assert coach_page.experience_matches('Intermediate', results), "Returned coach had wrong experience level"
        assert coach_page.goal_matches('Increase Stamina', results), "Returned coach had wrong specialization"
        coach_page.filter(min_cost='248.50', max_cost='248.50')
        assert coach_page.cost_matches('248.50', coach_page.results()), "Returned coach had wrong cost"
        coach_page.filter(name='abcdef')
        assert not coach_page.results(), "Should not have found any coaches with name abcdef"

    def test_request_coach_and_accept_client(self):
        self.dashboard.goto_coaches()
        # Request the first coach in the results
        self.wait.until(
            EC.element_to_be_clickable(CoachesLocators.MORE_BUTTON)
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(CoachesLocators.REQUEST_BUTTON)
        ).click()
        alert = self.wait.until(
            EC.visibility_of_element_located(CoachesLocators.ALERT)
        )
        assert 'successfully' in alert.text, "Coach was not requested"
        # Request the same coach again
        self.wait.until(
            EC.element_to_be_clickable(CoachesLocators.REQUEST_BUTTON)
        ).click()
        alert = self.wait.until(
            EC.visibility_of_element_located(CoachesLocators.ALERT)
        )
        assert 'Failed' in alert.text, "User should not be able to request a second coach"

        # Test that a coach can accept a request
        self.dashboard.logout()
        self.driver.get(SITE_URL)
        self.home.login('henryeugeneprice34@outlook.com', 'password1!')
        self.dashboard.goto_requests()
        assert 'Test' in self.driver.page_source and 'User' in self.driver.page_source, "Client request did not go through"
        self.driver.find_element(By.XPATH, "//button[text()='Accept']").click()
        self.dashboard.goto_clients()
        assert 'testuser123@gmail.com' in self.driver.page_source, "Test user did not show up in clients tab"

    def test_create_and_edit_workout_plan(self):
        self.dashboard.goto_plans()
        plan_page = pages.PlansPage(self.driver)
        # Create Plan
        self.driver.find_element(*WorkoutPlanLocators.CREATE_PLAN).click()
        self.wait.until(
            EC.visibility_of_element_located(FormLocators.TEXT_INPUT('Plan Title'))
        ).send_keys('abc')
        plan_page.add_exercise('Barbell Curl')
        self.driver.find_element(*WorkoutPlanLocators.SAVE_PLAN).click()
        plans = self.driver.find_elements(*WorkoutPlanLocators.PLAN_LIST)
        assert plan_page.plan_list_contains(plans, 'abc'), "Plan was not made"
        plan_page.select_plan('abc')
        assert plan_page.selected_plan_contains('Barbell Curl'), "Plan did not include an exercise"

        # Edit Plan
        plan_page.select_plan('abc')
        self.driver.find_element(*WorkoutPlanLocators.EDIT_PLAN).click()
        plan_page.add_exercise('Crunches')
        self.driver.find_element(*WorkoutPlanLocators.UPDATE_PLAN).click()
        time.sleep(0.5)
        plan_page.select_plan('abc')
        assert plan_page.selected_plan_contains('Crunches'), "Plan did not add exercise"

    def tearDown(self):
        self.driver.quit()
        clean_db()

class CoachTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(SITE_URL)
        self.wait = WebDriverWait(self.driver, 5)
        self.home = pages.HomePage(self.driver)
        # Make test user have a coach, since their db data gets wiped every time
        self.home.login("testuser123@gmail.com","password1!")
        self.dashboard = pages.Dashboard(self.driver)
        self.addCleanup(self.driver.quit)
        self.dashboard.goto_coaches()
        coaches_page = pages.CoachesPage(self.driver)
        coaches_page.filter(name='Henry')
        self.wait.until(
            EC.element_to_be_clickable(CoachesLocators.MORE_BUTTON)
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(CoachesLocators.REQUEST_BUTTON)
        ).click()

        self.dashboard.logout()
        self.driver.get(SITE_URL)
        self.home.login('henryeugeneprice34@outlook.com', 'password1!')
        self.dashboard.goto_requests()
        self.driver.find_element(By.XPATH, "//button[text()='Accept']").click()
        self.dashboard.goto_home()

    def test_view_client_dashboard(self):
        self.dashboard.goto_clients()
        self.driver.find_element(*ClientsLocators.TEST_USER).click()
        self.driver.find_element(*ClientsLocators.VIEW_INFO).click()
        assert 'Test' in self.driver.page_source
        assert "'s - Client Info" in self.driver.page_source, "Did not reach client's dashboard"

    def test_create_client_workout_plan(self):
        self.dashboard.goto_clients()
        self.driver.find_element(*ClientsLocators.TEST_USER).click()
        self.driver.find_element(*ClientsLocators.CLIENT_WORKOUTS).click()
        plan_page = pages.PlansPage(self.driver)
        self.driver.refresh()
        time.sleep(1)
        # Create Plan
        self.driver.find_element(*WorkoutPlanLocators.CREATE_PLAN).click()
        self.wait.until(
            EC.visibility_of_element_located(FormLocators.TEXT_INPUT('Plan Title'))
        ).send_keys('def')
        plan_page.add_exercise('Barbell Curl')
        self.driver.find_element(*WorkoutPlanLocators.SAVE_PLAN).click()
        plans = self.driver.find_elements(*WorkoutPlanLocators.PLAN_LIST)
        assert plan_page.plan_list_contains(plans, 'def'), "Plan was not made"
        plan_page.select_plan('def')
        assert plan_page.selected_plan_contains('Barbell Curl'), "Plan did not include an exercise"

    def tearDown(self):
        self.driver.quit()
        clean_db()


if __name__ == "__main__":
    unittest.main()
