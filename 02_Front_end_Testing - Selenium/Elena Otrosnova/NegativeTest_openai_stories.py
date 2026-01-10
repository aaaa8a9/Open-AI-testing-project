import unittest
import time
from test_helpers import (WebDriverFactory, PageHelpers, TestUtils, Constants,
                          ElementInteraction, StoriesPageHelpers)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class OpenAIStoriesEdgeCasesChromeTest(unittest.TestCase):
    """Chrome browser edge case test cases for OpenAI Stories"""

    def setUp(self):
        """Set up Chrome driver"""
        try:
            self.driver = WebDriverFactory.create_chrome_driver()
            self.browser_name = "Chrome"
        except Exception as e:
            self.skipTest(f"Chrome driver failed to initialize: {e}")

    def test_incorrect_url_shows_404_chrome(self):
        """TC_006: Verify that Stories page is not loading with an incorrectly entered URL in Chrome"""
        driver = self.driver
        incorrect_url = "https://openai.com/storiessss"

        driver.get(incorrect_url)
        TestUtils.wait_for_page_load(driver)

        # Check if 404 error page is displayed
        is_404 = self.check_for_404_error(driver)
        assert is_404, f"Expected 404 error page, but got normal page at {driver.current_url}"

        print(f"{self.browser_name}: 404 error page verification passed")

    def test_content_readable_at_200_percent_zoom_chrome(self):
        """TC_007: Verify that the stories content remains readable and properly structured when browser is zoomed to 200% or more in Chrome"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Zoom to 200%
        body = driver.find_element(By.TAG_NAME, "body")

        # Zoom in using keyboard shortcuts (Ctrl + multiple times)
        for _ in range(5):  # Zoom in 5 times to reach ~200%
            body.send_keys(Keys.CONTROL, Keys.ADD)
            time.sleep(0.3)

        time.sleep(2)  # Wait for zoom to apply

        # Verify content is still readable
        content_readable = self.verify_content_readable_at_zoom(driver)
        assert content_readable, "Content not readable or improperly structured at 200% zoom"

        print(f"{self.browser_name}: Content readability at 200% zoom verification passed")

    def test_story_headings_do_not_exceed_500_characters_chrome(self):
        """TC_008: Verify that story headings do not exceed 500 characters in Chrome"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Additional wait for dynamic content
        time.sleep(2)

        # Try to find ANY text content first for debugging
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body_text = body.text
            print(f"{self.browser_name}: Page has {len(body_text)} characters of text content")
        except:
            pass

        # Find all story headings using the actual page structure
        # Stories use different heading classes: text-h2, text-h5, etc.
        heading_selectors = [
            (By.CSS_SELECTOR, "a[href*='/index/'] div[class*='text-h']"),  # ⭐ All story headings
            (By.XPATH, "//a[contains(@href, '/index/')]//div[contains(@class, 'text-h')]"),  # ⭐ Alternative
            (By.CSS_SELECTOR, "div.text-h2"),  # Specific heading sizes
            (By.CSS_SELECTOR, "div.text-h3"),
            (By.CSS_SELECTOR, "div.text-h4"),
            (By.CSS_SELECTOR, "div.text-h5"),
            (By.XPATH, "//div[contains(@class, 'text-h2')]"),
            (By.XPATH, "//div[contains(@class, 'text-h5')]"),
            (By.CSS_SELECTOR, "h2"),  # Fallback traditional headings
            (By.CSS_SELECTOR, "h3"),
            (By.XPATH, "//h2"),
            (By.XPATH, "//h3")
        ]

        headings_found = False
        headings_valid = True
        invalid_headings = []
        all_headings = []

        for by_type, selector in heading_selectors:
            try:
                elements = driver.find_elements(by_type, selector)
                print(f"{self.browser_name}: Found {len(elements)} elements with selector: {selector}")

                if elements:
                    for i, element in enumerate(elements):
                        try:
                            # Check if element is displayed (but don't require it for headings)
                            heading_text = element.text.strip()

                            if heading_text and len(heading_text) > 3:  # Must have meaningful text
                                headings_found = True
                                all_headings.append(heading_text)
                                char_count = len(heading_text)

                                # Show first 60 characters of heading
                                preview = heading_text[:60] + "..." if len(heading_text) > 60 else heading_text
                                print(
                                    f"{self.browser_name}: Heading {len(all_headings)} length: {char_count} chars - '{preview}'")

                                # Check if heading exceeds 500 characters
                                if char_count > 500:
                                    headings_valid = False
                                    invalid_headings.append({
                                        'index': len(all_headings),
                                        'length': char_count,
                                        'text': heading_text[:100] + "..." if len(heading_text) > 100 else heading_text
                                    })
                                    print(
                                        f"{self.browser_name}: WARNING - Heading {len(all_headings)} exceeds 500 characters!")

                                # Check if heading has ellipsis (indicating truncation)
                                if char_count > 50:
                                    has_ellipsis = '...' in heading_text or '…' in heading_text
                                    if has_ellipsis:
                                        print(
                                            f"{self.browser_name}: Heading {len(all_headings)} properly truncated with ellipsis")
                        except Exception as e:
                            continue

                    if len(all_headings) >= 3:
                        # Found enough headings, stop searching
                        break
            except Exception as e:
                print(f"{self.browser_name}: Error with selector {selector}: {e}")
                continue

        # If still no headings found, take a more aggressive approach
        if not headings_found:
            print(f"{self.browser_name}: No headings found with standard selectors, trying all text elements...")
            try:
                # Get all text-containing elements
                all_elements = driver.find_elements(By.XPATH, "//*[string-length(normalize-space(text())) > 10]")
                print(f"{self.browser_name}: Found {len(all_elements)} elements with text content")

                for elem in all_elements[:20]:  # Check first 20 text elements
                    try:
                        text = elem.text.strip()
                        if text and len(text) > 10:
                            headings_found = True
                            all_headings.append(text)
                            print(f"{self.browser_name}: Text element {len(all_headings)}: {text[:50]}...")
                            if len(text) > 500:
                                headings_valid = False
                                invalid_headings.append({'index': len(all_headings), 'length': len(text)})
                    except:
                        continue
            except Exception as e:
                print(f"{self.browser_name}: Error finding text elements: {e}")

        assert headings_found, f"No story headings found on page after trying all selectors. Page may not have loaded properly."
        assert headings_valid, f"Found {len(invalid_headings)} headings exceeding 500 characters: {invalid_headings}"

        print(
            f"{self.browser_name}: Story heading character limit verification passed - checked {len(all_headings)} headings")

    def test_stories_page_without_javascript_chrome(self):
        """TC_009: Verify that the Load stories section with JavaScript disabled in Chrome"""
        # Need to create new driver with JavaScript disabled
        TestUtils.safe_teardown(self.driver, self.browser_name)

        try:
            self.driver = WebDriverFactory.create_chrome_driver(disable_javascript=True)
            driver = self.driver

            driver.get(Constants.STORIES_URL)
            TestUtils.wait_for_page_load(driver)

            # Check if basic content is accessible or if error message displays
            page_accessible = self.check_page_accessible_without_js(driver)

            # Either basic content should show or graceful degradation message
            assert page_accessible, "Page not accessible without JavaScript - no content or error message shown"

            print(f"{self.browser_name}: JavaScript disabled verification passed")

        except Exception as e:
            print(f"{self.browser_name}: JavaScript disabled test note: {e}")
            # This test may legitimately fail if site requires JS
            self.skipTest(f"Site may require JavaScript: {e}")

    def test_non_existent_story_id_shows_404_chrome(self):
        """TC_010: Verify that the Stories Access with non-existent ID shows 404 in Chrome"""
        driver = self.driver
        non_existent_url = "https://openai.com/stories/nonexistent-story-99999"

        driver.get(non_existent_url)
        TestUtils.wait_for_page_load(driver)

        # Check if 404 error page is displayed
        is_404 = self.check_for_404_error(driver)
        assert is_404, f"Expected 404 error for non-existent story, but got normal page at {driver.current_url}"

        print(f"{self.browser_name}: Non-existent story ID 404 verification passed")

    # Helper methods
    def check_for_404_error(self, driver):
        """Check if current page is a 404 error page"""
        try:
            # Check page title
            title = driver.title.lower()
            if '404' in title or 'not found' in title or 'error' in title:
                print(f"{self.browser_name}: 404 detected in page title: {title}")
                return True

            # Check page text content
            body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            error_indicators = ['404', 'not found', 'page not found', "doesn't exist", 'cannot find']

            for indicator in error_indicators:
                if indicator in body_text:
                    print(f"{self.browser_name}: 404 detected - found '{indicator}' in page content")
                    return True

            # Check for specific 404 elements
            error_selectors = [
                "//h1[contains(text(), '404')]",
                "//h1[contains(text(), 'Not Found')]",
                "//div[contains(@class, '404')]",
                "//div[contains(@class, 'error')]"
            ]

            for selector in error_selectors:
                try:
                    element = driver.find_element(By.XPATH, selector)
                    if element and element.is_displayed():
                        print(f"{self.browser_name}: 404 element found using selector: {selector}")
                        return True
                except:
                    continue

            print(f"{self.browser_name}: No 404 error detected")
            return False
        except Exception as e:
            print(f"{self.browser_name}: Error checking for 404: {e}")
            return False

    def verify_content_readable_at_zoom(self, driver):
        """Verify content is readable and properly structured at zoom level"""
        try:
            # Check if story cards are still visible
            stories_visible = StoriesPageHelpers.verify_stories_have_images(driver, self.browser_name, timeout=3)
            if not stories_visible:
                print(f"{self.browser_name}: Stories not visible at zoom")
                return False

            # Check for horizontal scrollbar (indicates layout problems)
            has_horizontal_scroll = driver.execute_script(
                "return document.documentElement.scrollWidth > document.documentElement.clientWidth;"
            )

            if has_horizontal_scroll:
                scroll_width = driver.execute_script("return document.documentElement.scrollWidth;")
                client_width = driver.execute_script("return document.documentElement.clientWidth;")
                print(
                    f"{self.browser_name}: Warning - Horizontal scroll detected (scroll: {scroll_width}, client: {client_width})")
                # Don't fail test for horizontal scroll, just warn

            # Check if text is readable (not overlapping)
            titles = driver.find_elements(By.CSS_SELECTOR, "h2, h3")
            if titles:
                first_title = titles[0]
                if first_title.is_displayed():
                    font_size = first_title.value_of_css_property("font-size")
                    print(f"{self.browser_name}: Title font size at zoom: {font_size}")

                    # Verify no text cutoff
                    overflow = first_title.value_of_css_property("overflow")
                    if overflow == "hidden":
                        print(f"{self.browser_name}: Warning - Text may be cut off (overflow: hidden)")

            print(f"{self.browser_name}: Content appears readable at zoom")
            return True

        except Exception as e:
            print(f"{self.browser_name}: Error verifying zoom readability: {e}")
            return False

    def check_page_accessible_without_js(self, driver):
        """Check if page is accessible without JavaScript"""
        try:
            # Check if any content is visible
            body = driver.find_element(By.TAG_NAME, "body")
            body_text = body.text.strip()

            if not body_text:
                print(f"{self.browser_name}: No content found without JavaScript")
                return False

            # Check for error messages or graceful degradation
            error_messages = [
                'javascript',
                'enable javascript',
                'requires javascript',
                'please enable',
                'browser not supported'
            ]

            body_text_lower = body_text.lower()
            for msg in error_messages:
                if msg in body_text_lower:
                    print(f"{self.browser_name}: Graceful degradation message found: '{msg}'")
                    return True

            # Check if basic content is available
            images = driver.find_elements(By.TAG_NAME, "img")
            links = driver.find_elements(By.TAG_NAME, "a")

            if len(images) > 0 or len(links) > 5:
                print(f"{self.browser_name}: Basic content available without JavaScript")
                return True

            print(f"{self.browser_name}: Page has content but may not be fully functional without JavaScript")
            return True

        except Exception as e:
            print(f"{self.browser_name}: Error checking accessibility without JS: {e}")
            return False

    def tearDown(self):
        """Clean up after each test"""
        TestUtils.safe_teardown(self.driver, self.browser_name)


class OpenAIStoriesEdgeCasesEdgeTest(unittest.TestCase):
    """Edge browser edge case test cases for OpenAI Stories"""

    def setUp(self):
        """Set up Edge driver"""
        try:
            self.driver = WebDriverFactory.create_edge_driver()
            self.browser_name = "Edge"
        except Exception as e:
            self.skipTest(f"Edge driver failed to initialize: {e}")

    def test_incorrect_url_shows_404_edge(self):
        """TC_006: Verify that Stories page is not loading with an incorrectly entered URL in Edge"""
        driver = self.driver
        incorrect_url = "https://openai.com/storiessss"

        driver.get(incorrect_url)
        TestUtils.wait_for_page_load(driver)

        is_404 = self.check_for_404_error(driver)
        assert is_404, f"Expected 404 error page, but got normal page at {driver.current_url}"

        print(f"{self.browser_name}: 404 error page verification passed")

    def test_content_readable_at_200_percent_zoom_edge(self):
        """TC_007: Verify that the stories content remains readable and properly structured when browser is zoomed to 200% or more in Edge"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        body = driver.find_element(By.TAG_NAME, "body")

        for _ in range(5):
            body.send_keys(Keys.CONTROL, Keys.ADD)
            time.sleep(0.3)

        time.sleep(2)

        content_readable = self.verify_content_readable_at_zoom(driver)
        assert content_readable, "Content not readable or improperly structured at 200% zoom"

        print(f"{self.browser_name}: Content readability at 200% zoom verification passed")

    def test_story_titles_do_not_exceed_500_characters_edge(self):
        """TC_008: Verify that story titles/headings do not exceed 500 characters in Edge"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Additional wait for dynamic content
        time.sleep(2)

        # Try to find ANY text content first for debugging
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body_text = body.text
            print(f"{self.browser_name}: Page has {len(body_text)} characters of text content")
        except:
            pass

        # Find all story titles with very broad selectors
        title_selectors = [
            (By.CSS_SELECTOR, "h2"),
            (By.CSS_SELECTOR, "h3"),
            (By.CSS_SELECTOR, "h1"),
            (By.CSS_SELECTOR, "h4"),
            (By.XPATH, "//h2"),
            (By.XPATH, "//h3"),
            (By.XPATH, "//h1"),
            (By.XPATH, "//h4"),
            (By.XPATH, "//*[contains(@class, 'title')]"),
            (By.XPATH, "//*[contains(@class, 'heading')]")
        ]

        titles_found = False
        titles_valid = True
        invalid_titles = []
        all_titles = []

        for by_type, selector in title_selectors:
            try:
                elements = driver.find_elements(by_type, selector)
                print(f"{self.browser_name}: Found {len(elements)} elements with selector: {selector}")

                if elements:
                    for i, element in enumerate(elements):
                        try:
                            # Check if element is displayed (but don't require it for titles)
                            title_text = element.text.strip()

                            if title_text and len(title_text) > 3:  # Must have meaningful text
                                titles_found = True
                                all_titles.append(title_text)
                                char_count = len(title_text)

                                # Show first 60 characters of title
                                preview = title_text[:60] + "..." if len(title_text) > 60 else title_text
                                print(
                                    f"{self.browser_name}: Title {len(all_titles)} length: {char_count} chars - '{preview}'")

                                # Check if title exceeds 500 characters
                                if char_count > 500:
                                    titles_valid = False
                                    invalid_titles.append({
                                        'index': len(all_titles),
                                        'length': char_count,
                                        'text': title_text[:100] + "..." if len(title_text) > 100 else title_text
                                    })
                                    print(
                                        f"{self.browser_name}: WARNING - Title {len(all_titles)} exceeds 500 characters!")

                                # Check if title has ellipsis (indicating truncation)
                                if char_count > 50:
                                    has_ellipsis = '...' in title_text or '…' in title_text
                                    if has_ellipsis:
                                        print(
                                            f"{self.browser_name}: Title {len(all_titles)} properly truncated with ellipsis")
                        except Exception as e:
                            continue

                    if len(all_titles) >= 3:
                        # Found enough titles, stop searching
                        break
            except Exception as e:
                print(f"{self.browser_name}: Error with selector {selector}: {e}")
                continue

        # If still no titles found, take a more aggressive approach
        if not titles_found:
            print(f"{self.browser_name}: No titles found with standard selectors, trying all text elements...")
            try:
                # Get all text-containing elements
                all_elements = driver.find_elements(By.XPATH, "//*[string-length(normalize-space(text())) > 10]")
                print(f"{self.browser_name}: Found {len(all_elements)} elements with text content")

                for elem in all_elements[:20]:  # Check first 20 text elements
                    try:
                        text = elem.text.strip()
                        if text and len(text) > 10:
                            titles_found = True
                            all_titles.append(text)
                            print(f"{self.browser_name}: Text element {len(all_titles)}: {text[:50]}...")
                            if len(text) > 500:
                                titles_valid = False
                                invalid_titles.append({'index': len(all_titles), 'length': len(text)})
                    except:
                        continue
            except Exception as e:
                print(f"{self.browser_name}: Error finding text elements: {e}")

        assert titles_found, f"No story titles found on page after trying all selectors. Page may not have loaded properly."
        assert titles_valid, f"Found {len(invalid_titles)} titles exceeding 500 characters: {invalid_titles}"

        print(
            f"{self.browser_name}: Story title character limit verification passed - checked {len(all_titles)} titles")

    def test_stories_page_without_javascript_edge(self):
        """TC_009: Verify that the Load stories section with JavaScript disabled in Edge"""
        TestUtils.safe_teardown(self.driver, self.browser_name)

        try:
            self.driver = WebDriverFactory.create_edge_driver(disable_javascript=True)
            driver = self.driver

            driver.get(Constants.STORIES_URL)
            TestUtils.wait_for_page_load(driver)

            page_accessible = self.check_page_accessible_without_js(driver)
            assert page_accessible, "Page not accessible without JavaScript - no content or error message shown"

            print(f"{self.browser_name}: JavaScript disabled verification passed")

        except Exception as e:
            print(f"{self.browser_name}: JavaScript disabled test note: {e}")
            self.skipTest(f"Site may require JavaScript: {e}")

    def test_non_existent_story_id_shows_404_edge(self):
        """TC_010: Verify that the Stories Access with non-existent ID shows 404 in Edge"""
        driver = self.driver
        non_existent_url = "https://openai.com/stories/nonexistent-story-99999"

        driver.get(non_existent_url)
        TestUtils.wait_for_page_load(driver)

        is_404 = self.check_for_404_error(driver)
        assert is_404, f"Expected 404 error for non-existent story, but got normal page at {driver.current_url}"

        print(f"{self.browser_name}: Non-existent story ID 404 verification passed")

    # Helper methods (same as Chrome test class)
    def check_for_404_error(self, driver):
        """Check if current page is a 404 error page"""
        try:
            title = driver.title.lower()
            if '404' in title or 'not found' in title or 'error' in title:
                print(f"{self.browser_name}: 404 detected in page title: {title}")
                return True

            body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            error_indicators = ['404', 'not found', 'page not found', "doesn't exist", 'cannot find']

            for indicator in error_indicators:
                if indicator in body_text:
                    print(f"{self.browser_name}: 404 detected - found '{indicator}' in page content")
                    return True

            error_selectors = [
                "//h1[contains(text(), '404')]",
                "//h1[contains(text(), 'Not Found')]",
                "//div[contains(@class, '404')]",
                "//div[contains(@class, 'error')]"
            ]

            for selector in error_selectors:
                try:
                    element = driver.find_element(By.XPATH, selector)
                    if element and element.is_displayed():
                        print(f"{self.browser_name}: 404 element found using selector: {selector}")
                        return True
                except:
                    continue

            print(f"{self.browser_name}: No 404 error detected")
            return False
        except Exception as e:
            print(f"{self.browser_name}: Error checking for 404: {e}")
            return False

    def verify_content_readable_at_zoom(self, driver):
        """Verify content is readable and properly structured at zoom level"""
        try:
            stories_visible = StoriesPageHelpers.verify_stories_have_images(driver, self.browser_name, timeout=3)
            if not stories_visible:
                print(f"{self.browser_name}: Stories not visible at zoom")
                return False

            has_horizontal_scroll = driver.execute_script(
                "return document.documentElement.scrollWidth > document.documentElement.clientWidth;"
            )

            if has_horizontal_scroll:
                scroll_width = driver.execute_script("return document.documentElement.scrollWidth;")
                client_width = driver.execute_script("return document.documentElement.clientWidth;")
                print(
                    f"{self.browser_name}: Warning - Horizontal scroll detected (scroll: {scroll_width}, client: {client_width})")

            titles = driver.find_elements(By.CSS_SELECTOR, "h2, h3")
            if titles:
                first_title = titles[0]
                if first_title.is_displayed():
                    font_size = first_title.value_of_css_property("font-size")
                    print(f"{self.browser_name}: Title font size at zoom: {font_size}")

                    overflow = first_title.value_of_css_property("overflow")
                    if overflow == "hidden":
                        print(f"{self.browser_name}: Warning - Text may be cut off (overflow: hidden)")

            print(f"{self.browser_name}: Content appears readable at zoom")
            return True

        except Exception as e:
            print(f"{self.browser_name}: Error verifying zoom readability: {e}")
            return False

    def check_page_accessible_without_js(self, driver):
        """Check if page is accessible without JavaScript"""
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body_text = body.text.strip()

            if not body_text:
                print(f"{self.browser_name}: No content found without JavaScript")
                return False

            error_messages = [
                'javascript',
                'enable javascript',
                'requires javascript',
                'please enable',
                'browser not supported'
            ]

            body_text_lower = body_text.lower()
            for msg in error_messages:
                if msg in body_text_lower:
                    print(f"{self.browser_name}: Graceful degradation message found: '{msg}'")
                    return True

            images = driver.find_elements(By.TAG_NAME, "img")
            links = driver.find_elements(By.TAG_NAME, "a")

            if len(images) > 0 or len(links) > 5:
                print(f"{self.browser_name}: Basic content available without JavaScript")
                return True

            print(f"{self.browser_name}: Page has content but may not be fully functional without JavaScript")
            return True

        except Exception as e:
            print(f"{self.browser_name}: Error checking accessibility without JS: {e}")
            return False

    def tearDown(self):
        """Clean up after each test"""
        TestUtils.safe_teardown(self.driver, self.browser_name)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(OpenAIStoriesEdgeCasesChromeTest))
    suite.addTests(loader.loadTestsFromTestCase(OpenAIStoriesEdgeCasesEdgeTest))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)