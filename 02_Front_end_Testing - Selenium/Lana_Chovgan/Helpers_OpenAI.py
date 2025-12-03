import time
#import self
from selenium.webdriver.common.by import By


def Safety_Link(driver):
    driver.get("https://openai.com/safety/")
    time.sleep(4)

def switch_window(driver):
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)

def API_log_in(driver):
    driver.find_element(By.XPATH, "//a[@href='https://platform.openai.com/login']").click()
    time.sleep(3)

def continue_button(driver):
        driver.find_element(By.XPATH, "//button[normalize-space()='Continue']")


