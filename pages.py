import time
from locators import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def clearForm(self, form):
        inputs = form.find_elements(By.XPATH, ".//input")
        for input_field in inputs:
            try:
                input_field.clear()
            except:
                # Input is probably not editable, doesn't need to be cleared anyway
                continue

class HomePage(BasePage):
    def title_matches(self):
        return "FitConnect" in self.driver.title

    def click_register_button(self):
        self.driver.find_element(*HomePageLocators.REGISTER_BUTTON).click()

    def click_login_button(self):
        self.driver.find_element(*HomePageLocators.LOGIN_BUTTON).click()

    # Make a function to login for use in other tests
    def login(self, email, password):
        self.click_login_button()
        self.driver.find_element(*FormLocators.TEXT_INPUT("Email Address")).send_keys(email)
        self.driver.find_element(*FormLocators.TEXT_INPUT("Password")).send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Just registration form, for testing
    def fill_registration_form(self, email='', first_name='', last_name='', gender=None, date='', password='', repeat_password=None):
        form = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
        self.clearForm(form)
        self.driver.find_element(*FormLocators.TEXT_INPUT("Email Address")).send_keys(email)
        self.driver.find_element(*FormLocators.TEXT_INPUT("First Name")).send_keys(first_name)
        self.driver.find_element(*FormLocators.TEXT_INPUT("Last Name")).send_keys(last_name)
        if gender is not None:
            self.driver.find_element(*FormLocators.SELECT_INPUT("Gender")).click()
            self.driver.find_element(*FormLocators.SELECT_OPTION(gender)).click()

        # Wait for popup menu to go away since waiting for button to be clickable is inconsistent
        self.wait.until(
            EC.invisibility_of_element_located((By.ID, "menu-"))
        )
        date_field = self.driver.find_element(*FormLocators.TEXT_INPUT("Date of Birth"))
        date_field.click()
        date_field.send_keys(date)
        if repeat_password is None:
            repeat_password = password
        self.driver.find_element(*FormLocators.TEXT_INPUT("Password")).send_keys(password)
        self.driver.find_element(*FormLocators.TEXT_INPUT("Repeat Password")).send_keys(repeat_password)
        self.driver.find_element(*FormLocators.CHECKBOX).click()
        self.driver.find_element(*FormLocators.NEXT_BUTTON).click()

    # Just intial survey form, for testing
    def fill_initial_survey(self, height='', weight='', goal=None):
        form = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
        self.clearForm(form)
        self.driver.find_element(*FormLocators.TEXT_INPUT("Weight (lbs)")).send_keys(weight)
        self.driver.find_element(*FormLocators.TEXT_INPUT("Height (cm)")).send_keys(height)
        if goal is not None:
            self.driver.find_element(*FormLocators.SELECT_INPUT("Goal")).click()
            self.driver.find_element(*FormLocators.SELECT_OPTION("2")).click()
            self.wait.until(
                EC.invisibility_of_element_located((By.ID, "menu-"))
            )
        self.driver.find_element(*FormLocators.NEXT_BUTTON).click()

    #Full registration flow
    def register_user(self, email='', first_name='', last_name='', gender=None, date='', password='', repeat_password=None, height='', weight='', goal=None):
        self.click_register_button()
        # Fill out first page of registration form
        self.fill_registration_form(email, first_name, last_name, gender, date, password, repeat_password)
        # Fill out Initial Survey
        self.fill_initial_survey(height, weight, goal)

        # Select User and submit
        self.driver.find_element(By.XPATH, "//button/div[text()='Client']").click()
        self.driver.find_element(*FormLocators.SUBMIT_BUTTON).click()

class Dashboard(BasePage):
    def title_matches(self):
        return "User Dashboard" in self.driver.title

    def latest_weight_is(self, weight):
        circle = self.wait.until(
                EC.visibility_of_element_located(DashboardLocators.LATEST_WEIGHT)
        )
        ActionChains(self.driver).move_to_element(circle).perform()
        value = self.driver.find_element(*DashboardLocators.GRAPH_VALUE).text
        return value == weight

    def latest_water_is(self, water):
        circle = self.wait.until(
                EC.visibility_of_element_located(DashboardLocators.LATEST_WATER)
        )
        ActionChains(self.driver).move_to_element(circle).perform()
        value = self.driver.find_element(*DashboardLocators.GRAPH_VALUE).text
        return value == water

    def latest_calorie_is(self, calories):
        circle = self.wait.until(
                EC.visibility_of_element_located(DashboardLocators.LATEST_CALORIE)
        )
        ActionChains(self.driver).move_to_element(circle).perform()
        value = self.driver.find_element(*DashboardLocators.GRAPH_VALUE).text
        return value == calories

    def latest_mood_is(self, mood):
        circle = self.wait.until(
                EC.visibility_of_element_located(DashboardLocators.LATEST_MOOD)
        )
        ActionChains(self.driver).move_to_element(circle).perform()
        value = self.driver.find_element(*DashboardLocators.GRAPH_VALUE).text
        return value == mood

    def fill_daily_survey(self, weight, water, calories, mood):
        self.driver.find_element(*FormLocators.TEXT_INPUT("Weight")).send_keys(weight)
        self.driver.find_element(*FormLocators.TEXT_INPUT("Water Amount (ml)")).send_keys(water)
        self.driver.find_element(*FormLocators.TEXT_INPUT("Calorie Amount")).send_keys(calories)
        self.driver.find_element(By.XPATH, "//button[text()='{}']".format(mood)).click()
        self.driver.find_element(*FormLocators.SUBMIT_BUTTON).click()
