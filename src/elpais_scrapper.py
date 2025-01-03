import json
import os
import re
import sys
import time
from collections import Counter

import selenium
from selenium import webdriver

from pages.home_page import HomePage
from pages.option_page import OpinionPage
from utils.logger import Logger
from utils.translator import Translator

MAX_ARTICLE_TO_SCRAPE = 5
IMAGE_DOWNLOAD_LOCATION = 'data' + os.sep + 'images' + os.sep

def scrape_elpais():
    logger = Logger(__name__)

    driver = webdriver.Chrome()
    translator = Translator()

    try:
        logger.info("Navigating to home page and ensuring Spanish language")
        home_page = HomePage(driver)
        home_page.handle_cookie_popup()
        home_page.ensure_spanish_language()
        home_page.go_to_opinion_section()

        logger.info("Fetching articles from Opinion section")
        opinion_page = OpinionPage(driver)

        # Create images directory if it doesn't exist
        os.makedirs(IMAGE_DOWNLOAD_LOCATION, exist_ok=True)
        translated_titles = []

        try:
            # We will retrieve more articles to handle StaleElementReferenceException
            articles = opinion_page.get_articles(2 * MAX_ARTICLE_TO_SCRAPE)
            articles_scrapped = 0
            # Process each article
            for i, article in enumerate(articles, 1):
                title = article.get_title()
                content = article.get_content()

                logger.debug(f"Title (Spanish): {title}")
                logger.debug(f"Content (Spanish): {content}")

                if article.download_image(f"{IMAGE_DOWNLOAD_LOCATION}article_{i}_image.jpg"):
                    logger.info(f"Image for article [{title}] saved as article_{i}_image.jpg")
                else:
                    logger.info(f"No image available for [{title}] article")

                translated_title = translator.translate(title)
                logger.debug(f"Title (English): {translated_title}")

                translated_titles.append(translated_title)
                logger.debug('Add a delay to avoid overwhelming the API')
                time.sleep(1)
                articles_scrapped += 1
                if articles_scrapped >= MAX_ARTICLE_TO_SCRAPE:
                    logger.info(f"Reached the maximum number of articles to scrape: {MAX_ARTICLE_TO_SCRAPE}")
                    break
        except selenium.common.exceptions.StaleElementReferenceException:
            logger.error("Stale element reference encountered. Skipping this article.")


        logger.debug('Analyze translated titles')
        logger.debug(f'translated_titles: {translated_titles}')
        all_words = " ".join(translated_titles).lower()
        all_words_clean = re.findall(r'\w+', all_words)  # keep only alphanumeric characters
        word_count = Counter(all_words_clean)

        logger.debug(f'all_words: {all_words}')
        logger.debug(f'word_counts: {word_count}')
        logger.info("Repeated words in translated headers:")
        for word, count in word_count.items():
            if count > 2:  # and len(word) > 3:  # Ignore short words like "the", "and", etc.
                logger.info(f"{word}: {count}")
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": '
            '"website scraping successful"}}')
    except Exception as err:
        message = 'Exception: ' + str(err.__class__) + str(err)
        logger.error(json.dumps(message))
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": '
            + json.dumps(message) + '}}')

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_elpais()
