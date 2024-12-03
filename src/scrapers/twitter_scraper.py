from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from enum import Enum
from .content_scraper import * 

'''
    *** Subclass TwitterScraper ***
    @author: Lillie Ayer
    
    ** Purpose: implements ContentScraperInterface with supporting implementations for scraping tweets on twitter

'''

class TwitterScraper(ContentScraperInterface):
    # Enums define the XPaths to find certain insights/info about a tweet
    class Tweet(Enum):
        CONTENT = "//article//div[@data-testid='tweetText']//span[text()]"
        AUTHOR = "//div[@data-testid='User-Name']//a[@role='link']//span[text()]"
        RETWEETS_QUOTES_LIKES = "//div[@role='group']//a//span[text()]"

    def __init__(self, driver=None):
        super().__init__(driver)
        
    
    # override superclass method for extracting engagements from twitter posts
    # @Override
    def extract_content_from_link(self, link):
        engagements = super().extract_content_from_link(link)
    
        # get content and author
        for metric in self.Tweet:
            try:
                if metric != self.Tweet.RETWEETS_QUOTES_LIKES:
                    tweet_info = WebDriverWait(self.driver, 10).until( EC.presence_of_element_located((By.XPATH, metric.value)))
                    engagements[metric.name] = tweet_info.text
                else:
                    # get retweets, quotes and likes
                    tweet_reactions = WebDriverWait(self.driver, 10).until( EC.presence_of_all_elements_located((By.XPATH, self.Tweet.RETWEETS_QUOTES_LIKES.value)))
                    engagements['RETWEETS'] = super().clean_metric(tweet_reactions[0].text)
                    engagements['QUOTES'] = super().clean_metric(tweet_reactions[2].text)
                    engagements['LIKES'] = super().clean_metric(tweet_reactions[4].text)
            except Exception as e:
                # notify console of failure
                print(f"** Scraping failure for: {link} **")
                print(f"{metric.name} failed to be scraped.")
                ## debug recording failures
                '''if link in failures: 
                    failures[link].append(metric.name)
                else:
                    failures[link] = [metric.name]'''
                # find next metric
                continue
        return engagements