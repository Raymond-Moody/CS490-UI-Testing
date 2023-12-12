import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Firefox()
browser.get('localhost:3000/')

try:
    #element = browser.find_element(by=By.XPATH, value="//button[text()='Register']")
    #Click Register
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Register']"))
    )
    element.click()

    #Find the email entry field
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "mui-4"))
    )
    element.send_keys("testuser1@email.com")

    #We know the form is loaded, so just grab the rest without waiting
    browser.find_element(by=By.ID, value="mui-5").send_keys("First")
    browser.find_element(by=By.ID, value="mui-6").send_keys("Last")
    browser.find_element(by=By.CLASS_NAME, value="MuiSelect-select").click()
    browser.find_element(by=By.CSS_SELECTOR, value="li[data-value='male']").click()
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "mui-8"))
    )
    element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "mui-8"))
    )
    #element = browser.find_element(by=By.ID, value="mui-8")
    element.click()
    element.send_keys("01012000")
    browser.find_element(by=By.ID, value="mui-9").send_keys("abc123$")
    browser.find_element(by=By.ID, value="mui-10").send_keys("abc123$")
    browser.find_element(by=By.CSS_SELECTOR, value="input[type='checkbox']").click()
    browser.find_element(by=By.XPATH, value="//button[text()='Next']").click()

    #Fill out initial survey
    browser.find_element(by=By.ID, value='mui-4').send_keys(150)
    browser.find_element(by=By.ID, value='mui-5').send_keys(175)
    browser.find_element(by=By.CLASS_NAME, value="MuiSelect-select").click()
    browser.find_element(by=By.CSS_SELECTOR, value="li[data-value='1']").click()
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
    )
    element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Next']"))
    )
    time.sleep(1)
    element.click()
except Exception as e:
    print(e)
    browser.quit()
