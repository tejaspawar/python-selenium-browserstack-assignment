# Elpais Website Scraper with Title Analysis

A Python-based web scraping tool that extracts article titles, translates them, and performs word frequency analysis. The project uses Selenium WebDriver with BrowserStack integration for robust web scraping.

## Features
- Automated web scraping with configurable article limits
- Title translation capability
- Word frequency analysis of translated titles
- Rate limiting to prevent API overwhelming
- BrowserStack integration for reliable testing
- Comprehensive error handling and logging
- Automated session status reporting

## Prerequisites
- Python 3.x
- Selenium WebDriver
- BrowserStack account
- Required Python packages:
  - selenium
  - json
  - time
  - re
  - collections
  - logging

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tejaspawar/python-selenium-browserstack-assignment.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
## Configuration
1. Set up BrowserStack credentials 
   
- Option 1: in browserstack.yml:
```yaml
userName: "your_username"
accessKey: "your_access_key"
```
- Option 2: You can also export them as environment variables, BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY

 For Linux/ MacOS:
```bash
export BROWSERSTACK_USERNAME=<browserstack-username>
export BROWSERSTACK_ACCESS_KEY=<browserstack-access-key>
````
For Windows
```bash
setx BROWSERSTACK_USERNAME=<browserstack-username>
setx BROWSERSTACK_ACCESS_KEY=<browserstack-access-key>
````

2. Update API key for using translation services
   You need to export it as environment variable, TRANSLATOR_API_KEY

 For Linux/ MacOS:
```bash
export TRANSLATOR_API_KEY=<your_translator_api_key>
````
For Windows
```bash
setx TRANSLATOR_API_KEY=<your_translator_api_key>
````
3. Configure scraping parameters in `elpais_scrapper.py`:
```python
MAX_ARTICLE_TO_SCRAPE = 5  # Adjust as needed
```

## Usage
The scraper performs the following operations:

 - Ensures website loads in spanish language
 - Extracts titles from web pages
 - Translates the extracted titles 
 - Implements rate limiting (1-second delay between requests)
 - Analyzes word frequency in translated titles 
 - Reports words that appear more than twice 
 - Updates BrowserStack session status

## Run the scraper:

To run the sample test across platforms defined in the browserstack.yml file, run:

```python
browserstack-sdk src/elpais_scrapper.py
```

## Error Handling
The script handles various exceptions:
 - StaleElementReferenceException for dynamic page elements 
 - General exceptions with detailed logging 
 - BrowserStack session status updates for both success and failure cases

## Logging
The script provides comprehensive logging:
 - Debug level: Detailed operation tracking 
 - Info level: Important milestones and results 
 - Error level: Exception details and failures

## Output Example
Repeated words in translated headers:
 - word1: 3
 - word2: 4
 - ...


