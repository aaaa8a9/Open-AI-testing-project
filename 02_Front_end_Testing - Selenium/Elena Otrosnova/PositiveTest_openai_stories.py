import unittest
import time
from test_helpers import (WebDriverFactory, PageHelpers, TestUtils, Constants,
                          ElementInteraction, StoriesPageHelpers)


class OpenAIStoriesChromeTest(unittest.TestCase):
    """Chrome browser test cases for OpenAI Stories"""

    def setUp(self):
        """Set up Chrome driver"""
        try:
            self.driver = WebDriverFactory.create_chrome_driver()
            self.browser_name = "Chrome"
        except Exception as e:
            self.skipTest(f"Chrome driver failed to initialize: {e}")

    def test_stories_page_loads_with_content_chrome(self):
        """TC_001: Verify that stories page loads correctly with images, titles, and descriptions in Chrome"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Verify page title
        title_valid, title = PageHelpers.verify_page_title(
            driver, Constants.EXPECTED_STORIES_TITLE_TEXTS, self.browser_name
        )
        assert title_valid, f"Expected 'Stories' in title, got: {title}"

        # Verify stories cards with images
        stories_with_images = StoriesPageHelpers.verify_stories_have_images(driver, self.browser_name)
        assert stories_with_images, "Stories cards with images not found in Chrome"

        # Verify stories have titles
        stories_with_titles = StoriesPageHelpers.verify_stories_have_titles(driver, self.browser_name)
        assert stories_with_titles, "Stories cards with titles not found in Chrome"

        # Verify stories have descriptions
        stories_with_descriptions = StoriesPageHelpers.verify_stories_have_descriptions(driver, self.browser_name)
        assert stories_with_descriptions, "Stories cards with descriptions not found in Chrome"

        print(f"{self.browser_name}: Stories page content verification passed")

    def test_load_more_button_works_chrome(self):
        """TC_002: Verify that 'Load more' button works correctly in Chrome"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Scroll to bottom of page
        StoriesPageHelpers.scroll_to_bottom(driver, self.browser_name)
        time.sleep(1)

        # Verify Load more button is visible
        load_more_visible = StoriesPageHelpers.verify_load_more_button_visible(driver, self.browser_name)
        assert load_more_visible, "Load more button not visible in Chrome"

        # Check if more stories are available to load
        more_available = StoriesPageHelpers.check_if_load_more_available(driver, self.browser_name)

        # Get initial story count
        initial_count = StoriesPageHelpers.get_stories_count(driver, self.browser_name)
        print(f"{self.browser_name}: Initial story count: {initial_count}")
        assert initial_count > 0, "No stories found on page initially"

        # Click Load more button
        load_more_clicked = StoriesPageHelpers.click_load_more_button(driver, self.browser_name)
        assert load_more_clicked, "Could not click Load more button in Chrome"

        # Wait for loading indicator to complete
        loading_complete = StoriesPageHelpers.wait_for_loading_complete(driver, self.browser_name)
        assert loading_complete, "Loading did not complete in Chrome"

        # Verify additional stories loaded
        final_count = StoriesPageHelpers.get_stories_count(driver, self.browser_name)
        print(f"{self.browser_name}: Final story count: {final_count}")

        # If more stories were available, count should increase
        # If no more stories available, count staying the same is acceptable
        if more_available:
            assert final_count > initial_count, f"Stories not loaded: initial={initial_count}, final={final_count}"
            print(f"{self.browser_name}: Load more functionality verification passed - stories loaded")
        else:
            print(
                f"{self.browser_name}: Load more functionality verified - no more stories available to load (count: {final_count})")
            # Test passes because button worked even though no new stories loaded

    def test_api_section_displays_correctly_chrome(self):
        """TC_003: Verify that 'API' section is displayed and only shows API-related stories in Chrome"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Click on API section
        api_section_clicked = StoriesPageHelpers.click_api_section(driver, self.browser_name)
        assert api_section_clicked, "Could not click API section in Chrome"

        # Wait for page to load
        time.sleep(2)
        TestUtils.wait_for_page_load(driver)

        # Verify only API-related stories are displayed
        api_stories_only = StoriesPageHelpers.verify_api_stories_displayed(driver, self.browser_name)
        assert api_stories_only, "Non-API stories found or no API stories displayed in Chrome"

        print(f"{self.browser_name}: API section verification passed")

    def test_sort_button_opens_dropdown_chrome(self):
        """TC_004: Verify that clicking Sort button opens sort dropdown/menu in Chrome"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Locate and click Sort button
        sort_button_clicked = StoriesPageHelpers.click_sort_button(driver, self.browser_name)
        assert sort_button_clicked, "Could not click Sort button in Chrome"

        # Verify sort dropdown/menu opens
        sort_menu_visible = StoriesPageHelpers.verify_sort_menu_visible(driver, self.browser_name)
        assert sort_menu_visible, "Sort dropdown/menu not visible in Chrome"

        # Verify all sort options are visible
        all_options_visible = StoriesPageHelpers.verify_all_sort_options_visible(driver, self.browser_name)
        assert all_options_visible, "Not all sort options visible in Chrome"

        print(f"{self.browser_name}: Sort button and dropdown verification passed")

    def test_filter_button_displays_categories_chrome(self):
        """TC_005: Verify that All filter categories display correctly in Chrome"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Locate and click Filter button
        filter_button_clicked = StoriesPageHelpers.click_filter_button(driver, self.browser_name)
        assert filter_button_clicked, "Could not click Filter button in Chrome"

        # Verify filter panel/dropdown opens
        filter_panel_visible = StoriesPageHelpers.verify_filter_panel_visible(driver, self.browser_name)
        assert filter_panel_visible, "Filter panel/dropdown not visible in Chrome"

        # Verify all filter categories are displayed
        all_categories_visible = StoriesPageHelpers.verify_all_filter_categories(driver, self.browser_name)
        assert all_categories_visible, "Not all filter categories displayed in Chrome"

        print(f"{self.browser_name}: Filter categories verification passed")

    def tearDown(self):
        """Clean up after each test"""
        TestUtils.safe_teardown(self.driver, self.browser_name)


class OpenAIStoriesEdgeTest(unittest.TestCase):
    """Edge browser test cases for OpenAI Stories"""

    def setUp(self):
        """Set up Edge driver"""
        try:
            self.driver = WebDriverFactory.create_edge_driver()
            self.browser_name = "Edge"
        except Exception as e:
            self.skipTest(f"Edge driver failed to initialize: {e}")

    def test_stories_page_loads_with_content_edge(self):
        """TC_001: Verify that stories page loads correctly with images, titles, and descriptions in Edge"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Verify page title
        title_valid, title = PageHelpers.verify_page_title(
            driver, Constants.EXPECTED_STORIES_TITLE_TEXTS, self.browser_name
        )
        assert title_valid, f"Expected 'Stories' in title, got: {title}"

        # Verify stories cards with images
        stories_with_images = StoriesPageHelpers.verify_stories_have_images(driver, self.browser_name)
        assert stories_with_images, "Stories cards with images not found in Edge"

        # Verify stories have titles
        stories_with_titles = StoriesPageHelpers.verify_stories_have_titles(driver, self.browser_name)
        assert stories_with_titles, "Stories cards with titles not found in Edge"

        # Verify stories have descriptions
        stories_with_descriptions = StoriesPageHelpers.verify_stories_have_descriptions(driver, self.browser_name)
        assert stories_with_descriptions, "Stories cards with descriptions not found in Edge"

        print(f"{self.browser_name}: Stories page content verification passed")

    def test_load_more_button_works_edge(self):
        """TC_002: Verify that 'Load more' button works correctly in Edge"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Scroll to bottom of page
        StoriesPageHelpers.scroll_to_bottom(driver, self.browser_name)
        time.sleep(1)

        # Verify Load more button is visible
        load_more_visible = StoriesPageHelpers.verify_load_more_button_visible(driver, self.browser_name)
        assert load_more_visible, "Load more button not visible in Edge"

        # Check if more stories are available to load
        more_available = StoriesPageHelpers.check_if_load_more_available(driver, self.browser_name)

        # Get initial story count
        initial_count = StoriesPageHelpers.get_stories_count(driver, self.browser_name)
        print(f"{self.browser_name}: Initial story count: {initial_count}")
        assert initial_count > 0, "No stories found on page initially"

        # Click Load more button
        load_more_clicked = StoriesPageHelpers.click_load_more_button(driver, self.browser_name)
        assert load_more_clicked, "Could not click Load more button in Edge"

        # Wait for loading indicator to complete
        loading_complete = StoriesPageHelpers.wait_for_loading_complete(driver, self.browser_name)
        assert loading_complete, "Loading did not complete in Edge"

        # Verify additional stories loaded
        final_count = StoriesPageHelpers.get_stories_count(driver, self.browser_name)
        print(f"{self.browser_name}: Final story count: {final_count}")

        # If more stories were available, count should increase
        # If no more stories available, count staying the same is acceptable
        if more_available:
            assert final_count > initial_count, f"Stories not loaded: initial={initial_count}, final={final_count}"
            print(f"{self.browser_name}: Load more functionality verification passed - stories loaded")
        else:
            print(
                f"{self.browser_name}: Load more functionality verified - no more stories available to load (count: {final_count})")
            # Test passes because button worked even though no new stories loaded

    def test_api_section_displays_correctly_edge(self):
        """TC_003: Verify that 'API' section is displayed and only shows API-related stories in Edge"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Click on API section
        api_section_clicked = StoriesPageHelpers.click_api_section(driver, self.browser_name)
        assert api_section_clicked, "Could not click API section in Edge"

        # Wait for page to load
        time.sleep(2)
        TestUtils.wait_for_page_load(driver)

        # Verify only API-related stories are displayed
        api_stories_only = StoriesPageHelpers.verify_api_stories_displayed(driver, self.browser_name)
        assert api_stories_only, "Non-API stories found or no API stories displayed in Edge"

        print(f"{self.browser_name}: API section verification passed")

    def test_sort_button_opens_dropdown_edge(self):
        """TC_004: Verify that clicking Sort button opens sort dropdown/menu in Edge"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Locate and click Sort button
        sort_button_clicked = StoriesPageHelpers.click_sort_button(driver, self.browser_name)
        assert sort_button_clicked, "Could not click Sort button in Edge"

        # Verify sort dropdown/menu opens
        sort_menu_visible = StoriesPageHelpers.verify_sort_menu_visible(driver, self.browser_name)
        assert sort_menu_visible, "Sort dropdown/menu not visible in Edge"

        # Verify all sort options are visible
        all_options_visible = StoriesPageHelpers.verify_all_sort_options_visible(driver, self.browser_name)
        assert all_options_visible, "Not all sort options visible in Edge"

        print(f"{self.browser_name}: Sort button and dropdown verification passed")

    def test_filter_button_displays_categories_edge(self):
        """TC_005: Verify that All filter categories display correctly in Edge"""
        driver = self.driver
        driver.get(Constants.STORIES_URL)
        TestUtils.wait_for_page_load(driver)

        # Locate and click Filter button
        filter_button_clicked = StoriesPageHelpers.click_filter_button(driver, self.browser_name)
        assert filter_button_clicked, "Could not click Filter button in Edge"

        # Verify filter panel/dropdown opens
        filter_panel_visible = StoriesPageHelpers.verify_filter_panel_visible(driver, self.browser_name)
        assert filter_panel_visible, "Filter panel/dropdown not visible in Edge"

        # Verify all filter categories are displayed
        all_categories_visible = StoriesPageHelpers.verify_all_filter_categories(driver, self.browser_name)
        assert all_categories_visible, "Not all filter categories displayed in Edge"

        print(f"{self.browser_name}: Filter categories verification passed")

    def tearDown(self):
        """Clean up after each test"""
        TestUtils.safe_teardown(self.driver, self.browser_name)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(OpenAIStoriesChromeTest))
    suite.addTests(loader.loadTestsFromTestCase(OpenAIStoriesEdgeTest))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)