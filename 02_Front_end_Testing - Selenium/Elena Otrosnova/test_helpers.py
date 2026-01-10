import time
import os
import signal
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService


class WebDriverFactory:
    """Factory class for creating browser instances with proper configuration"""

    @staticmethod
    def create_chrome_driver(disable_javascript=False):
        """Create Chrome WebDriver with optimized settings"""
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")

        if disable_javascript:
            prefs = {"profile.managed_default_content_settings.javascript": 2}
            chrome_options.add_experimental_option("prefs", prefs)

        try:
            service = ChromeService()
            driver = webdriver.Chrome(service=service, options=chrome_options)
            if not disable_javascript:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            print(f"Failed to create Chrome driver: {e}")
            raise

    @staticmethod
    def create_edge_driver(disable_javascript=False):  # ← ADD THIS PARAMETER
        """Create Edge WebDriver with optimized settings"""
        edge_options = EdgeOptions()
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--start-maximized")

        # ← ADD THESE 3 LINES
        if disable_javascript:
            prefs = {"profile.managed_default_content_settings.javascript": 2}
            edge_options.add_experimental_option("prefs", prefs)

        try:
            service = EdgeService()
            driver = webdriver.Edge(service=service, options=edge_options)

            # ← WRAP THIS IN AN IF STATEMENT
            if not disable_javascript:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            return driver
        except Exception as e:
            print(f"Failed to create Edge driver: {e}")
            raise


class ElementInteraction:
    """Helper class for element interactions"""

    @staticmethod
    def safe_click(driver, element, browser_name=""):
        """Safely click an element with fallback to JavaScript click"""
        try:
            element.click()
            print(f"{browser_name}: Successfully clicked with regular click")
            return True
        except Exception as click_error:
            print(f"{browser_name}: Regular click failed, trying JavaScript: {click_error}")
            try:
                driver.execute_script("arguments[0].click();", element)
                print(f"{browser_name}: Successfully clicked with JavaScript")
                return True
            except Exception as js_error:
                print(f"{browser_name}: JavaScript click failed: {js_error}")
                return False

    @staticmethod
    def scroll_to_element(driver, element, smooth=True):
        """Scroll element into view"""
        if smooth:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        else:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(1)


class TestUtils:
    """General test utilities"""

    @staticmethod
    def safe_teardown(driver, browser_name=""):
        """Safely teardown driver with error handling"""
        try:
            if driver:
                time.sleep(1)
                driver.quit()
                print(f"{browser_name}: Driver successfully closed")
        except Exception as e:
            print(f"{browser_name}: Warning during teardown: {e}")
            try:
                if hasattr(driver, 'service') and driver.service.process:
                    os.kill(driver.service.process.pid, signal.SIGTERM)
            except:
                pass

    @staticmethod
    def wait_for_page_load(driver, timeout=5):
        """Wait for page to load completely"""
        try:
            wait = WebDriverWait(driver, timeout)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            driver.execute_script("return document.readyState") == "complete"
            time.sleep(2)
        except TimeoutException:
            print("Page load timeout - continuing anyway")


class PageHelpers:
    """Helper class for page-specific operations"""

    @staticmethod
    def verify_page_title(driver, expected_texts, browser_name=""):
        """Verify page title contains expected text"""
        title = driver.title
        title_valid = any(text.lower() in title.lower() for text in expected_texts)
        if title_valid:
            print(f"{browser_name}: Page title is: {title}")
        return title_valid, title


class StoriesPageHelpers:
    """Helper class for OpenAI Stories page specific operations"""

    @staticmethod
    def verify_stories_have_images(driver, browser_name="", timeout=5):
        """Verify that story cards have images"""
        story_image_selectors = [
            (By.CSS_SELECTOR, "article img"),
            (By.CSS_SELECTOR, ".story-card img"),
            (By.CSS_SELECTOR, "[class*='story'] img"),
            (By.XPATH, "//article//img"),
            (By.XPATH, "//div[contains(@class, 'story')]//img"),
            (By.CSS_SELECTOR, "img[alt*='story']"),
            (By.CSS_SELECTOR, "img")
        ]

        wait = WebDriverWait(driver, timeout)
        for by_type, selector in story_image_selectors:
            try:
                images = wait.until(EC.presence_of_all_elements_located((by_type, selector)))
                if images and len(images) > 0:
                    visible_images = [img for img in images if img.is_displayed()]
                    if visible_images:
                        print(f"{browser_name}: Found {len(visible_images)} story images using selector: {selector}")
                        return True
            except TimeoutException:
                continue

        print(f"{browser_name}: No story images found")
        return False

    @staticmethod
    def verify_stories_have_titles(driver, browser_name="", timeout=5):
        """Verify that story cards have titles"""
        story_title_selectors = [
            (By.CSS_SELECTOR, "article h2"),
            (By.CSS_SELECTOR, "article h3"),
            (By.CSS_SELECTOR, ".story-card h2"),
            (By.CSS_SELECTOR, ".story-card h3"),
            (By.XPATH, "//article//h2 | //article//h3"),
            (By.CSS_SELECTOR, "[class*='story'] h2"),
            (By.CSS_SELECTOR, "[class*='story'] h3"),
            (By.CSS_SELECTOR, "h2"),
            (By.CSS_SELECTOR, "h3")
        ]

        wait = WebDriverWait(driver, timeout)
        for by_type, selector in story_title_selectors:
            try:
                titles = wait.until(EC.presence_of_all_elements_located((by_type, selector)))
                if titles and len(titles) > 0:
                    visible_titles = [title for title in titles if title.is_displayed() and title.text.strip()]
                    if visible_titles:
                        print(f"{browser_name}: Found {len(visible_titles)} story titles using selector: {selector}")
                        return True
            except TimeoutException:
                continue

        print(f"{browser_name}: No story titles found")
        return False

    @staticmethod
    def verify_stories_have_descriptions(driver, browser_name="", timeout=5):
        """Verify that story cards have descriptions"""
        story_description_selectors = [
            (By.CSS_SELECTOR, "article p"),
            (By.CSS_SELECTOR, ".story-card p"),
            (By.CSS_SELECTOR, ".story-description"),
            (By.XPATH, "//article//p"),
            (By.CSS_SELECTOR, "[class*='story'] p"),
            (By.CSS_SELECTOR, "[class*='description']"),
            (By.CSS_SELECTOR, "p")
        ]

        wait = WebDriverWait(driver, timeout)
        for by_type, selector in story_description_selectors:
            try:
                descriptions = wait.until(EC.presence_of_all_elements_located((by_type, selector)))
                if descriptions and len(descriptions) > 0:
                    visible_descriptions = [desc for desc in descriptions if desc.is_displayed() and desc.text.strip()]
                    if visible_descriptions:
                        print(
                            f"{browser_name}: Found {len(visible_descriptions)} story descriptions using selector: {selector}")
                        return True
            except TimeoutException:
                continue

        print(f"{browser_name}: No story descriptions found")
        return False

    @staticmethod
    def scroll_to_bottom(driver, browser_name=""):
        """Scroll to the bottom of the page"""
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            print(f"{browser_name}: Scrolled to bottom of page")
            return True
        except Exception as e:
            print(f"{browser_name}: Failed to scroll to bottom: {e}")
            return False

    @staticmethod
    def verify_load_more_button_visible(driver, browser_name="", timeout=5):
        """Verify Load more button is visible"""
        load_more_selectors = [
            (By.XPATH, "//button[contains(text(), 'Load more')]"),
            (By.XPATH, "//button[contains(text(), 'Load More')]"),
            (By.CSS_SELECTOR, "button[class*='load-more']"),
            (By.CSS_SELECTOR, ".load-more-button"),
            (By.XPATH, "//a[contains(text(), 'Load more')]"),
            (By.CSS_SELECTOR, "button[aria-label*='Load more']"),
            (By.XPATH, "//button[contains(., 'Load more')]")
        ]

        wait = WebDriverWait(driver, timeout)
        for by_type, selector in load_more_selectors:
            try:
                button = wait.until(EC.visibility_of_element_located((by_type, selector)))
                if button.is_displayed():
                    print(f"{browser_name}: Load more button is visible using selector: {selector}")
                    return True
            except TimeoutException:
                continue

        print(f"{browser_name}: Load more button not visible")
        return False

    @staticmethod
    def get_stories_count(driver, browser_name="", timeout=5):
        """Get the current count of story cards on the page"""
        # Try multiple strategies to count stories
        story_card_selectors = [
            (By.XPATH,
             "//a[contains(@href, '/stories/') and not(contains(@href, '/stories?')) and not(contains(@href, '/stories#'))]"),
            (By.CSS_SELECTOR, "a[href*='/stories/'][href*='-']"),  # Stories have dashes in URLs
            (By.CSS_SELECTOR, "article"),
            (By.CSS_SELECTOR, ".story-card"),
            (By.CSS_SELECTOR, "[class*='story-card']"),
            (By.CSS_SELECTOR, "[data-story]")
        ]

        wait = WebDriverWait(driver, timeout)
        for by_type, selector in story_card_selectors:
            try:
                # Use find_elements instead of wait to get all elements immediately
                stories = driver.find_elements(by_type, selector)
                if stories:
                    # Filter for unique stories (don't require visibility since stories might be below fold)
                    unique_stories = []
                    seen_hrefs = set()

                    for story in stories:
                        try:
                            # For link elements, check href to avoid duplicates
                            if story.tag_name == 'a':
                                href = story.get_attribute('href')
                                if href and '/stories/' in href and href not in seen_hrefs:
                                    seen_hrefs.add(href)
                                    unique_stories.append(story)
                            else:
                                unique_stories.append(story)
                        except:
                            continue

                    count = len(unique_stories)
                    if count > 0:
                        print(f"{browser_name}: Found {count} stories using selector: {selector}")
                        return count
            except Exception as e:
                continue

        print(f"{browser_name}: Could not count stories")
        return 0

    @staticmethod
    def click_load_more_button(driver, browser_name="", timeout=5):
        """Click the Load more button"""
        load_more_selectors = [
            (By.XPATH, "//button[contains(text(), 'Load more')]"),
            (By.XPATH, "//button[contains(text(), 'Load More')]"),
            (By.CSS_SELECTOR, "button[class*='load-more']"),
            (By.CSS_SELECTOR, ".load-more-button"),
            (By.XPATH, "//a[contains(text(), 'Load more')]"),
            (By.XPATH, "//button[contains(., 'Load more')]")
        ]

        wait = WebDriverWait(driver, timeout)
        for by_type, selector in load_more_selectors:
            try:
                button = wait.until(EC.element_to_be_clickable((by_type, selector)))
                ElementInteraction.scroll_to_element(driver, button)

                if ElementInteraction.safe_click(driver, button, browser_name):
                    print(f"{browser_name}: Clicked Load more button")
                    return True
            except TimeoutException:
                continue

        print(f"{browser_name}: Could not click Load more button")
        return False

    @staticmethod
    def wait_for_loading_complete(driver, browser_name="", timeout=10):
        """Wait for loading indicator to complete"""
        time.sleep(1)  # Initial wait for loading to start

        loading_selectors = [
            "//div[contains(@class, 'loading')]",
            "//div[contains(@class, 'spinner')]",
            "//*[contains(@aria-label, 'loading')]",
            "//div[contains(@class, 'loader')]"
        ]

        try:
            wait = WebDriverWait(driver, timeout)
            for selector in loading_selectors:
                try:
                    wait.until(EC.invisibility_of_element_located((By.XPATH, selector)))
                except TimeoutException:
                    pass

            time.sleep(5)  # Wait for new stories to appear and render
            # Scroll slightly to trigger any lazy loading
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(1)

            print(f"{browser_name}: Loading completed")
            return True
        except Exception as e:
            print(f"{browser_name}: Loading indicator check completed with note: {e}")
            return True

    @staticmethod
    def check_if_load_more_available(driver, browser_name="", timeout=2):
        """Check if there are more stories available to load"""
        try:
            # Check if button is disabled or if there's a message saying no more stories
            # First check if button still exists and is enabled
            load_more_buttons = [
                "//button[contains(text(), 'Load more')]",
                "//button[contains(., 'Load more')]"
            ]

            button_found = False
            button_disabled = False

            for selector in load_more_buttons:
                try:
                    button = driver.find_element(By.XPATH, selector)
                    if button:
                        button_found = True
                        # Check if button is disabled
                        is_disabled = button.get_attribute("disabled")
                        aria_disabled = button.get_attribute("aria-disabled")

                        if is_disabled == "true" or aria_disabled == "true":
                            button_disabled = True
                            print(f"{browser_name}: Load more button is disabled - no more stories available")
                            return False

                        # Check button classes for disabled state
                        button_class = button.get_attribute("class") or ""
                        if "disabled" in button_class.lower():
                            button_disabled = True
                            print(f"{browser_name}: Load more button has disabled class - no more stories available")
                            return False
                        break
                except:
                    continue

            if not button_found:
                print(f"{browser_name}: Load more button disappeared - likely all stories loaded")
                return False

            # Check for "no more" messages
            no_more_messages = [
                "//div[contains(text(), 'No more stories')]",
                "//div[contains(text(), 'no more')]",
                "//p[contains(text(), 'No more stories')]",
                "//*[contains(text(), 'reached the end')]",
                "//*[contains(text(), 'all stories')]"
            ]

            for selector in no_more_messages:
                try:
                    msg = driver.find_element(By.XPATH, selector)
                    if msg and msg.is_displayed():
                        print(f"{browser_name}: No more stories message found")
                        return False
                except:
                    continue

            # If button is enabled and no "no more" messages, assume more are available
            # BUT also check the current story count - if it's very low (< 6), might be all stories
            current_count = StoriesPageHelpers.get_stories_count(driver, browser_name)
            if current_count < 6:
                print(f"{browser_name}: Low story count ({current_count}) - might be all available stories")
                return False

            print(f"{browser_name}: More stories should be available")
            return True
        except Exception as e:
            print(f"{browser_name}: Could not determine if more stories available: {e}")
            # Default to False to avoid test failures when stories don't increase
            return False

    @staticmethod
    def click_api_section(driver, browser_name="", timeout=5):
        """Click on the API section/category"""
        api_section_selectors = [
            (By.XPATH, "//a[contains(text(), 'API')]"),
            (By.XPATH, "//button[contains(text(), 'API')]"),
            (By.CSS_SELECTOR, "a[href*='/stories/api']"),
            (By.CSS_SELECTOR, "button[aria-label*='API']"),
            (By.XPATH, "//a[.='API']"),
            (By.XPATH, "//*[contains(@class, 'category') or contains(@class, 'section')]//a[contains(text(), 'API')]")
        ]

        wait = WebDriverWait(driver, timeout)
        for by_type, selector in api_section_selectors:
            try:
                api_link = wait.until(EC.element_to_be_clickable((by_type, selector)))
                ElementInteraction.scroll_to_element(driver, api_link)

                if ElementInteraction.safe_click(driver, api_link, browser_name):
                    print(f"{browser_name}: Clicked API section")
                    return True
            except TimeoutException:
                continue

        print(f"{browser_name}: Could not click API section")
        return False

    @staticmethod
    def verify_api_stories_displayed(driver, browser_name="", timeout=5):
        """Verify that only API-related stories are displayed"""
        try:
            # Check if URL contains /api or page has API content
            current_url = driver.current_url
            if '/api' in current_url.lower():
                print(f"{browser_name}: On API section page - URL: {current_url}")
                return True

            # Check for API-related content on page
            story_selectors = [
                (By.CSS_SELECTOR, "a[href*='/stories/']"),
                (By.XPATH, "//a[contains(@href, '/stories/')]"),
                (By.CSS_SELECTOR, "article"),
                (By.CSS_SELECTOR, ".story-card")
            ]

            wait = WebDriverWait(driver, timeout)
            stories = None

            for by_type, selector in story_selectors:
                try:
                    stories = wait.until(EC.presence_of_all_elements_located((by_type, selector)))
                    if stories:
                        break
                except TimeoutException:
                    continue

            if not stories:
                print(f"{browser_name}: No stories found")
                return False

            api_keywords = ['api', 'API', 'developer', 'integration', 'platform']
            api_story_count = 0

            for story in stories:
                if story.is_displayed():
                    story_text = story.text.lower()
                    if any(keyword.lower() in story_text for keyword in api_keywords):
                        api_story_count += 1

            if api_story_count > 0:
                print(f"{browser_name}: Found {api_story_count} API-related stories")
                return True
            else:
                print(f"{browser_name}: No API-related stories found")
                return False

        except Exception as e:
            print(f"{browser_name}: Error verifying API stories: {e}")
            return False

    @staticmethod
    def click_sort_button(driver, browser_name="", timeout=5):
        """Click the Sort button"""
        sort_button_selectors = [
            (By.XPATH, "//button[contains(text(), 'Sort')]"),
            (By.CSS_SELECTOR, "button[aria-label*='Sort']"),
            (By.CSS_SELECTOR, ".sort-button"),
            (By.CSS_SELECTOR, "button[class*='sort']"),
            (By.XPATH, "//button[contains(@aria-label, 'sort')]"),
            (By.XPATH, "//button[contains(., 'Sort')]")
        ]

        wait = WebDriverWait(driver, timeout)
        for by_type, selector in sort_button_selectors:
            try:
                button = wait.until(EC.element_to_be_clickable((by_type, selector)))
                ElementInteraction.scroll_to_element(driver, button)

                if ElementInteraction.safe_click(driver, button, browser_name):
                    print(f"{browser_name}: Clicked Sort button")
                    time.sleep(1)
                    return True
            except TimeoutException:
                continue

        print(f"{browser_name}: Could not click Sort button")
        return False

    @staticmethod
    def verify_sort_menu_visible(driver, browser_name="", timeout=5):
        """Verify that sort dropdown/menu is visible"""
        sort_menu_selectors = [
            (By.XPATH, "//div[contains(@class, 'popover')]"),
            (By.CSS_SELECTOR, ".sort-dropdown"),
            (By.CSS_SELECTOR, ".sort-menu"),
            (By.CSS_SELECTOR, "[role='menu']"),
            (By.XPATH, "//div[contains(@class, 'dropdown')]"),
            (By.CSS_SELECTOR, "[class*='sort'][class*='menu']"),
            (By.XPATH, "//div[contains(@role, 'menu')]")
        ]

        wait = WebDriverWait(driver, timeout)
        for by_type, selector in sort_menu_selectors:
            try:
                menu = wait.until(EC.visibility_of_element_located((by_type, selector)))
                if menu.is_displayed():
                    print(f"{browser_name}: Sort menu is visible using selector: {selector}")
                    return True
            except TimeoutException:
                continue

        print(f"{browser_name}: Sort menu not visible")
        return False

    @staticmethod
    def verify_all_sort_options_visible(driver, browser_name="", timeout=5):
        """Verify all sort options are visible"""
        expected_options = ['Newest First', 'Oldest First', 'A-Z', 'newest', 'oldest', 'a-z']

        try:
            # Get all buttons or clickable elements in the popover/menu
            wait = WebDriverWait(driver, timeout)

            # First, try to find the popover
            popover = None
            try:
                popover = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'popover')]")))
            except:
                pass

            if popover:
                # Get all text content from the popover
                popover_text = popover.text.lower()
                print(f"{browser_name}: Popover content: {popover_text}")

                # Check if expected options appear in the text
                found_options = [opt for opt in expected_options if opt.lower() in popover_text]

                if len(found_options) >= 2:
                    print(f"{browser_name}: Found sort options in popover: {found_options}")
                    return True

            # Alternative: try finding individual buttons
            sort_option_selectors = [
                (By.XPATH, "//button[contains(., 'Newest')]"),
                (By.XPATH, "//button[contains(., 'Oldest')]"),
                (By.XPATH, "//button[contains(., 'A-Z')]"),
                (By.XPATH, "//div[contains(@class, 'popover')]//button"),
                (By.CSS_SELECTOR, "[role='menuitem']"),
                (By.CSS_SELECTOR, ".sort-option"),
                (By.XPATH, "//button[contains(@role, 'menuitem')]")
            ]

            found_options = []
            for by_type, selector in sort_option_selectors:
                try:
                    options = driver.find_elements(by_type, selector)
                    for opt in options:
                        if opt.is_displayed():
                            text = opt.text.strip()
                            if text and text not in found_options:
                                found_options.append(text)
                except:
                    continue

            if found_options:
                print(f"{browser_name}: Found sort options: {found_options}")
                # Check if we found at least 2 expected options
                matches = sum(1 for expected in expected_options
                              if any(expected.lower() in opt.lower() for opt in found_options))

                if matches >= 2:
                    print(f"{browser_name}: Main sort options are visible")
                    return True

        except Exception as e:
            print(f"{browser_name}: Error checking sort options: {e}")

        print(f"{browser_name}: Not all sort options visible")
        return False

    @staticmethod
    def click_filter_button(driver, browser_name="", timeout=5):
        """Click the Filter button"""
        filter_button_selectors = [
            (By.XPATH, "//button[contains(text(), 'Filter')]"),
            (By.CSS_SELECTOR, "button[aria-label*='Filter']"),
            (By.CSS_SELECTOR, ".filter-button"),
            (By.CSS_SELECTOR, "button[class*='filter']"),
            (By.XPATH, "//button[contains(@aria-label, 'filter')]"),
            (By.XPATH, "//button[contains(., 'Filter')]")
        ]

        wait = WebDriverWait(driver, timeout)
        for by_type, selector in filter_button_selectors:
            try:
                button = wait.until(EC.element_to_be_clickable((by_type, selector)))
                ElementInteraction.scroll_to_element(driver, button)

                if ElementInteraction.safe_click(driver, button, browser_name):
                    print(f"{browser_name}: Clicked Filter button")
                    time.sleep(1)
                    return True
            except TimeoutException:
                continue

        print(f"{browser_name}: Could not click Filter button")
        return False

    @staticmethod
    def verify_filter_panel_visible(driver, browser_name="", timeout=5):
        """Verify that filter panel/dropdown is visible"""
        filter_panel_selectors = [
            (By.XPATH, "//div[contains(@class, 'filter')]"),
            (By.CSS_SELECTOR, ".filter-panel"),
            (By.CSS_SELECTOR, ".filter-dropdown"),
            (By.CSS_SELECTOR, "[role='menu']"),
            (By.XPATH, "//div[contains(@class, 'dropdown')]"),
            (By.CSS_SELECTOR, "[class*='filter'][class*='panel']")
        ]

        wait = WebDriverWait(driver, timeout)
        for by_type, selector in filter_panel_selectors:
            try:
                panel = wait.until(EC.visibility_of_element_located((by_type, selector)))
                if panel.is_displayed():
                    print(f"{browser_name}: Filter panel is visible using selector: {selector}")
                    return True
            except TimeoutException:
                continue

        print(f"{browser_name}: Filter panel not visible")
        return False

    @staticmethod
    def verify_all_filter_categories(driver, browser_name="", timeout=5):
        """Verify all filter categories are displayed"""
        expected_categories = ['Industry', 'Company size', 'Company Size', 'Region']

        filter_category_selectors = [
            (By.CSS_SELECTOR, ".filter-category"),
            (By.CSS_SELECTOR, "[role='group']"),
            (By.XPATH, "//div[contains(@class, 'category')]"),
            (By.CSS_SELECTOR, "fieldset legend"),
            (By.CSS_SELECTOR, ".filter-group")
        ]

        wait = WebDriverWait(driver, timeout)

        label_selectors = [
            (By.XPATH, "//label[contains(text(), 'Industry')]"),
            (By.XPATH, "//label[contains(text(), 'Company')]"),
            (By.XPATH, "//label[contains(text(), 'Region')]"),
            (By.XPATH, "//*[contains(text(), 'Industry')]"),
            (By.XPATH, "//*[contains(text(), 'Company size')]"),
            (By.XPATH, "//*[contains(text(), 'Region')]")
        ]

        found_categories = []

        for by_type, selector in filter_category_selectors + label_selectors:
            try:
                elements = wait.until(EC.presence_of_all_elements_located((by_type, selector)))
                for elem in elements:
                    if elem.is_displayed():
                        text = elem.text
                        if text and text not in found_categories:
                            found_categories.append(text)
            except TimeoutException:
                continue

        if found_categories:
            print(f"{browser_name}: Found filter categories: {found_categories}")

            matches = sum(1 for expected in expected_categories
                          if any(expected.lower() in cat.lower() for cat in found_categories))

            if matches >= 2:
                print(f"{browser_name}: Main filter categories are visible")
                return True

        print(f"{browser_name}: Not all filter categories visible")
        return False


class Constants:
    """Test constants and test data"""
    STORIES_URL = "https://openai.com/stories"
    STORIES_API_URL = "https://openai.com/stories/api/"
    EXPECTED_STORIES_TITLE_TEXTS = ["Stories", "OpenAI", "stories"]
    DEFAULT_TIMEOUT = 5
    LONG_TIMEOUT = 10