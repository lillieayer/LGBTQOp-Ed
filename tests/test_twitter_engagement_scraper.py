import pytest
from src.scrapers.twitter_scraper import TwitterScraper

# *** Test Fixtures for Twitter Scraper ***

@pytest.fixture
def mock_tweet_scraper(mock_driver):
    yield TwitterScraper(mock_driver)

# mock data reactions, comments, shares etc updated on 12/29/2024
@pytest.fixture
def tweet_mock_data():
    yield {'LINK': "https://x.com/PlayStation/status/1870954467849351217", 'CONTENT': "Name a hidden gem video game you're always recommending 💎", 'AUTHOR': "PlayStation",'RETWEETS': 1400.0, 'REPLIES': 4800.0, 'LIKES': 14000.0 }

#*** Black Box Testing for Twitter Scraper ***
    
'''
    purpose: to test that Tweet Scraper object 
    returns correct metrics in dictionary format
    input: random tweet with 
    pass: manually logged metrics match scraping metrics''' 
def test_scrape_tweet_dict(mock_tweet_scraper, tweet_mock_data):
    try: 
        result = mock_tweet_scraper.extract_content_from_link(tweet_mock_data['LINK'])
        print(result)
    except Exception as e:
        print(e)
    assert result == tweet_mock_data

'''
purpose: to test that Tweet Scraper object 
returns correct metrics after scraping multiple times
in a row to ensure consistent results
input: random tweet  
pass: results match manually logged metrics each time''' 

def test_scrape_tweet_consistency(mock_tweet_scraper, tweet_mock_data):
    results = []
    for i in range(5):
        result = mock_tweet_scraper.extract_content_from_link(tweet_mock_data['LINK'])
        results.append(result)
    assert all(result == tweet_mock_data for result in results)
        