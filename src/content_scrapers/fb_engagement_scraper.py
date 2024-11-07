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

# to add abstraction, maps to index of items in reactions_path array

class Post(Enum):
    CONTENT = "//div[@data-ad-preview='message']//div[text()]"
    REACTIONS =  "//div[contains(text(), 'All reactions:')]/following-sibling::span[1]//span[text()]"
    COMMENTS_SHARES = "//div[@role='button']//span[starts-with(@class, 'html-span') and text()]"

# video content doesn't allow shares
class Video(Enum):
    # content and comments doesn't work
    CONTENT = "//div[@role='banner']/following-sibling::div[1]//div[not(@role='tablist') and not(@role='tab') and not(@role='none')]//span[text()]"
    REACTIONS = "//span[@aria-label='See who reacted to this' and @role='toolbar']/following-sibling::*[1]//span[text()]"
    COMMENTS = "//div[@role='button]//span[contains(text(),'comments')]"

class Reel(Enum):
    # reactions and comments works
    REACTIONS = "//div[./div[starts-with(@aria-label, 'Like') and @role='button']]/following-sibling::div[1]//span[text()]"
    COMMENTS = "//div[./div[starts-with(@aria-label, 'Comment') and @role='button']]/following-sibling::div[1]//span[text()]"
    SHARES = "(//div[.//div[starts-with(@aria-label, 'Comment') and @role='button']])[1]/following-sibling::div[1]//span[text()]"

''' Purpose: to grab the comments and shares from a post 
''' 
def get_num_comments_shares_from_post(driver:webdriver.Chrome)-> Tuple[str,str]:
    # from xpath returns count of comments/shares --> also grabs comments/shares from posts in background/below
    engagements = WebDriverWait(driver, 10).until( EC.presence_of_all_elements_located((By.XPATH, Post.COMMENTS_SHARES.value)))
    comments = engagements[0].text
    shares = engagements[1].text
    return comments,shares
           
def find_num_engagements_from_post(driver:webdriver.Chrome, link:str,  post_type:Enum,)->str:
    engagements = {'LINK':link}
    driver.get(link)
    # for 
    try:
        for metric in post_type:
            
            if metric != Post.COMMENTS_SHARES:
                # gets first presence of element
                engagement = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, metric.value)))
                engagements[metric.name] = engagement.text
            else:
                # grabs comments and shares at the same time --> only occurs in fb posts DOM
                comments, shares = get_num_comments_shares_from_post(driver)
                engagements['COMMENTS'] = comments
                engagements['SHARES'] = shares
        return engagements
    except Exception as e:
        print("Can't find reaction element!", e)

def extract_engagements_from_files(driver:webdriver.Chrome, dir:str):
    files = ['lakewood_church_shooter.txt']
    #for file in os.listdir(dir):
    for file in files:
        all_posts_links = extract_links_from_file(dir + '/' + file)
        narrative_insights = []
        
        for post_link in all_posts_links:
            if ('facebook.com/watch' in post_link) or ('fb.com/watch' in post_link):
                post_type = Video
            elif ('facebook.com/reel' in post_link) or ('fb.com/reel' in post_link):
                post_type = ""
            else:
                post_type = Post

            assert post_type is not None, f"Error when analyzing post type in {post_link}"
            
            post_insights = find_num_engagements_from_post(driver, post_link, post_type)
            # add dictionary of each post info to narrative list
            narrative_insights.append(post_insights)
        filename = file.split('.')
        with open('./output/fb' + filename[0] + '_engagements.json', 'w', encoding='utf-8') as engagement_file:
            json.dump(narrative_insights, engagement_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    # test reels
    link = "https://www.facebook.com/reel/2380911872082021"
    driver.get(link)
    e = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH,Reel.SHARES.value)))
    print(e.text)
    #extract_engagements_from_files(driver, './links')
    # Close the browser
    input("finished")
    driver.quit()