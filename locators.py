from selenium.webdriver.common.by import By

class FormLocators(object):
    CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Next']")

    def TEXT_INPUT(label):
        return (By.XPATH, "//label[contains(.,'{}')]/following-sibling::div[1]/input".format(label))

    def SELECT_INPUT(label):
        return (By.XPATH, "//label[contains(.,'{}')]/following-sibling::div[1]/div".format(label))
    
    def SELECT_OPTION(value):
        return (By.CSS_SELECTOR, "li[data-value='{}']".format(value))

class HomePageLocators(object):
    REGISTER_BUTTON = (By.XPATH, "//button[text()='Register']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Login']")

class DashboardLocators(object):
    pass

class WorkoutPlanLocators(object):
    pass
