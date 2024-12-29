import pytest
from src.scrapers.twitter_scraper import TwitterScraper

# *** Test Fixtures for FB Scraper ***

@pytest.fixture
def mock_fb_scraper(mock_driver):
    return TwitterScraper(mock_driver)

# mock data reactions, comments, shares etc updated on 12/29/2024

@pytest.fixture(scope="module")
def tweet_mock_data():
    return {'LINK': "https://www.facebook.com/reel/592654566749105", 'REACTIONS': 3700.0, 'COMMENTS': 202.0, 'SHARES': 34.0 }

