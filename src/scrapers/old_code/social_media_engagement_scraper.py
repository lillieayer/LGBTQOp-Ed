from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from file_processors import *
from typing import Tuple
from enum import Enum
import os,json

'''
Note: for this engagement scraper you do not need to be logged in!
It's actually essential that you are not so that way the scraper doesn't
detect any posts in the background from the account'''



# Enums define the XPaths to find certain insights/info about a social media type
class Tweet(Enum):
    CONTENT = "//article//div[@data-testid='tweetText']//span[text()]"
    AUTHOR = "//div[@data-testid='User-Name']//a[@role='link']//span[text()]"
    RETWEETS_QUOTES_LIKES = "//div[@role='group']//a//span[text()]"
    DATE = "//a[@role='link']//time"

class FBPost(Enum):
    AUTHOR = "//div[@data-ad-rendering-role='profile_name']//h2//a[@role='link']//strong/span[text()]"
    CONTENT = "//div[@data-ad-preview='message']//div[text()]"
    REACTIONS =  "//div[contains(text(), 'All reactions:')]/following-sibling::span[1]//span[text()]"
    COMMENTS_SHARES = "//div[@role='button']//span[starts-with(@class, 'html-span') and text()]"

# video content doesn't allow public share metrics
class FBVideo(Enum):
    # content doesn't work
   # CONTENT = "//div[@role='banner']/following-sibling::div[1]//div[not(@role='tablist') and not(@role='tab') and not(@role='none')]//span[text()]"
    REACTIONS = "//span[@aria-label='See who reacted to this' and @role='toolbar']/following-sibling::*[1]//span[text()]"
    COMMENTS = "//div[./span[@aria-label='See who reacted to this' and @role='toolbar']]/following-sibling::div[2]//span[text()]"

class FBReel(Enum):
    REACTIONS = "//div[./div[starts-with(@aria-label, 'Like') and @role='button']]/following-sibling::div[1]//span[text()]"
    COMMENTS = "//div[./div[starts-with(@aria-label, 'Comment') and @role='button']]/following-sibling::div[1]//span[text()]"
    SHARES = "//div[./div[starts-with(@aria-label, 'Share') and @role='button']]/following-sibling::div[1]//span[text()]"

def clean_metric(count_label:str)->float:
    count = count_label
    if 'K' in count_label:
        i = count_label.index('K')
        count = count_label[0:i]
        count = float(count)
        count *= 1000
    else:
        if " " in count:
            count = count_label.split(' ')[0]
        if ',' in count:
            count = count.replace(',','')
        count = float(count)
    return count
   
def get_num_engagements_from_tweet(driver:webdriver.Chrome)->Tuple[float, float, float]:
    
    engagements = WebDriverWait(driver, 10).until( EC.presence_of_all_elements_located((By.XPATH, Tweet.RETWEETS_QUOTES_LIKES.value)))
    retweets = clean_metric(engagements[0].text)
    quotes = clean_metric(engagements[2].text)
    likes = clean_metric(engagements[4].text)
    return retweets, quotes, likes


''' Purpose: to grab the comments and shares from a fb post 
''' 
def get_num_comments_shares_from_fb_post(driver:webdriver.Chrome)-> Tuple[float,float]:
    # from xpath returns count of comments/shares --> also grabs comments/shares from posts in background/below
    engagements = WebDriverWait(driver, 10).until( EC.presence_of_all_elements_located((By.XPATH, FBPost.COMMENTS_SHARES.value)))
    comments = engagements[0].text
    shares = engagements[1].text
    count_comments = clean_metric(comments)
    count_shares = clean_metric(shares)
    return count_comments,count_shares
           
def find_num_engagements_from_link(driver:webdriver.Chrome, link:str,  post_type:Enum, failures:dict[str, list[str]])->dict:
    engagements = {'LINK':link}
    driver.get(link)
    # for 
    for metric in post_type:
        try: 
            if metric == Tweet.RETWEETS_QUOTES_LIKES:
                retweets, quotes, likes = get_num_engagements_from_tweet(driver)
                engagements['RETWEETS'] = retweets
                engagements['QUOTES'] = quotes
                engagements['LIKES'] = likes
    
            elif metric != FBPost.COMMENTS_SHARES:
                    # gets first presence of element
                engagement = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, metric.value)))
                        # clean engagement count
                count = engagement.text
                if (metric.name != "CONTENT") and (metric.name != "AUTHOR") and (metric.name != 'DATE'):
                    count = clean_metric(count)
                engagements[metric.name] = count
            else:
                    # grabs comments and shares at the same time --> only occurs in fb posts DOM
                comments, shares = get_num_comments_shares_from_fb_post(driver)
                engagements['COMMENTS'] = comments
                engagements['SHARES'] = shares
        except Exception as e:
            # notify console of failure
            print(f"** Scraping failure for: {link} **")
            print(f"{metric.name} failed to be scraped.")
            ## debug recording failures
            if link in failures: 
                failures[link].append(metric.name)
            else:
                failures[link] = [metric.name]
            # find next metric
            continue

            
    return engagements

def extract_engagements_from_files(driver:webdriver.Chrome, dir:str):
    all_failed_links = []
    for file in os.listdir(dir):
        all_posts_links = extract_links_from_file(dir + '/' + file)
        narrative_insights = []
        # records failed links per narrative
        failed_links = {}
        if 'twitter' in dir:
            post_type = Tweet
            folder = 'twitter'
        else:
            folder = 'fb'
        
        for post_link in all_posts_links:
            # if analyzing fb links must check each for media type
            if folder == 'fb':
                if ('facebook.com/watch' in post_link) or ('fb.watch' in post_link) or ('/videos/' in post_link):
                    post_type = FBVideo
                elif ('facebook.com/reel' in post_link) or ('fb.reel' in post_link):
                    post_type = FBReel
                else:
                    post_type = FBPost

            assert post_type is not None, f"Error when analyzing post type in {post_link}"
            post_insights = find_num_engagements_from_link(driver, post_link, post_type, failed_links)
            # add dictionary of each post info to narrative list
            narrative_insights.append(post_insights)
            # record narratives failed links
        all_failed_links.append(failed_links)
        filename = file.split('.')
        with open('./output/high_volume/' + folder + '/' + filename[0] + '_engagements.json', 'w', encoding='utf-8') as engagement_file:
            json.dump(narrative_insights, engagement_file, ensure_ascii=False, indent=4)
    with open('./output/high_volume/' + folder + '/' + 'failed_links.json', 'w', encoding='utf-8') as failed_links_file:
            json.dump(all_failed_links, failed_links_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    extract_engagements_from_files(driver, "./links/twitter/")
    input("finished")
    driver.quit()