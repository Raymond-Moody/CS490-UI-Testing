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
    EXERCISE_SEARCH = (By.XPATH, "//label[text()='Find an exercise']/following-sibling::div[1]/input")
    EXERCISE_RESULT = (By.XPATH, "//div[contains(@class, 'exerciseBox')]/h6")

class DashboardLocators(object):
    DAILY_SURVEY_BUTTON = (By.XPATH, "//button[text()='Fill Survey']")
    GRAPH_VALUE = (By.CSS_SELECTOR, "span.recharts-tooltip-item-value")

    LATEST_WEIGHT = (By.XPATH, "//h6[text()='Weight Tracker']/following-sibling::div[1]")
    LATEST_WATER = (By.XPATH, "//h6[text()='Water Intake']/following-sibling::div[1]")
    LATEST_CALORIE = (By.XPATH, "//h6[text()='Calorie Tracker']/following-sibling::div[1]")
    LATEST_MOOD = (By.XPATH, "//h6[text()='Mood Tracker']/following-sibling::div[1]")

    HOME_TAB = (By.CSS_SELECTOR, "a[href='/c/dashboard'] > div")
    COACHES_TAB = (By.CSS_SELECTOR, "a[href='/c/coaches'] > div")
    PLANS_TAB = (By.CSS_SELECTOR, "a[href='/c/workoutplan'] > div")
    REQUESTS_TAB = (By.CSS_SELECTOR, "a[href='/c/my-requests'] > div")
    CLIENTS_TAB = (By.CSS_SELECTOR, "a[href='/c/my-clients'] > div")

class WorkoutPlanLocators(object):
    CREATE_PLAN = (By.XPATH, "//button[text()='Create New Plan']")
    SAVE_PLAN = (By.XPATH, "//button[text()='Save Plan']")
    EDIT_PLAN = (By.XPATH, "//button[text()='Edit Plan']")
    UPDATE_PLAN = (By.XPATH, "//button[text()='Update Plan']")
    ADD_EXERCISE = (By.XPATH, "//button/h6[text()='Add Exercise']")
    CONFIRM_EXERCISE = (By.XPATH, "//button[text()='Add Exercise']")
    CONFIRM_EXERCISE_DATA = (By.CSS_SELECTOR, "svg[data-testid='CheckIcon']")
    PLAN_LIST = (By.XPATH, "//h6[text()='Your Workout plans']/following-sibling::ul[1]/div")
    #PLAN_IN_LIST = (By.XPATH, "//h6[text()='Your Workout Plans']/following-sibling::ul[1]/div")
    EXERCISE_IN_PLAN = (By.XPATH, "//div[contains(@class, 'ReadWorkoutPlan-toolbar')]/h6")

    def PLAN_IN_LIST(title):
        return (By.XPATH, "//div[text()='{}']".format(title))

class CoachesLocators(object):
    REQUEST_BUTTON = (By.XPATH, "//button[text()='Request Coach']")
    MESSAGE_BUTTON = (By.XPATH, "//button[text()='Message Coach']")
    MORE_BUTTON = (By.XPATH, "//p[text()='More Options']")
    FILTER_BUTTON = (By.XPATH, "//p[text()='Advanced Filters']")
    ALERT = (By.CSS_SELECTOR, ".MuiAlert-message")
    COACH_PROFILE = (By.CSS_SELECTOR, ".MuiCard-root")

class ClientsLocators(object):
    TEST_USER = (By.XPATH, "//button//h2[contains(text(), 'Test')]")
    VIEW_INFO = (By.XPATH, "//button[text()='View Client Info']")
    CLIENT_WORKOUTS = (By.XPATH, "//button[text()='Client Workout Info']")
