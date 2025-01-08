import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.logger import Logger


class HomePage(BasePage):
    """
    Page object class representing El País newspaper homepage.

    This class provides methods to interact with various elements on the El País homepage,
    including language selection, navigation to different sections, and handling cookie popups.

    Attributes:
        URL (str): The base URL for El País website
        LANGUAGE_BUTTON (tuple): Locator for the language selection button
        LANGUAGE_DROPDOWN (tuple): Locator for the language dropdown menu
        SPANISH_OPTION (tuple): Locator for the Spanish language option
        OPINION_LINK (tuple): Locator for the Opinion section link
        AGREE_BUTTON (tuple): Locator for the cookie consent button
    """

    URL = "https://elpais.com/"
    LANGUAGE_BUTTON = (By.CSS_SELECTOR, "button[data-toggle='language-edition']")
    LANGUAGE_DROPDOWN = (By.XPATH, "//li[@id='edition_head']")
    SPANISH_OPTION = (By.XPATH, "//a[contains(@href, 'elpais.com/')]")
    SELECTED_LANGUAGE = (By.XPATH, "//li[@class='ed_c']")
    OPINION_LINK = (By.XPATH, "//*[@id='hamburger_container']//a[contains(@href, '/opinion/')]")
    AGREE_BUTTON_BROWSER = (By.ID, "didomi-notice-agree-button")  # browser only
    AGREE_BUTTON_IOS = (By.CLASS_NAME, "pmConsentWall-button")
    MENU_BUTTON_OPEN = (By.ID, "btn_open_hamburger")
    MENU_BUTTON_CLOSE = (By.ID, "btn_toggle_hamburger")

    def __init__(self, driver):
        """
        Initialize the HomePage with a WebDriver instance and navigate to the homepage.

        Args:
            driver: The Selenium WebDriver instance
        """
        super().__init__(driver)
        self.logger = Logger(__name__)
        self.driver.get(self.URL)

    def ensure_spanish_language(self):
        """
        Verify that the website is displayed in Spanish language.

        This method checks the current language setting of the webpage and asserts
        that it is set to Spanish (ESPAÑA).

        Raises:
            AssertionError: If the webpage is not in Spanish language
        """
        self.logger.debug('Ensure the website is in Spanish')
        language = self.driver.find_element(By.XPATH, "//html").get_attribute('lang')
        assert language == 'es-ES', f"Webpage loaded in [{language}]"

    def go_to_opinion_section(self):
        """
        Navigate to the Opinion section of the website.

        This method clicks on the Opinion section link and waits for the navigation
        to complete.
        """
        self.logger.debug("Navigating to Opinion section")
        self.wait_and_click(self.MENU_BUTTON_OPEN)

        options_link = self.driver.find_element(*self.OPINION_LINK)
        # Scroll till 'Opinion' section from hamburger menu, this is required for small screen devices or when
        # device orientation changed to landscape
        self.driver.execute_script("arguments[0].scrollIntoView();", options_link)
        self.wait_and_click(self.OPINION_LINK)

    def handle_cookie_popup(self):
        """
        Handle the cookie consent popup by accepting it.

        This method waits for the cookie popup to appear and clicks the accept button.
        If the popup doesn't appear within 30 seconds, it will raise a TimeoutException.

        Raises:
            TimeoutException: If the cookie popup doesn't appear within the timeout period
        """
        try:
            self.logger.debug("Wait for the cookie pop-up to appear and find the accept button")
            accept_button = self.wait_for_presence_any(locator_list=[self.AGREE_BUTTON_IOS, self.AGREE_BUTTON_BROWSER], timeout=10)
            accept_button.click()
        except Exception as e:
            self.logger.debug(f"Error handling cookie popup: {str(e)}")
            raise
