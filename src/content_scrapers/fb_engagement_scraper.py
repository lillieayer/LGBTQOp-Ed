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

''' Scraper gets the number of comments, reactions and shares from a post '''

def get_reactions_from_post(driver:webdriver.Chrome)->str:
    try:
        num_reactions = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'All reactions:')]/following-sibling::span[1]//span[text()]")))
        return num_reactions.text
    except Exception as e:
        print("Can't find reaction element!", e)

def get_reactions_from_video(driver:webdriver.Chrome)->str:
    try:
        num_reactions = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, "//span[@aria-label='See who reacted to this' and @role='toolbar']/following-sibling::*[1]//span[text()]")))
        return num_reactions.text
    except Exception as e:
        print("Can't find reaction element!", e)


if __name__ == '__main__':
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.facebook.com/watch/live/?ref=watch')
    print(get_reactions_from_video(driver))
    # Close the browser
    input("finished")
    driver.quit()