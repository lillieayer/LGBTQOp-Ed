from fb_comment_scraper import *

config = dotenv_values("../../.env") 

#lori42898
EMAIL = config["FB_EMAIL"]
PASSWORD = config["FB_PASSWORD"]

if __name__ == '__main__':
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    login_to_facebook(driver)
    comments = fetch_comments_from_post("https://www.facebook.com/watch/?v=3439901456224795", driver)
    with open('debug_links_comments.json', 'a', encoding='utf-8') as file:
        json.dump(comments, file, ensure_ascii=False, indent=4)
    # Close the browser
    input("finished")
    driver.quit()

