import requests
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from utils.logger import Logger


class Article:
    """
    A class representing an article element on a webpage with methods to extract its content.

    This class provides functionality to interact with article elements, including retrieving
    the title, content, and downloading associated images.

    Attributes:
        TITLE (tuple): Locator tuple for the article title using CSS selector 'h2'
        CONTENT (tuple): Locator tuple for the article content using CSS selector 'p.c_d'
        IMAGE (tuple): Locator tuple for the article image using CSS selector 'img'

    Args:
        driver: The Selenium WebDriver instance
        element: The WebElement representing the article container
    """

    TITLE = (By.CSS_SELECTOR, "h2")
    CONTENT = (By.CSS_SELECTOR, "p.c_d")
    IMAGE = (By.CSS_SELECTOR, "img")

    def __init__(self, driver, element):
        """
        Initialize an Article instance.

        Args:
            driver: The Selenium WebDriver instance
            element: The WebElement representing the article container
        """
        self.driver = driver
        self.element = element
        self.logger = Logger(__name__)

    def get_title(self):
        """
        Retrieve the title of the article.

        Returns:
            str: The text content of the article title

        Raises:
            NoSuchElementException: If the title element cannot be found
            StaleElementReferenceException: If the element is no longer valid
        """
        self.logger.debug('Fetching title of article')
        return self.element.find_element(*self.TITLE).text

    def get_content(self):
        """
        Retrieve the main content of the article.

        Returns:
            str: The text content of the article

        Raises:
            NoSuchElementException: If the content element cannot be found
            StaleElementReferenceException: If the element is no longer valid
        """
        self.logger.debug('Fetching content of article')
        return self.element.find_element(*self.CONTENT).text

    def download_image(self, filename):
        """
        Download the article's image and save it to a file.

        Args:
            filename (str): The path where the image will be saved

        Returns:
            bool: True if the image was successfully downloaded and saved,
                 False if there was an error

        Raises:
            NoSuchElementException: If the image element cannot be found
            StaleElementReferenceException: If the element is no longer valid
            RequestException: If there's an error downloading the image
        """
        self.logger.debug(f'Attempt downloading image to {filename}')
        try:
            img = self.element.find_element(*self.IMAGE)
            img_url = img.get_attribute("src")
            img_data = requests.get(img_url).content
            with open(filename, "wb") as handler:
                handler.write(img_data)
            self.logger.debug('Image successfully saved')
            return True
        except NoSuchElementException as nse:
            # Handle Selenium exceptions when element is not found
            self.logger.debug(f"Failed to find image element: {str(nse)}")
            return False
        except StaleElementReferenceException as sere:
            # Note: The original file appears to be incomplete at this point
            self.logger.debug(f"Element is stale: {str(sere)}")
            return False
