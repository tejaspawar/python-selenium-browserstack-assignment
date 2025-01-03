import os
from http import HTTPStatus
from pathlib import Path

import requests
import yaml

from utils.logger import Logger


class Translator:
    """
    A class that provides text translation functionality using the Rapid Translate API.

    This class handles translation requests between different languages using
    the Rapid Translate Multi Traduction API service.

    Attributes:
        logger: Logger instance for tracking translation operations
        url (str): The endpoint URL for the translation API
    """

    def __init__(self):
        """
        Initialize the Translator with logger and API endpoint configuration.
        """
        self.logger = Logger(__name__)

        self.api_key = os.environ.get('TRANSLATOR_API_KEY')
        if self.api_key is None:
            self.logger.error('TRANSLATOR_API_KEY environment variable not set')
            raise ValueError('TRANSLATOR_API_KEY environment variable not set')

        # rapid-translate-multi-traduction APIs
        self.host = 'rapid-translate-multi-traduction.p.rapidapi.com'

        self.url = f"https://{self.host}/t"

    def translate(self, text, source_lang='ES', target_lang='EN'):
        """
        Translate text from source language to target language.

        Makes a POST request to the Rapid Translate API to translate the given text.

        Args:
            text (str): The text to be translated
            source_lang (str, optional): The source language code. Defaults to 'ES' (Spanish)
            target_lang (str, optional): The target language code. Defaults to 'EN' (English)

        Returns:
            str: The translated text

        Raises:
            requests.exceptions.RequestException: If the API request fails
            ValueError: If the API response is invalid or cannot be parsed
        """
        self.logger.debug(f'Translating text: [{text}] to {target_lang} by sending request to {self.url}')
        translation = ''
        payload = {
            "from": source_lang,
            "to": target_lang,
            "q": [text]
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }

        response = requests.post(self.url, json=payload, headers=headers)
        if response.status_code == HTTPStatus.OK:
            self.logger.debug('API request successful')
            self.logger.debug(f'response.json: [{response.json()}]')
            # we send single string to translate, hence get only the first
            # element form json
            translation = response.json()[0]
        elif response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            self.logger.error('API request throttled from server side')
            self.logger.error(f'response.json: [{response.json()}]')
        else:
            self.logger.error('API request failed')
            self.logger.error(f'response status: [{response.status_code}]')
            self.logger.error(f'response.text: [{response.text}]')
        return translation
