from locators import *
from element import BasePageElement

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class HomePage(BasePage):
    def is_title_matches(self):
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

class Dashboard(BasePage):
    def is_title_matches(self):
        return "User Dashboard" in self.driver.title
