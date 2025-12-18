from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException
import time

url_main = "https://openai.com/"
url_company = "https://openai.com/about"

def delay(seconds=1):
    time.sleep(seconds)

def take_screenshot(driver, filename="screenshot.png"):
    driver.save_screenshot(filename)

def assert_element_visible(driver, xpath, description="element"):
  # Checks that element is displayed
    try:
        element = driver.find_element(By.XPATH, xpath)
        assert element.is_displayed()
        print(f"{description} is displayed")
        return True
    except NoSuchElementException:
        print(f"{description} is not displayed")
        take_screenshot(driver)
        return False
    except AssertionError:
        print(f"Something is wrong with {description}")
        take_screenshot(driver)
        return False

def assert_element_text_equals(driver, xpath, expected_text, description="element"):
# Checks element is equal
    try:
        element = driver.find_element(By.XPATH, xpath)
        actual_text = element.text.strip()
        assert expected_text in actual_text, f"Expected '{expected_text}', got '{actual_text}'"
        print(f"{expected_text} is in {description}'s text")
        return True
    except AssertionError:
        print(f"{expected_text} is not in {description}'s text")
        take_screenshot(driver)
        return False

def click_and_verify(driver, click_xpath, url_contains, text_xpath, expected_text, description="link"):

    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, click_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        try:
            element.click()
        except Exception:
            driver.execute_script("arguments[0].click();", element)

        WebDriverWait(driver, 10).until(EC.url_contains(url_contains))

        assert_element_text_equals(driver, text_xpath, expected_text, description)
        print(f"{description} leads to correct page")
        driver.back()
        return True
    except AssertionError:
        print(f"{description} leads to incorrect page")
        take_screenshot(driver)
        return False