import unittest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MilaS.helpers import element_helpers as h
fake = Faker()
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class ChromePositiveTestCases(unittest.TestCase):

    def setUp(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.driver.execute_script("document.body.style.zoom='70%'")

    def test_1_invalid_parameters(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 4).until(EC.url_contains("https://openai.com/about/"))
        h.delay()
        driver.get(
            "https://openai.com/about/?foo=bar&undefined_param=123&%ZZ=@@@&debug=true&null=&injection=<script>alert(1)</script>")

        print("----------------------test1-------------------------")

        try:
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'text-h1')]"))
            )
            assert element.is_displayed()
            print("Current url ", driver.current_url)
            print("Links opens with invalid parameters")
        except TimeoutException:
            print("Timed out waiting for h1 element")
        except NoSuchElementException:
            print("No elements found")
        except AssertionError:
            print("Link doesn't open with invalid parameters")

    def test_2_Small_Resolutions(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 4).until(EC.url_contains("openai.com/about/"))
        h.delay()
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=320,240")
        print("----------------------test2-------------------------")

        h.assert_element_visible(driver, "//*[@id='main']/div/div[2]/div/div/div/div[1]/h3", "title")
        print("title is visible")
        h.assert_element_visible(driver, "//*[@id='main']/div/section[1]/div/div/div[1]/div[1]/div/h2", "news")
        print("news is visible")
        h.assert_element_visible(driver, "//*[@id='main']/div/section[1]/div/div/div[2]/div[1]/div/h2", "product")
        print("product is visible")
        h.take_screenshot(driver)


    def test_3_Mistake_in_URL(self):
        driver = self.driver
        driver.get("https://openai.com/aboutabout")
        h.delay()
        print("----------------------test3-------------------------")
        h.assert_element_text_equals(driver,"//body//div[@class='duration-sidebar ease-curve-sidebar grid transition-[grid-template-columns] grid-cols-[0_1fr] md:grid-cols-[0_theme(spacing.nav-width)_1fr]']//p[1]","Error light blinks once", "error message"
        )

    def test_4_Large_Resolutions(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 4).until(EC.url_contains("openai.com/about/"))
        h.delay()
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=3840,2160")
        print("----------------------test4-------------------------")
        h.take_screenshot(driver)

        h.assert_element_visible(driver, "//*[@id='main']/div/div[2]/div/div/div/div[1]/h3", "title")
        print("title is visible")
        h.assert_element_visible(driver, "//*[@id='main']/div/section[1]/div/div/div[1]/div[1]/div/h2", "news")
        print("news is visible")
        h.assert_element_visible(driver, "//*[@id='main']/div/section[1]/div/div/div[2]/div[1]/div/h2", "product")
        print("product is visible")

class EdgeNegativeTestCases(unittest.TestCase):

    def setUp(self):
        os.environ["SE_DRIVER_MIRROR_URL"] = "https://msedgedriver.microsoft.com"
        options = webdriver.EdgeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Edge(options=options)
        self.driver.execute_script("document.body.style.zoom='70%'")

    def test_1_invalid_parameters(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 4).until(EC.url_contains("https://openai.com/about/"))
        h.delay()
        driver.get(
            "https://openai.com/about/?foo=bar&undefined_param=123&%ZZ=@@@&debug=true&null=&injection=<script>alert(1)</script>")

        print("----------------------test1-------------------------")

        try:
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h1[contains(@class,'text-h1')]"))
            )
            assert element.is_displayed()
            print("Current url ", driver.current_url)
            print("Links opens with invalid parameters")
        except TimeoutException:
            print("Timed out waiting for h1 element")
        except NoSuchElementException:
            print("No elements found")
        except AssertionError:
            print("Link doesn't open with invalid parameters")

    def test_2_Small_Resolutions(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 4).until(EC.url_contains("openai.com/about/"))
        h.delay()
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=320,240")
        print("----------------------test2-------------------------")

        h.assert_element_visible(driver, "//*[@id='main']/div/div[2]/div/div/div/div[1]/h3", "title")
        print("title is visible")
        h.assert_element_visible(driver, "//*[@id='main']/div/section[1]/div/div/div[1]/div[1]/div/h2", "news")
        print("news is visible")
        h.assert_element_visible(driver, "//*[@id='main']/div/section[1]/div/div/div[2]/div[1]/div/h2", "product")
        print("product is visible")
        h.take_screenshot(driver)


    def test_3_Mistake_in_URL(self):
        driver = self.driver
        driver.get("https://openai.com/aboutabout")
        h.delay()
        print("----------------------test3-------------------------")
        h.assert_element_text_equals(driver,"//body//div[@class='duration-sidebar ease-curve-sidebar grid transition-[grid-template-columns] grid-cols-[0_1fr] md:grid-cols-[0_theme(spacing.nav-width)_1fr]']//p[1]","Error light blinks once", "error message"
        )

    def test_4_Large_Resolutions(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 4).until(EC.url_contains("openai.com/about/"))
        h.delay()
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=3840,2160")
        print("----------------------test4-------------------------")
        h.take_screenshot(driver)

        h.assert_element_visible(driver, "//*[@id='main']/div/div[2]/div/div/div/div[1]/h3", "title")
        print("title is visible")
        h.assert_element_visible(driver, "//*[@id='main']/div/section[1]/div/div/div[1]/div[1]/div/h2", "news")
        print("news is visible")
        h.assert_element_visible(driver, "//*[@id='main']/div/section[1]/div/div/div[2]/div[1]/div/h2", "product")
        print("product is visible")

    def tearDown(self):
        self.driver.quit()