import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv, dotenv_values 
from fb_comment_scraper import *

''' Scraper gets the number of comments, reactions and shares from a post '''

def get_reactions_from_post(driver:webdriver.Chrome):
    try:
        num_reactions = driver.find_element(By.XPATH, "//*div[@text'button']//div[contains(text(), 'All reactions:')]/following-sibling::span[1]/descendant::span[1]/descendant::span[1]")
        print(num_reactions)
    except Exception as e:
        print("Can't find element", e)


if __name__ == '__main__':
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    login_to_facebook(driver)
    driver.get(link)
    get_reactions_from_post(driver)
    # Close the browser
    input("finished")
    driver.quit()