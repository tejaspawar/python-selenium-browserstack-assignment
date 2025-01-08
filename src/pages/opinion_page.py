from selenium.webdriver.common.by import By

from utils.logger import Logger
from .article import Article
from .base_page import BasePage


class OpinionPage(BasePage):
    """
    Page object class representing the Opinion section of El País newspaper.

    This class provides methods to interact with and extract content from the Opinion
    section, particularly focusing on article retrieval.

    Attributes:
        ARTICLES (tuple): Locator tuple for finding article elements on the page using CSS selector
    """

    ARTICLES = (By.CSS_SELECTOR, "article.c-d")

    def __init__(self, driver):
        """
        Initialize the OpinionPage with a WebDriver instance.

        Args:
            driver: The Selenium WebDriver instance
        """
        super().__init__(driver)
        self.logger = Logger(__name__)

    def get_articles(self, count=5):
        """
        Retrieve a specified number of articles from the Opinion page.

        This method waits for article elements to be present on the page and returns
        a list of Article objects representing the first 'count' articles found.

        Args:
            count (int, optional): The number of articles to retrieve. Defaults to 5.

        Returns:
            list[Article]: A list of Article objects representing the found articles.

        Raises:
            TimeoutException: If the articles are not found within the default timeout period
        """
        self.logger.debug(f"Fetching {count} articles from Opinion page")
        article_elements = self.wait_for_all_presence(self.ARTICLES)[:count]
        return [Article(self.driver, element) for element in article_elements]
