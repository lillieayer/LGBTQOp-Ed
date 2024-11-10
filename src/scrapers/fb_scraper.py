from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
from enum import Enum
from content_scraper import *


'''
*** Subclass FBScraper ***
@author: Lillie Ayer

** Purpose:
implements ContentScraperInterface with supporting implementations for scraping various post types on faceook'''

class FBScraper(ContentScraperInterface):

    # define media enums --> constant xpaths for finding dif web elements in the DOM
    class FBPost(Enum):
        AUTHOR = "//div[@data-ad-rendering-role='profile_name']//h2//a[@role='link']//strong/span[text()]"
        CONTENT = "//div[@data-ad-preview='message']//div[text()]"
        REACTIONS =  "//div[contains(text(), 'All reactions:')]/following-sibling::span[1]//span[text()]"
        COMMENTS_SHARES = "//div[@role='button']//span[starts-with(@class, 'html-span') and text()]"

    # video content doesn't show public shares
    class FBVideo(Enum):
        # CONTENT = "//div[@role='banner']/following-sibling::div[1]//div[not(@role='tablist') and not(@role='tab') and not(@role='none')]//span[text()]"
        REACTIONS = "//span[@aria-label='See who reacted to this' and @role='toolbar']/following-sibling::*[1]//span[text()]"
        COMMENTS = "//div[./span[@aria-label='See who reacted to this' and @role='toolbar']]/following-sibling::div[2]//span[text()]"

    class FBReel(Enum):
        REACTIONS = "//div[./div[starts-with(@aria-label, 'Like') and @role='button']]/following-sibling::div[1]//span[text()]"
        COMMENTS = "//div[./div[starts-with(@aria-label, 'Comment') and @role='button']]/following-sibling::div[1]//span[text()]"
        SHARES = "//div[./div[starts-with(@aria-label, 'Share') and @role='button']]/following-sibling::div[1]//span[text()]"

    def __init__(self, driver=None):
        super().__init__(driver)
    

    # override superclass method for extracting engagements from fb posts/reels/lives
    # @Override
    def extract_content_from_link(self, link:str)->dict:
        # setup scraper using superclass implementation
        engagements = super().extract_content_from_link(link)
        # identify specific media type for locating web elements
        if ('facebook.com/watch' in link) or ('fb.watch' in link) or ('/videos/' in link):
            post_type = self.FBVideo
        elif ('facebook.com/reel' in link) or ('fb.reel' in link):
            post_type = self.FBReel
        else:
            post_type = self.FBPost
        
        for metric in post_type:
            try:
                if metric != self.FBPost.COMMENTS_SHARES:
                    # gets first presence of element
                    engagement = WebDriverWait(self.driver, 10).until( EC.presence_of_element_located((By.XPATH, metric.value)))
                    # clean engagement count
                    count = engagement.text
                    if (metric.name != "CONTENT") and (metric.name != "AUTHOR"):
                        count = super().clean_metric(count)
                    engagements[metric.name] = count
                else:
                    # grabs comments and shares at the same time --> only occurs in fb posts DOM
                    fb_insights = WebDriverWait(self.driver, 10).until( EC.presence_of_all_elements_located((By.XPATH, FBScraper.FBPost.COMMENTS_SHARES.value)))
                    engagements['COMMENTS'] = super().clean_metric(fb_insights[0].text)
                    engagements['SHARES'] = super().clean_metric(fb_insights[1].text)
            
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