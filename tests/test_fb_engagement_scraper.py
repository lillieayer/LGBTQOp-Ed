import pytest
from src.scrapers.fb_scraper import FBScraper

# *** Test Fixtures for FB Scraper ***

@pytest.fixture
def mock_fb_scraper(mock_driver):
    yield FBScraper(mock_driver)

# mock data reactions, comments, shares etc updated on 12/29/2024

@pytest.fixture
def fb_reel_mock_data():
    yield {'LINK': "https://www.facebook.com/reel/592654566749105", 'REACTIONS': 3700.0, 'COMMENTS': 202.0, 'SHARES': 34.0 }

@pytest.fixture
def fb_post_mock_data():
   yield {'LINK': "https://www.facebook.com/photo/?fbid=1049350047232097&set=a.568969405270166", 'AUTHOR':'Memes', 'CONTENT': "Accurate.", 'REACTIONS': 6300.0, 'COMMENTS': 348.0, 'SHARES': 971.0 }

#*** Black Box Testing for FB Scraper ***
    
'''
    purpose: to test that FB Scraper object 
    returns correct metrics in dictionary format
    input: random facebook reel with 
    pass: manually logged metrics match scraping metrics''' 
def test_scrape_reel_dict(mock_fb_scraper, fb_reel_mock_data):
    try: 
        result = mock_fb_scraper.extract_content_from_link(fb_reel_mock_data['LINK'])
    except Exception as e:
        print(e)
    assert result == fb_reel_mock_data

'''
purpose: to test that FB Scraper object 
returns correct metrics after scraping multiple times
in a row to ensure consistent results
input: random facebook reel  
pass: results match manually logged metrics each time''' 

def test_scrape_reel_consistency(mock_fb_scraper, fb_reel_mock_data):
    results = []
    for i in range(5):
        result = mock_fb_scraper.extract_content_from_link(fb_reel_mock_data['LINK'])
        results.append(result)
    assert all(result == fb_reel_mock_data for result in results)
        
   
'''
    purpose: to test that FB Scraper object 
    returns correct metrics in dictionary format
    input: random facebook reel with 
    pass: manually logged metrics match scraping metrics''' 
def test_scrape_post_dict(mock_fb_scraper, fb_post_mock_data):
    try: 
        result = mock_fb_scraper.extract_content_from_link(fb_post_mock_data['LINK'])
    except Exception as e:
        print(e)
    assert result == fb_post_mock_data

'''
purpose: to test that FB Scraper object 
returns correct metrics after scraping multiple times
in a row to ensure consistent results
input: random facebook reel  
pass: results match manually logged metrics each time''' 

def test_scrape_post_consistency(mock_fb_scraper, fb_post_mock_data):
    results = []
    for i in range(5):
        result = mock_fb_scraper.extract_content_from_link(fb_post_mock_data['LINK'])
        results.append(result)
    assert all(result == fb_post_mock_data for result in results)


# *** White Box Testing for FB Scraper ***
        