from fb_comment_scraper import *

def search_fb_query(keywords, driver):
    try:
        time.sleep(3)
        print("Looking for search bar for querying...")

        search_bar = driver.find_element(By.XPATH, '//div[@role="banner"]//input[@placeholder="Search Facebook"]')
    
       # search_bar.send_keys(keywords)
        # search_bar.send_keys(Keys.RETURN)
    except Exception as e:
        print("Error finding search icon: \n", e)

if __name__ == "__main__":  
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    login_to_facebook(driver)
    search_fb_query("hello", driver)
    # Close the browser
    input("finished")
    driver.quit()
