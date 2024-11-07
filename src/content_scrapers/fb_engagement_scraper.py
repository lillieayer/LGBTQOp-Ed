from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fb_comment_scraper import *
from file_processors import *
from typing import Tuple
from enum import Enum
import os

'''
Note: for this engagement scraper you do not need to be logged in!
It's actually essential that you are not so that way the scraper doesn't
detect any posts in the background from the account'''
# to add abstraction, maps to index of items in reactions_path array

class Post(Enum):
    CONTENT = "//div[@data-ad-preview='message']//div[text()]"
    REACTIONS =  "//div[contains(text(), 'All reactions:')]/following-sibling::span[1]//span[text()]"
    COMMENTS_SHARES = "//div[@role='button']//span[starts-with(@class, 'html-span') and text()]"

# video content doesn't allow shares
class Video(Enum):
    # content doesn't work
   # CONTENT = "//div[@role='banner']/following-sibling::div[1]//div[not(@role='tablist') and not(@role='tab') and not(@role='none')]//span[text()]"
    REACTIONS = "//span[@aria-label='See who reacted to this' and @role='toolbar']/following-sibling::*[1]//span[text()]"
    COMMENTS = "//div[./span[@aria-label='See who reacted to this' and @role='toolbar']]/following-sibling::div[2]//span[text()]"

class Reel(Enum):
    # reactions and comments works
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
        if " " in count_label:
            count = count_label.split(' ')[0]
        count = float(count)
    return count
   

''' Purpose: to grab the comments and shares from a post 
''' 
def get_num_comments_shares_from_post(driver:webdriver.Chrome)-> Tuple[float,float]:
    # from xpath returns count of comments/shares --> also grabs comments/shares from posts in background/below
    engagements = WebDriverWait(driver, 10).until( EC.presence_of_all_elements_located((By.XPATH, Post.COMMENTS_SHARES.value)))
    comments = engagements[0].text
    shares = engagements[1].text
    count_comments = clean_metric(comments)
    count_shares = clean_metric(shares)
    return count_comments,count_shares
           
def find_num_engagements_from_post(driver:webdriver.Chrome, link:str,  post_type:Enum,)->dict:
    engagements = {'LINK':link}
    driver.get(link)
    # for 
    for metric in post_type:   
        if metric != Post.COMMENTS_SHARES:
            try:
                # gets first presence of element
                engagement = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, metric.value)))
                    # clean engagement count
                count = engagement.text
                if metric.name != "CONTENT":
                    count = clean_metric(count)
                engagements[metric.name] = count
            except Exception as e:
                print("Exception caught as", e)
            finally:
                # find next element
                continue

        else:
                # grabs comments and shares at the same time --> only occurs in fb posts DOM
            comments, shares = get_num_comments_shares_from_post(driver)
            engagements['COMMENTS'] = comments
            engagements['SHARES'] = shares
    return engagements

def extract_engagements_from_files(driver:webdriver.Chrome, dir:str):
    for file in os.listdir(dir):
        all_posts_links = extract_links_from_file(dir + '/' + file)
        narrative_insights = []
        
        for post_link in all_posts_links:
            if ('facebook.com/watch' in post_link) or ('fb.watch' in post_link):
                post_type = Video
            elif ('facebook.com/reel' in post_link) or ('fb.reel' in post_link):
                post_type = Reel
            else:
                post_type = Post

            assert post_type is not None, f"Error when analyzing post type in {post_link}"
            
            post_insights = find_num_engagements_from_post(driver, post_link, post_type)
            # add dictionary of each post info to narrative list
            narrative_insights.append(post_insights)
        filename = file.split('.')
        with open('./output/fb/' + filename[0] + '_engagements.json', 'w', encoding='utf-8') as engagement_file:
            json.dump(narrative_insights, engagement_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    extract_engagements_from_files(driver, './links')
    input("finished")
    driver.quit()