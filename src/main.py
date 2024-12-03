from scrapers import fb_scraper
from scrapers import twitter_scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options




''' This file is the main file which handles creating the scraper objects and scraping all data from links'''

if __name__ == "__main__":
    # start web driver for scraping
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    # setup scrapers 
    fb_scraper = fb_scraper.FBScraper(driver)
    twitter_scraper = twitter_scraper.TwitterScraper(driver)

    fb_scraper.extract_content_from_files('./links/fb/','./output/fb/', 'engagements' )
    fb_scraper.extract_content_from_files('./links/control/fb/','./output/control/', 'engagements' )
    twitter_scraper.extract_content_from_files('./links/twitter/', './output/twitter/', 'engagements')
    twitter_scraper.extract_content_from_files('./links/control/twitter/', './output/control/', 'engagements')
    # finish web driver for scraping
    input("finished")
    driver.quit()

    # now process dataframes


    # now visualize
