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
        self.driver.find_element(*HomePageLocators.REGISTER_BUTTON).click()

    # Make a function to login for use in other tests

class Dashboard(BasePage):
    def is_title_matches(self):
        return "User Dashboard" in self.driver.title
