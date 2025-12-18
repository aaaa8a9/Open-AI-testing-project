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
from selenium.webdriver.edge.options import Options as Edge_Options



class ChromePositiveTestCases(unittest.TestCase):

    def setUp(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.driver.execute_script("document.body.style.zoom='70%'")

    def test_1_correct_page(self):
        driver = self.driver
        driver.get(h.url_main)
        WebDriverWait(driver, 2).until(EC.url_contains("openai.com"))
        h.delay()
        print("----------------------test1-------------------------")

        try:
            assert driver.find_element(By.XPATH, "//a[normalize-space()='Company']").is_displayed()
            assert driver.find_element(By.XPATH, "//a[normalize-space()='Company']").is_enabled()
            print("Company is displayed and enabled")
        except AssertionError:
            print("Company tab is not found")

    def test_2_Plan_and_Charter(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 2).until(EC.url_contains("openai.com/about/"))
        h.delay()
        print("----------------------test2-------------------------")

        h.assert_element_visible(driver, "//h3[normalize-space()='Our vision for the future of AGI']", "Header")
        h.assert_element_text_equals(driver, "//h3[normalize-space()='Our vision for the future of AGI']", "Our vision for the future of AGI", "Header")

        h.assert_element_visible(driver, "//a[normalize-space()='Our plan for AGI']", "Our plan for AGI button")
        h.assert_element_visible(driver, "//a[normalize-space()='Our Charter']", "Our Charter button")

        h.click_and_verify(driver, "//a[normalize-space()='Our Charter']", "charter", "//h1", "Our Charter", "Charter button")
        h.click_and_verify(driver, "//a[normalize-space()='Our plan for AGI']", "planning-for-agi-and-beyond", "//h1", "Our plan for AGI", "AGI button")

    def test_3_Latest_News(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 5).until(EC.url_contains("openai.com/about/"))
        h.delay()
        print("----------------------test3-------------------------")

        h.assert_element_visible(driver, "//h2[normalize-space()='Latest news']", "Latest news section")

        # 1st news Sora
        h.assert_element_visible(driver, "//section[1]", "1st news picture")
        h.assert_element_text_equals(driver, "//div[contains(@class,'text-h5')]", "Sora 2 is here", "1st news title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Sora 2')]", "sora-2", "//h1[contains(text(),'Sora 2 is here')]", "Sora 2 is here", "Sora 2")

        # 2nd news Parental controls
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Introducing parental controls')]//div[contains(@class,'text-h5')]", "2nd news title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Introducing parental controls')]//div[contains(@class,'text-h5')]", "Introducing parental controls", "2nd news title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Introducing parental controls')]", "introducing-parental-controls", "//h1[contains(text(),'Introducing parental controls')]", "Introducing parental controls", "Parental controls")

    def test_4_Our_research(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 2).until(EC.url_contains("openai.com/about/"))
        h.delay()
        print("----------------------test4-------------------------")

        # 1st research Measuring the performance
        h.assert_element_visible(driver, "//section[1]", "1st research picture")
        h.assert_element_text_equals(driver, "//div[contains(@class,'text-h5')]", "Measuring the performance", "1st research title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Measuring the performance')]", "gdpval", "//h1[contains(text(),'Measuring the performance')]", "Measuring the performance", "Measuring the performance research")

        # # 2nd research Codex
        h.assert_element_visible(driver, "//a[contains(@aria-label,'How people are using ChatGPT')]//div[contains(@class,'text-h5')]", "2nd research title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'How people are using ChatGPT')]//div[contains(@class,'text-h5')]", "How people are using ChatGPT", "2nd research title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'How people are using ChatGPT')]", "how-people-are-using-chatgpt", "//h1[contains(text(),'How people are using ChatGPT')]", "How people are using ChatGPT", "People using GPT research")

        # 3rd research Why language models hallucinate
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Why language models hallucinate')]//div[contains(@class,'text-h5')]", "3rd research title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Why language models hallucinate')]//div[contains(@class,'text-h5')]", "Why language models hallucinate", "3rd research title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Why language models hallucinate')]", "why-language-models-hallucinate", "//h1[contains(text(),'Why language models hallucinate')]", "Why language models hallucinate", "Language models research")

        # 4th research Understanding neural networks
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Understanding neural networks through sparse circuits')]//div[contains(@class,'text-h5')]", "4th research title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Understanding neural networks through sparse circuits')]//div[contains(@class,'text-h5')]", "Understanding neural networks through sparse circuits", "4th research title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Understanding neural networks through sparse circuits')]", "understanding-neural-networks-through-sparse-circuits", "//h1[contains(text(),'Understanding neural networks through sparse circuits')]", "Understanding neural networks through sparse circuits", "Neural networks research")


    def test_5_Our_products(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 2).until(EC.url_contains("openai.com/about/"))
        h.delay()
        print("----------------------test5-------------------------")

        # 1st product Sora
        h.assert_element_visible(driver, "//section[1]", "1st product picture")
        h.assert_element_text_equals(driver, "//div[contains(@class,'text-h5')]", "Sora 2 is here", "1st product title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Sora 2')]", "sora-2", "//h1[contains(text(),'Sora 2 is here')]", "Sora 2 is here", "Sora 2 product")

        # 2nd product Codex
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Introducing upgrades to Codex')]//div[contains(@class,'text-h5')]", "2nd product title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Introducing upgrades to Codex')]//div[contains(@class,'text-h5')]", "Introducing upgrades to Codex", "2nd product title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Introducing upgrades to Codex')]", "introducing-upgrades-to-codex", "//h1[contains(text(),'Introducing upgrades to Codex')]", "Introducing upgrades to Codex", "Codex product")

        # 3rd product Group chats
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Introducing group chats in ChatGPT')]//div[contains(@class,'text-h5')]", "3rd product title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Introducing group chats in ChatGPT')]//div[contains(@class,'text-h5')]", "Introducing group chats in ChatGPT", "3rd product title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Introducing group chats in ChatGPT')]", "group-chats", "//h1[contains(text(),'Introducing group chats in ChatGPT')]", "Introducing group chats in ChatGPT", "Group chats product")

        # 4th product Introducing shopping research in ChatGPT
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Introducing shopping research in ChatGPT')]//div[contains(@class,'text-h5')]", "4th product title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Introducing shopping research in ChatGPT')]//div[contains(@class,'text-h5')]", "Introducing shopping research in ChatGPT", "4th product title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Introducing shopping research in ChatGPT')]", "chatgpt-shopping-research", "//h1[contains(text(),'Introducing shopping research in ChatGPT')]", "Introducing shopping research in ChatGPT", "Shopping research product")

    def tearDown(self):
        self.driver.quit()

class EdgePositiveTestCases(unittest.TestCase):

    def setUp(self):
        os.environ["SE_DRIVER_MIRROR_URL"] = "https://msedgedriver.microsoft.com"
        options = Edge_Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Edge(options=options)
        self.driver.execute_script("document.body.style.zoom='70%'")

    def test_1_correct_pageEdge(self):
        driver = self.driver
        driver.get(h.url_main)
        WebDriverWait(driver, 2).until(EC.url_contains("openai.com"))
        h.delay()
        print("----------------------test1-------------------------")

        try:
            assert driver.find_element(By.XPATH, "//a[normalize-space()='Company']").is_displayed()
            assert driver.find_element(By.XPATH, "//a[normalize-space()='Company']").is_enabled()
            print("Company is displayed and enabled")
        except AssertionError:
            print("Company tab is not found")

    def test_2_Plan_and_CharterEdge(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 2).until(EC.url_contains("openai.com/about/"))
        h.delay()
        print("----------------------test2-------------------------")

        h.assert_element_visible(driver, "//h3[normalize-space()='Our vision for the future of AGI']", "Header")
        h.assert_element_text_equals(driver, "//h3[normalize-space()='Our vision for the future of AGI']", "Our vision for the future of AGI", "Header")

        h.assert_element_visible(driver, "//a[normalize-space()='Our plan for AGI']", "Our plan for AGI button")
        h.assert_element_visible(driver, "//a[normalize-space()='Our Charter']", "Our Charter button")

        h.click_and_verify(driver, "//a[normalize-space()='Our Charter']", "charter", "//h1", "Our Charter", "Charter button")
        h.click_and_verify(driver, "//a[normalize-space()='Our plan for AGI']", "planning-for-agi-and-beyond", "//h1", "Our plan for AGI", "AGI button")

    def test_3_Latest_NewsEdge(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 2).until(EC.url_contains("openai.com/about/"))
        h.delay()
        print("----------------------test3-------------------------")

        h.assert_element_visible(driver, "//h2[normalize-space()='Latest news']", "Latest news section")

        # 1st news Sora
        h.assert_element_visible(driver, "//section[1]", "1st news picture")
        h.assert_element_text_equals(driver, "//div[contains(@class,'text-h5')]", "Sora 2 is here", "1st news title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Sora 2')]", "sora-2", "//h1[contains(text(),'Sora 2 is here')]", "Sora 2 is here", "Sora 2")

        # 2nd news Parental controls
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Introducing parental controls')]//div[contains(@class,'text-h5')]", "2nd news title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Introducing parental controls')]//div[contains(@class,'text-h5')]", "Introducing parental controls", "2nd news title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Introducing parental controls')]", "introducing-parental-controls", "//h1[contains(text(),'Introducing parental controls')]", "Introducing parental controls", "Parental controls")


    def test_4_Our_researchEdge(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 6).until(EC.url_contains("openai.com/about/"))
        h.delay()
        print("----------------------test4-------------------------")

        # 1st research Measuring the performance
        h.assert_element_visible(driver, "//section[1]", "1st research picture")
        h.assert_element_text_equals(driver, "//div[contains(@class,'text-h5')]", "Measuring the performance", "1st research title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Measuring the performance')]", "gdpval", "//h1[contains(text(),'Measuring the performance')]", "Measuring the performance", "Measuring the performance research")

        # # 2nd research Codex
        h.assert_element_visible(driver, "//a[contains(@aria-label,'How people are using ChatGPT')]//div[contains(@class,'text-h5')]", "2nd research title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'How people are using ChatGPT')]//div[contains(@class,'text-h5')]", "How people are using ChatGPT", "2nd research title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'How people are using ChatGPT')]", "how-people-are-using-chatgpt", "//h1[contains(text(),'How people are using ChatGPT')]", "How people are using ChatGPT", "People using GPT research")

        # 3rd research Why language models hallucinate
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Why language models hallucinate')]//div[contains(@class,'text-h5')]", "3rd research title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Why language models hallucinate')]//div[contains(@class,'text-h5')]", "Why language models hallucinate", "3rd research title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Why language models hallucinate')]", "why-language-models-hallucinate", "//h1[contains(text(),'Why language models hallucinate')]", "Why language models hallucinate", "Language models research")

        # 4th research Understanding neural networks
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Understanding neural networks through sparse circuits')]//div[contains(@class,'text-h5')]", "4th research title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Understanding neural networks through sparse circuits')]//div[contains(@class,'text-h5')]", "Understanding neural networks through sparse circuits", "4th research title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Understanding neural networks through sparse circuits')]", "understanding-neural-networks-through-sparse-circuits", "//h1[contains(text(),'Understanding neural networks through sparse circuits')]", "Understanding neural networks through sparse circuits", "Neural networks research")


    def test_5_Our_productsEdge(self):
        driver = self.driver
        driver.get(h.url_company)
        WebDriverWait(driver, 6).until(EC.url_contains("openai.com/about/"))
        h.delay()
        print("----------------------test5-------------------------")

        # 1st product Sora
        h.assert_element_visible(driver, "//section[1]", "1st product picture")
        h.assert_element_text_equals(driver, "//div[contains(@class,'text-h5')]", "Sora 2 is here", "1st product title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Sora 2')]", "sora-2", "//h1[contains(text(),'Sora 2 is here')]", "Sora 2 is here", "Sora 2 product")

        # 2nd product Codex
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Introducing upgrades to Codex')]//div[contains(@class,'text-h5')]", "2nd product title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Introducing upgrades to Codex')]//div[contains(@class,'text-h5')]", "Introducing upgrades to Codex", "2nd product title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Introducing upgrades to Codex')]", "introducing-upgrades-to-codex", "//h1[contains(text(),'Introducing upgrades to Codex')]", "Introducing upgrades to Codex", "Codex product")

        # 3rd product Group chats
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Introducing group chats in ChatGPT')]//div[contains(@class,'text-h5')]", "3rd product title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Introducing group chats in ChatGPT')]//div[contains(@class,'text-h5')]", "Introducing group chats in ChatGPT", "3rd product title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Introducing group chats in ChatGPT')]", "group-chats", "//h1[contains(text(),'Introducing group chats in ChatGPT')]", "Introducing group chats in ChatGPT", "Group chats product")

        # 4th product Introducing shopping research in ChatGPT
        h.assert_element_visible(driver, "//a[contains(@aria-label,'Introducing shopping research in ChatGPT')]//div[contains(@class,'text-h5')]", "4th product title")
        h.assert_element_text_equals(driver, "//a[contains(@aria-label,'Introducing shopping research in ChatGPT')]//div[contains(@class,'text-h5')]", "Introducing shopping research in ChatGPT", "4th product title")
        h.click_and_verify(driver, "//a[contains(@aria-label,'Introducing shopping research in ChatGPT')]", "chatgpt-shopping-research", "//h1[contains(text(),'Introducing shopping research in ChatGPT')]", "Introducing shopping research in ChatGPT", "Shopping research product")

    def tearDown(self):
        self.driver.quit()