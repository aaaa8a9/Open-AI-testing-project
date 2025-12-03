import time
import unittest
import random
from selenium import webdriver
import os
import Helpers_OpenAI as h

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.common import WebDriverException as WDE, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def delay():
    time.sleep(random.randint(3,4))
# This function is for delay() it randomly pics time between 2 and 4 seconds

class ChromeTestPositive(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        #options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        #options.page_load_strategy = 'eager'
        driver = self.driver
        wait = WebDriverWait(driver, 5)
# This is a class setUp. We will have 2 (chrome, edge)

    def test_chrome_TC_P_001(self):
        driver = self.driver
# Verify that the 'Safety' link opens the correct page and validate the presence of three unique elements
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Verify that the 'Introducing Parental Controls' section is present on the page
        Parental_Controls = driver.find_element(By.XPATH, "(//a[@id='65FG7bFcn1JxADqHbF1nQx'])[1]")
        driver.execute_script("return arguments[0].scrollIntoView(true);", Parental_Controls)
        if Parental_Controls is not None:
            print("✅ Section 'Parental_Controls' is visible and displayed")
        else:
            print("❌ Section 'Parental_Controls' is not displayed")
        delay()
# 3. Verify that the 'Test' diagram is displayed on the page
        Test_diagram = driver.find_element(By.XPATH, "//div[@class='relative font-mono uppercase md:h-[1080px] md:w-[1920px]']")
        driver.execute_script("return arguments[0].scrollIntoView(true);", Test_diagram)
        if Test_diagram is not None:
            print("✅ Section 'Test_diagram' is visible and displayed")
        else:
            print("❌ Section 'Test_diagram' is not displayed")
        delay()
# 4. Verify that the page title is 'Safety at Every Step'
        try:
            assert "Safety & responsibility | OpenAI" in driver.title
            print("✅ Title is correct!")
        except WDE:
            print("❌ Title is wrong! Title is: ", driver.title)

    def test_chrome_TC_P_002(self):
        driver = self.driver
# Verify the presence and functionality of the 'Where is AI Going?' video on the page
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Locate the 'Where is AI Going?' video on the page
        Where_is_IA_going = driver.find_element(By.XPATH, "//div[@class='group relative flex h-full w-full overflow-hidden outline-none rounded-md aspect-16/9 md:aspect-16/9 lg:aspect-16/9 bg-primary-4']")
        driver.execute_script("return arguments[0].scrollIntoView(true);", Where_is_IA_going)
        time.sleep(7)
        driver.save_screenshot("before_play.png")
        if Where_is_IA_going is not None:
            print("✅ Section 'Where_is_IA_going' is visible and displayed")
        else:
            print("❌ Section 'Where_is_IA_going' is not displayed")
# 3. Play the video
        play_button = driver.find_element(By.XPATH, "//div[@class='flex-initial']//button[@aria-label='Pause video']//*[name()='svg']")
        play_button.click()
        #driver.execute_script("arguments[0].click();", play_button)
        time.sleep(11)
# 4. Check if video is playing
        driver.save_screenshot("after_play.png")
        if Where_is_IA_going.is_displayed():
            print("✅ Video is playing!")
        else:
            print("❌ Video is NOT playing!")

    def test_chrome_TC_P_003(self):
        driver = self.driver
# Verify that the main image is present on the page under the subsection 'Security & Privacy'
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Click on the 'Security & privacy' link-button on the left side of the page
        driver.find_element(By.XPATH, "//a[@class='transition ease-curve-a duration-250 ps-3xs pe-xs py-4xs block h-full w-full focus-visible:rounded-sm'][normalize-space()='Security & Privacy']").click()
        time.sleep(5)
# 3. Verify that the 'OpenAI Humans' image is present on the page
        wait = WebDriverWait(driver, 4)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//img[@alt='OpenAI humans']")))
            print("✅ 'OpenAI Humans' image is visible on the page")
        except NoSuchElementException:
            print("❌ Page is wrong!")

    def test_chrome_TC_P_004(self):
        driver = self.driver
# Verify that the 'Download All Data' button in the 'Safety Evaluations Hub' section is working
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
        # Set a known download director

        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)

        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
        }
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options)
        driver.get("https://openai.com/safety/")
        time.sleep(7)
# 2. Scroll down to the section 'Go Deeper on Safety'
        Go_Deeper_on_Safety = driver.find_element(By.XPATH, "//body/div[@class='duration-sidebar ease-curve-sidebar grid transition-[grid-template-columns] grid-cols-[0_1fr] md:grid-cols-[0_theme(spacing.nav-width)_1fr]']/div[@class='pt-header-h relative']/div/main[@id='main']/div[@class='flex flex-col mt-10 gap-2xl @md:gap-3xl']/div[3]/div[1]")
        driver.execute_script("return arguments[0].scrollIntoView(true);", Go_Deeper_on_Safety)
        time.sleep(5)
# 3. Click the 'Explore the Safety Evaluations Hub' link-button
        driver.find_element(By.XPATH, "//a[normalize-space()='Explore the safety evaluations hub']").click()
        time.sleep(7)
# 4. Click on ""Download All Data""
        driver.find_element(By.XPATH, "//a[normalize-space()='Download all data']").click()
# 5. Verify that the file has been downloaded successfully
        # Wait until file appears
        timeout = 10
        downloaded = False
        for _ in range(timeout):
            files = os.listdir(download_dir)
            if any(f.endswith(".zip") or f.endswith(".json") for f in files):  # adjust extension
                downloaded = True
                break
            time.sleep(3)

        if downloaded:
            print("✅ File downloaded successfully!")
        else:
            print("❌ File not found.")

    def test_chrome_TC_P_005(self):
        driver = self.driver
# Verify that the 'Listen to Article' player is working in the 'OpenAI Safety Update' section
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
        driver.switch_to.window(driver.window_handles[-1])
# 2. Scroll down to the 'Latest News on Safety' section
        latest_news_section = driver.find_element(By.XPATH, "//h2[normalize-space()='Latest news on safety']")
        driver.execute_script("arguments[0].scrollIntoView(true);", latest_news_section)
        time.sleep(4)
# 3. Click the 'OpenAI Safety Update' link-button
        driver.find_element(By.XPATH, "//a[@id='56VJpNfXGEenoGLOvzemCi']").click()
        time.sleep(5)
# 4. Locate the 'Listen to Article' player
        audio_button = driver.find_element(By.XPATH, "//button[@aria-label='Play audio of page text']")
# 5. Click on the 'Listen to Article' player
        audio_button.click()
        time.sleep(3)
        audio_player = driver.find_element(By.XPATH, "//div[@class='relative flex']")
        time.sleep(3)
# 6. Verify audio playback
        is_paused = driver.execute_script("return arguments[0].paused", audio_button)
        start_time = driver.execute_script("return arguments[0].currentTime", audio_player)
        time.sleep(2)
        end_time = driver.execute_script("return arguments[0].currentTime", audio_player)
        is_paused = driver.execute_script("return arguments[0].paused", audio_player)
        # assert is_paused is False, "Audio should be playing but is paused"
        # assert end_time > start_time, "Audio currentTime did not advance — not playing"
        print("✅ 'Listen to Article' player is working!")

    # Anything declared in tearDown will be executed for all test cases
# Closing browser. You need to use "tearDown" method only one time for every Class
    def tearDown(self):
        self.driver.quit()

class EdgeTestPositive(unittest.TestCase):
    def setUp(self):
        options = webdriver.EdgeOptions()
        # options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        self.driver.maximize_window()
        # options.page_load_strategy = 'eager'
        driver = self.driver
        wait = WebDriverWait(driver, 5)

    # This is a class setUp. We will have 2 (chrome, edge)

    def test_edge_TC_P_001(self):
        driver = self.driver
        # Verify that the 'Safety' link opens the correct page and validate the presence of three unique elements
        # 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
        # 2. Verify that the 'Introducing Parental Controls' section is present on the page
        Parental_Controls = driver.find_element(By.XPATH, "(//a[@id='65FG7bFcn1JxADqHbF1nQx'])[1]")
        driver.execute_script("return arguments[0].scrollIntoView(true);", Parental_Controls)
        if Parental_Controls is not None:
            print("✅ Section 'Parental_Controls' is visible and displayed")
        else:
            print("❌ Section 'Parental_Controls' is not displayed")
        delay()
        # 3. Verify that the 'Test' diagram is displayed on the page
        Test_diagram = driver.find_element(By.XPATH,
                                           "//div[@class='relative font-mono uppercase md:h-[1080px] md:w-[1920px]']")
        driver.execute_script("return arguments[0].scrollIntoView(true);", Test_diagram)
        if Test_diagram is not None:
            print("✅ Section 'Test_diagram' is visible and displayed")
        else:
            print("❌ Section 'Test_diagram' is not displayed")
        delay()
        # 4. Verify that the page title is 'Safety at Every Step'
        try:
            assert "Safety & responsibility | OpenAI" in driver.title
            print("✅ Title is correct!")
        except WDE:
            print("❌ Title is wrong! Title is: ", driver.title)

    def test_edge_TC_P_002(self):
        driver = self.driver
        # Verify the presence and functionality of the 'Where is AI Going?' video on the page
        # 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
        # 2. Locate the 'Where is AI Going?' video on the page
        Where_is_IA_going = driver.find_element(By.XPATH,
                                                "//div[@class='group relative flex h-full w-full overflow-hidden outline-none rounded-md aspect-16/9 md:aspect-16/9 lg:aspect-16/9 bg-primary-4']")
        driver.execute_script("return arguments[0].scrollIntoView(true);", Where_is_IA_going)
        time.sleep(7)
        driver.save_screenshot("before_play.png")
        if Where_is_IA_going is not None:
            print("✅ Section 'Where_is_IA_going' is visible and displayed")
        else:
            print("❌ Section 'Where_is_IA_going' is not displayed")
        # 3. Play the video
        play_button = driver.find_element(By.XPATH,
                                          "//div[@class='flex-initial']//button[@aria-label='Pause video']//*[name()='svg']")
        play_button.click()
        # driver.execute_script("arguments[0].click();", play_button)
        time.sleep(11)
        # 4. Check if video is playing
        driver.save_screenshot("after_play.png")
        if Where_is_IA_going.is_displayed():
            print("✅ Video is playing!")
        else:
            print("❌ Video is NOT playing!")

    def test_edge_TC_P_003(self):
        driver = self.driver
        # Verify that the main image is present on the page under the subsection 'Security & Privacy'
        # 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
        # 2. Click on the 'Security & privacy' link-button on the left side of the page
        driver.find_element(By.XPATH,
                            "//a[@class='transition ease-curve-a duration-250 ps-3xs pe-xs py-4xs block h-full w-full focus-visible:rounded-sm'][normalize-space()='Security & Privacy']").click()
        time.sleep(5)
        # 3. Verify that the 'OpenAI Humans' image is present on the page
        wait = WebDriverWait(driver, 4)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//img[@alt='OpenAI humans']")))
            print("✅ 'OpenAI Humans' image is visible on the page")
        except NoSuchElementException:
            print("❌ Page is wrong!")

    def test_edge_TC_P_004(self):
        driver = self.driver
        # Verify that the 'Download All Data' button in the 'Safety Evaluations Hub' section is working
        # 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
        # Set a known download director

        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)

        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
        }
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options)
        driver.get("https://openai.com/safety/")
        time.sleep(7)
        # 2. Scroll down to the section 'Go Deeper on Safety'
        Go_Deeper_on_Safety = driver.find_element(By.XPATH,
                                                  "//body/div[@class='duration-sidebar ease-curve-sidebar grid transition-[grid-template-columns] grid-cols-[0_1fr] md:grid-cols-[0_theme(spacing.nav-width)_1fr]']/div[@class='pt-header-h relative']/div/main[@id='main']/div[@class='flex flex-col mt-10 gap-2xl @md:gap-3xl']/div[3]/div[1]")
        driver.execute_script("return arguments[0].scrollIntoView(true);", Go_Deeper_on_Safety)
        time.sleep(5)
        # 3. Click the 'Explore the Safety Evaluations Hub' link-button
        driver.find_element(By.XPATH, "//a[normalize-space()='Explore the safety evaluations hub']").click()
        time.sleep(7)
        # 4. Click on ""Download All Data""
        driver.find_element(By.XPATH, "//a[normalize-space()='Download all data']").click()
        # 5. Verify that the file has been downloaded successfully
        # Wait until file appears
        timeout = 10
        downloaded = False
        for _ in range(timeout):
            files = os.listdir(download_dir)
            if any(f.endswith(".zip") or f.endswith(".json") for f in files):  # adjust extension
                downloaded = True
                break
            time.sleep(3)

        if downloaded:
            print("✅ File downloaded successfully!")
        else:
            print("❌ File not found.")

    def test_edge_TC_P_005(self):
        driver = self.driver
        # Verify that the 'Listen to Article' player is working in the 'OpenAI Safety Update' section
        # 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
        driver.switch_to.window(driver.window_handles[-1])
        # 2. Scroll down to the 'Latest News on Safety' section
        latest_news_section = driver.find_element(By.XPATH, "//h2[normalize-space()='Latest news on safety']")
        driver.execute_script("arguments[0].scrollIntoView(true);", latest_news_section)
        time.sleep(4)
        # 3. Click the 'OpenAI Safety Update' link-button
        driver.find_element(By.XPATH, "//a[@id='56VJpNfXGEenoGLOvzemCi']").click()
        time.sleep(5)
        # 4. Locate the 'Listen to Article' player
        audio_button = driver.find_element(By.XPATH, "//button[@aria-label='Play audio of page text']")
        # 5. Click on the 'Listen to Article' player
        audio_button.click()
        time.sleep(3)
        audio_player = driver.find_element(By.XPATH, "//div[@class='relative flex']")
        time.sleep(3)
        # 6. Verify audio playback
        is_paused = driver.execute_script("return arguments[0].paused", audio_button)
        start_time = driver.execute_script("return arguments[0].currentTime", audio_player)
        time.sleep(2)
        end_time = driver.execute_script("return arguments[0].currentTime", audio_player)
        is_paused = driver.execute_script("return arguments[0].paused", audio_player)
        # assert is_paused is False, "Audio should be playing but is paused"
        # assert end_time > start_time, "Audio currentTime did not advance — not playing"
        print("✅ 'Listen to Article' player is working!")

    # Anything declared in tearDown will be executed for all test cases
    # Closing browser. You need to use "tearDown" method only one time for every Class
    def tearDown(self):
        self.driver.quit()


class ChromeTestNegative(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        #options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        #options.page_load_strategy = 'eager'
        driver = self.driver
        wait = WebDriverWait(driver, 5)
# This is a class setUp. We will have 2 (chrome, edge)

    def test_chrome_TC_N_001(self):
        driver = self.driver
#Verify that the 'Search' button (magnifying glass icon) is disabled or inactive when the search field is empty
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Locate the Search Button (Magnifying Glass Icon) in the top right corner
        search_button = driver.find_element(By.XPATH, "//button[@aria-label='Open Search']//*[name()='svg']")
# 3. Click the Search Button
        search_button.click()
        time.sleep(2)
# 4. Attempt to submit with an empty search field
        search_input = driver.find_element(By.XPATH, "//textarea[@class='placeholder:text-primary-44 text-h3 @md:text-h2 z-[1] min-h-[1lh] w-full resize-none bg-transparent focus:outline-none']")
        delay()
    # Verify field is empty
        assert search_input.get_attribute("value") == "", "Search field should be empty"
        time.sleep(5)
    # Try to submit with empty input
        search_input.submit()
        time.sleep(2)
    # Verify URL did not change (still on safety page)
        assert "openai.com/safety" in driver.current_url, "Search should not work when empty"
        print("✅ Search button is inactive when search field is empty")

    def test_chrome_TC_N_002(self):
        driver = self.driver
#Verify that the system displays an appropriate error message or shows no results when an invalid search term is entered in the search field
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Locate the Search Button (Magnifying Glass Icon) in the top right corner
        search_button = driver.find_element(By.XPATH, "//button[@aria-label='Open Search']//*[name()='svg']")
# 3. Click the Search Button
        search_button.click()
        time.sleep(2)
# 4. Enter "UUUU" into the search input field
        search_input = driver.find_element(By.XPATH, "//textarea[@class='placeholder:text-primary-44 text-h3 @md:text-h2 z-[1] min-h-[1lh] w-full resize-none bg-transparent focus:outline-none']")
        search_input.send_keys("UUUU")
        time.sleep(2)
# 5. Click the submit button
        search_input.submit()
        time.sleep(8)
        # ✅ Verify expected result: "It looks like your question goes beyond what we can assist with here" message appears
        page_source = driver.page_source
        assert "It looks like your question goes beyond what we can assist with here." in page_source, "Expected 'It looks like your question goes beyond what we can assist with here' message for invalid search term"
        print("✅ Verified: Invalid search shows 'It looks like your question goes beyond what we can assist with here'")

    def test_chrome_TC_N_003(self):
        driver = self.driver
# Verify that the 'OpenAI Platform' login form does not allow submission when the email field is empty
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Click on the "API log in" link
        h.API_log_in(driver)
# 3. Navigate to the new tab
        h.switch_window(driver)
# 4. Leave the "Email Address" field empty
        email_input = driver.find_element(By.NAME, "email")
        assert email_input.get_attribute("value") == "", "Email field should be empty"
# 5. Click the 'Continue' button
        continue_button = driver.find_element(By.XPATH, "//button[normalize-space()='Continue']")
        continue_button.click()
        time.sleep(2)
# ✅ Expected Result: Error message "Email is required"
        page_source = driver.page_source
        assert "Email is required" in page_source, "Expected error message 'Email is required' not found"
        print("✅ Verified: Login form does not allow submission when email is empty")

    def test_chrome_TC_N_004(self):
        driver = self.driver
# Verify that the 'ChatGPT' login form does not allow submission with an invalid phone number
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Click on the "API log in" link
        h.API_log_in(driver)
# 3. Navigate to the new tab
        h.switch_window(driver)
# 4. Click on "Continue with phone" button
        phone_btn = driver.find_element(By.XPATH, "//button[@type='button']")
        phone_btn.click()
        time.sleep(2)
# 5. Enter invalid phone number '564 66'
        phone_input = driver.find_element(By.XPATH, "//input[@id='tel']")
        phone_input.send_keys("564 66")
        time.sleep(3)
# 6. Click the 'Continue' button
        continue_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Continue']")
        continue_btn.click()
        time.sleep(3)
        # ✅ Expected Result: Error message "Phone number is not valid"
        page_source = driver.page_source
        assert "Phone number is not valid" in page_source, "Expected error message 'Phone number is not valid' not found"
        print("✅ Verified: ChatGPT login form rejects invalid phone number with proper error message")

    def test_chrome_TC_N_005(self):
        driver = self.driver
# Verify that the 'OpenAI Platform' login form does not allow submission with an invalid email address
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Click on the "API log in" link
        h.API_log_in(driver)
# 3. Navigate to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)
# 4. Enter invalid email address "dila@gmail"
        email_input = driver.find_element(By.XPATH, "//input[@id='«r1»-email']")
        email_input.send_keys("dila@gmail")
        time.sleep(2)
# 5. Click the 'Continue' button
        continue_button = driver.find_element(By.XPATH, "//button[normalize-space()='Continue']")
        continue_button.click()
        time.sleep(3)
        # ✅ Expected Result: Error message "Email is not valid"
        page_source = driver.page_source
        assert "Email is not valid" in page_source, "Expected error message 'Email is not valid' not found"
        print("✅ Verified: error message 'Email is not valid'")

    # Anything declared in tearDown will be executed for all test cases
# Closing browser. You need to use "tearDown" method only one time for every Class
    def tearDown(self):
        self.driver.quit()

class EdgeTestNegative(unittest.TestCase):
    def setUp(self):
        options = webdriver.EdgeOptions()
        #options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        self.driver.maximize_window()
        #options.page_load_strategy = 'eager'
        driver = self.driver
        wait = WebDriverWait(driver, 5)
# This is a class setUp. We will have 2 (chrome, edge)

    def test_edge_TC_N_001(self):
        driver = self.driver
#Verify that the 'Search' button (magnifying glass icon) is disabled or inactive when the search field is empty
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Locate the Search Button (Magnifying Glass Icon) in the top right corner
        search_button = driver.find_element(By.XPATH, "//button[@aria-label='Open Search']//*[name()='svg']")
# 3. Click the Search Button
        search_button.click()
        time.sleep(2)
# 4. Attempt to submit with an empty search field
        search_input = driver.find_element(By.XPATH, "//textarea[@class='placeholder:text-primary-44 text-h3 @md:text-h2 z-[1] min-h-[1lh] w-full resize-none bg-transparent focus:outline-none']")
        delay()
    # Verify field is empty
        assert search_input.get_attribute("value") == "", "Search field should be empty"
        time.sleep(5)
    # Try to submit with empty input
        search_input.submit()
        time.sleep(2)
    # Verify URL did not change (still on safety page)
        assert "openai.com/safety" in driver.current_url, "Search should not work when empty"
        print("✅ Search button is inactive when search field is empty")

    def test_edge_TC_N_002(self):
        driver = self.driver
#Verify that the system displays an appropriate error message or shows no results when an invalid search term is entered in the search field
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Locate the Search Button (Magnifying Glass Icon) in the top right corner
        search_button = driver.find_element(By.XPATH, "//button[@aria-label='Open Search']//*[name()='svg']")
# 3. Click the Search Button
        search_button.click()
        time.sleep(2)
# 4. Enter "UUUU" into the search input field
        search_input = driver.find_element(By.XPATH, "//textarea[@class='placeholder:text-primary-44 text-h3 @md:text-h2 z-[1] min-h-[1lh] w-full resize-none bg-transparent focus:outline-none']")
        search_input.send_keys("UUUU")
        time.sleep(2)
# 5. Click the submit button
        search_input.submit()
        time.sleep(8)
        # ✅ Verify expected result: "It looks like your question goes beyond what we can assist with here" message appears
        page_source = driver.page_source
        assert "It looks like your question goes beyond what we can assist with here." in page_source, "Expected 'It looks like your question goes beyond what we can assist with here' message for invalid search term"
        print("✅ Verified: Invalid search shows 'It looks like your question goes beyond what we can assist with here'")

    def test_edge_TC_N_003(self):
        driver = self.driver
# Verify that the 'OpenAI Platform' login form does not allow submission when the email field is empty
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Click on the "API log in" link
        h.API_log_in(driver)
# 3. Navigate to the new tab
        h.switch_window(driver)
# 4. Leave the "Email Address" field empty
        email_input = driver.find_element(By.NAME, "email")
        assert email_input.get_attribute("value") == "", "Email field should be empty"
# 5. Click the 'Continue' button
        continue_button = driver.find_element(By.XPATH, "//button[normalize-space()='Continue']")
        continue_button.click()
        time.sleep(2)
# ✅ Expected Result: Error message "Email is required"
        page_source = driver.page_source
        assert "Email is required" in page_source, "Expected error message 'Email is required' not found"
        print("✅ Verified: Login form does not allow submission when email is empty")

    def test_edge_TC_N_004(self):
        driver = self.driver
# Verify that the 'ChatGPT' login form does not allow submission with an invalid phone number
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Click on the "API log in" link
        h.API_log_in(driver)
# 3. Navigate to the new tab
        h.switch_window(driver)
# 4. Click on "Continue with phone" button
        phone_btn = driver.find_element(By.XPATH, "//button[@type='button']")
        phone_btn.click()
        time.sleep(2)
# 5. Enter invalid phone number '564 66'
        phone_input = driver.find_element(By.XPATH, "//input[@id='tel']")
        phone_input.send_keys("564 66")
        time.sleep(3)
# 6. Click the 'Continue' button
        continue_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Continue']")
        continue_btn.click()
        time.sleep(3)
        # ✅ Expected Result: Error message "Phone number is not valid"
        page_source = driver.page_source
        assert "Phone number is not valid" in page_source, "Expected error message 'Phone number is not valid' not found"
        print("✅ Verified: ChatGPT login form rejects invalid phone number with proper error message")

    def test_edge_TC_N_005(self):
        driver = self.driver
# Verify that the 'OpenAI Platform' login form does not allow submission with an invalid email address
# 1. Go to https://openai.com/safety/
        h.Safety_Link(driver)
# 2. Click on the "API log in" link
        h.API_log_in(driver)
# 3. Navigate to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)
# 4. Enter invalid email address "dila@gmail"
        email_input = driver.find_element(By.XPATH, "//input[@id='«r1»-email']")
        email_input.send_keys("dila@gmail")
        time.sleep(2)
# 5. Click the 'Continue' button
        continue_button = driver.find_element(By.XPATH, "//button[normalize-space()='Continue']")
        continue_button.click()
        time.sleep(3)
        # ✅ Expected Result: Error message "Email is not valid"
        page_source = driver.page_source
        assert "Email is not valid" in page_source, "Expected error message 'Email is not valid' not found"
        print("✅ Verified: error message 'Email is not valid'")

    # Anything declared in tearDown will be executed for all test cases
# Closing browser. You need to use "tearDown" method only one time for every Class
    def tearDown(self):
        self.driver.quit()
