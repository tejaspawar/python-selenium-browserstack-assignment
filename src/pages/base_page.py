from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec

class BasePage:
    """
    A base page class that provides common web element interaction methods using Selenium WebDriver.

    This class implements wrapper methods for common Selenium WebDriver wait operations
    and element interactions. It serves as a foundation for page object classes.

    Args:
        driver: The Selenium WebDriver instance to be used for browser interactions

    Attributes:
        driver: The WebDriver instance used to interact with the browser
    """

    def __init__(self, driver):
        """
        Initialize the BasePage with a WebDriver instance.

        Args:
            driver: The Selenium WebDriver instance
        """
        self.driver = driver

    def wait_and_click(self, locator, timeout=10):
        """
        Wait for an element to be clickable and then click it.

        Args:
            locator (tuple): A tuple of (By strategy, locator string) to find the element
            timeout (int, optional): Maximum time to wait for the element. Defaults to 10 seconds

        Returns:
            None

        Raises:
            TimeoutException: If the element is not clickable within the timeout period
        """
        element = WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(locator)
        )
        element.click()

    def wait_for_presence(self, locator, timeout=10):
        """
        Wait for an element to be present in the DOM.

        Args:
            locator (tuple): A tuple of (By strategy, locator string) to find the element
            timeout (int, optional): Maximum time to wait for the element. Defaults to 10 seconds

        Returns:
            WebElement: The found web element

        Raises:
            TimeoutException: If the element is not present within the timeout period
        """
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(locator)
        )

    def wait_for_presence_any(self, locator_list, timeout=10):
        """
        Wait for any element from a list of locators to be present in the DOM.

        Args:
            locator_list (list[tuple]): A list of (By strategy, locator string) tuples to find the elements
            timeout (int, optional): Maximum time to wait for the elements. Defaults to 10 seconds

        Returns:
            WebElement: The first found web element

        Raises:
            TimeoutException: If none of the elements are present within the timeout period
        """
        for locator in locator_list:
            try:
                self.wait_for_presence(locator, timeout)
                return self.driver.find_element(*locator)
            except:
                continue


    def scroll_to_element(self, locator, timeout=10):
        """
        Scroll page till element is visible.

        Args:
            locator (tuple): A tuple of (By strategy, locator string) to find the element
            timeout (int, optional): Maximum time to wait for the element. Defaults to 10 seconds

        Returns:
            None

        Raises:
            TimeoutException: If the element is not present within the timeout period
        """
        element = self.driver.find_element(*locator)
        actions = ActionChains(self.driver)
        actions.scroll_to_element(element).perform()


    def wait_to_be_clickable(self, locator, timeout=10):
        """
        Wait for an element to be clickable.

        Args:
            locator (tuple): A tuple of (By strategy, locator string) to find the element
            timeout (int, optional): Maximum time to wait for the element. Defaults to 10 seconds

        Returns:
            WebElement: The clickable web element

        Raises:
            TimeoutException: If the element is not clickable within the timeout period
        """
        return WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(locator)
        )

    def wait_for_all_presence(self, locator, timeout=10):
        """
        Wait for all elements matching the locator to be present in the DOM.

        Args:
            locator (tuple): A tuple of (By strategy, locator string) to find the elements
            timeout (int, optional): Maximum time to wait for the elements. Defaults to 10 seconds

        Returns:
            list[WebElement]: A list of found web elements

        Raises:
            TimeoutException: If the elements are not present within the timeout period
        """
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_all_elements_located(locator)
        )
