import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.scrapers.fb_scraper import FBScraper

@pytest.fixture(scope="module")
def mock_driver():
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  return webdriver.Chrome(options = chrome_options)
