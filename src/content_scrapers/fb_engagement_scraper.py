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
from enum import Enum

# to add abstraction, maps to index of items in reactions_path array
class Media(Enum):
    POST = 0
    VIDEO = 1

''' Store xpath references to find reactions element in different types of fb media (posts, lives, reels) as keys
and then hold their different engagements '''
reactions_xpath = [ "//div[contains(text(), 'All reactions:')]/following-sibling::span[1]//span[text()]",
                    "//span[@aria-label='See who reacted to this' and @role='toolbar']/following-sibling::*[1]//span[text()]"
]
  
           
def extract_engagements_from_post(driver:webdriver.Chrome, post_type:Enum)->str:
    # for 
    try:
        
        #reactions = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, reactions_xpath[post_type.value])))
            # number of comments logo/container may not be expanded
         # number of shares/comments hidden in pseudo-element (css) sandwhiched between ::before and ::after tags
             # so doesn't exist in dom, must use javascript to find element
             # comments is first
        engagement_elements = driver.execute_script("""
            let metrics = [];
            const num_comments_shares = Array.from(document.querySelectorAll('[class^="html-span"]'));
            num_comments_shares.forEach(metric => {
                metrics.push(metric.textContent);
            });
            return metrics;
"""
        )
        print(engagement_elements)
    except Exception as e:
        print("Can't find reaction element!", e)

def get_reactions_from_video(driver:webdriver.Chrome)->str:
    try:
        num_reactions = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, "//span[@aria-label='See who reacted to this' and @role='toolbar']/following-sibling::*[1]//span[text()]")))
        return num_reactions.text
    except Exception as e:
        print("Can't find reaction element!", e)


def get_shares_from_post(driver:webdriver.Chrome):

    pass


if __name__ == '__main__':
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.facebook.com/corpuschristicronica/posts/pfbid031mgN8ToWXJu73vb4oFAhJoLQR4FgC4EURAKnfxFr7FTHBvdFvZWQHreVvn9TenzNl')
    print(extract_engagements_from_post(driver, "post"))
    # Close the browser
    input("finished")
    driver.quit()