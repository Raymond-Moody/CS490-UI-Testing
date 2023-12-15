from selenium.webdriver.common.by import By

class FormLocators(object):
    CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Next']")
    ROOT = (By.CLASS_NAME, "MuiModal-root")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Submit']")

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
    DAILY_SURVEY_BUTTON = (By.XPATH, "//button[text()='Fill Survey']")
    GRAPH_VALUE = (By.CSS_SELECTOR, "span.recharts-tooltip-item-value")

    #LATEST_WEIGHT = (By.XPATH, "//h6[text()='Weight Tracker']/following-sibling::div[1]//circle[last()]")
    #LATEST_WEIGHT = (By.XPATH, "//h6[text()='Weight Tracker']/following-sibling::div[1]/div[1]")
    LATEST_WEIGHT = (By.XPATH, "//h6[text()='Weight Tracker']/following-sibling::div[1]")
    LATEST_WATER = (By.XPATH, "//h6[text()='Water Intake']/following-sibling::div[1]")
    LATEST_CALORIE = (By.XPATH, "//h6[text()='Calorie Tracker']/following-sibling::div[1]")
    LATEST_MOOD = (By.XPATH, "//h6[text()='Mood Tracker']/following-sibling::div[1]")

class WorkoutPlanLocators(object):
    pass
