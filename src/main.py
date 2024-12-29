from scrapers.fb_scraper import *
from scrapers.twitter_scraper import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


'''
Scrapes the OP-Ed specific data from the 
links folder and organizes the performance metrics into 
json files in the output folder
'''
def scrape_lgbtq_data():
    # start web driver for scraping
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    # setup scrapers 
    fb_scraper = FBScraper(driver)
    twitter_scraper = TwitterScraper(driver)

    fb_scraper.extract_content_from_files('./links/fb/','./output/fb/', 'engagements' )
    fb_scraper.extract_content_from_files('./links/control/fb/','./output/control/', 'engagements' )
    twitter_scraper.extract_content_from_files('./links/twitter/', './output/twitter/', 'engagements')
    twitter_scraper.extract_content_from_files('./links/control/twitter/', './output/control/', 'engagements')
    # finish web driver for scraping
    input("finished")
    driver.quit()

if __name__ == "__main__":
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    twitter_scraper = TwitterScraper(driver)
    result = twitter_scraper.extract_content_from_link('https://x.com/charliekirk11/status/1826463097005244852')
    print(result)
    


    # now visualize
