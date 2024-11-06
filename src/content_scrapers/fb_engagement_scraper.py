from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv, dotenv_values 
from fb_comment_scraper import *
from typing import Tuple
from enum import Enum

# to add abstraction, maps to index of items in reactions_path array

class Post(Enum):
    TITLE = "//div[@role='dialog']//h2//span[text()]"
    REACTIONS =  "//div[@role='dialog']//div[contains(text(), 'All reactions:')]/following-sibling::span[1]//span[text()]"
    COMMENTS_SHARES = "//div[@role='button']//span[starts-with(@class, 'html-span') and text()]"
class Video(Enum):
    TITLE = "//div[@id='watch_feed']//span[text()]"
    REACTIONS = "//span[@aria-label='See who reacted to this' and @role='toolbar']/following-sibling::*[1]//span[text()]"
    COMMENTS = "//div[@role='button]//span[contains(text(),'comments')]"

  
def get_num_comments_shares_from_post(driver:webdriver.Chrome)-> Tuple[str,str]:
    engagements = WebDriverWait(driver, 10).until( EC.presence_of_all_elements_located((By.XPATH, 
                                                                                        )))
    comments = engagements[0].text
    shares = engagements[1].text
    return comments,shares
           
def extract_num_engagements_from_post(driver:webdriver.Chrome, post_type:Enum)->str:
    engagements = {}
    # for 
    try:
        for metric in post_type:
            if metric.name != post_type.COMMENTS:
                # gets first presence of element
                engagement = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, metric.value)))
                engagements[metric.name] = engagement.text
            else:
                # grabs comments and shares at the same time --> only occurs in fb posts DOM
                comments, shares = get_num_comments_shares_from_post(driver)
                engagements['COMMENTS'] = comments
                engagements['SHARES'] = shares
        print(engagements)
        

    except Exception as e:
        print("Can't find reaction element!", e)


if __name__ == '__main__':
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    login_to_facebook(driver)
    driver.get('https://www.facebook.com/permalink.php?story_fbid=pfbid02sSKEQDhuir19DXixnBJv6XAGfHMfyK89YA5t1GvtWUBo3nUC9USdagW3E9pK2oKGl&id=61553573245040')
    extract_num_engagements_from_post(driver)
    # Close the browser
    input("finished")
    driver.quit()