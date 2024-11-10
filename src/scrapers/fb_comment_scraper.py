from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time, json, os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv, dotenv_values  
from fb_scraper import *

'''
    This is an improved version of scraper that
    also translates comment to english.
    It also works in alternate facebook format

    Extended by Lillie Ayer: 
    - added extra protection of credentials 
    - refactored for readability/reusability
    - cleaned links as they're read in to get rid of errors
    - added methods to extract comments in bulk simultaneously:
       -  from multiple files
        - from multiple posts 

'''


class FBCommentScraper(FBScraper):
    def __init__(self, driver=None):
        super().__init__(driver)

    # ************* Authentication Methods *****************
    '''Returns tuple of facebook credentials'''
    def load_fb_credentials(self):
        load_dotenv()
        config = dotenv_values(".env") 
        EMAIL = config['FB_EMAIL']
        PASSWORD = config['FB_PASSWORD']
        creds =  (EMAIL, PASSWORD)
        return creds

    '''
    - links bounds are one off, need additional space at end of link in links.txt
    - lines in links.txt file matter, interprets empty lines as links
    - interprets comments and their child elements but gets confused when commenter posts links (interprets as another element doesnt group in body) --> shifts element recording 
    - analyze sentiments --> how many comments are in support and then how many likes/replies they get'''

    # ** Note this is an essential first step to using the FB comment scraper
    # before you can use scraper superclass or subclass methods
    def login_to_facebook(self):

        self.driver.get('https://www.facebook.com/')
        time.sleep(3)  # Wait for the page to load
        creds = self.load_fb_credentials()

        email_input = self.driver.find_element(By.NAME, 'email')
        email_input.send_keys(creds[0])

        password_input = self.driver.find_element(By.NAME, 'pass')
        password_input.send_keys(creds[1])
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for login to complete

    # ************* Navigating FB Elements Methods *****************

    def click_comment_button(self):
        try:
            print("Clicking comment button...")
            
            # Look for the div with role="button" and aria-label="Comment"
            comment_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Comment']"))
            )

            # Scroll the button into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", comment_button)  # Ensure it's visible
            time.sleep(0.5)  # Allow time for scrolling

            try:
                # Click using JavaScript
                self.driver.execute_script("arguments[0].click();", comment_button)
                print("Clicked 'Comment' button via JS.")
            except Exception as js_click_error:
                print(f"JS click failed: {js_click_error}, retrying with ActionChains.")

                # Fallback to ActionChains if JS click fails
                actions = ActionChains(self.driver)
                actions.move_to_element(comment_button).click().perform()
                print("Clicked 'Comment' button using ActionChains.")

            time.sleep(0.5)  # Short pause to allow any UI changes
        except TimeoutException:
            print("No 'Comment' button found.")
        except Exception as e:
            print(f"Error: {e}")

    def click_comment_button_live_case(self):
        try:
            print("Clicking comment button...")
            
            # Look for the div with role="button" and aria-label="Comment"
            comment_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Leave a comment']"))
            )

            # Scroll the button into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", comment_button)  # Ensure it's visible
            time.sleep(0.5)  # Allow time for scrolling

            try:
                # Click using JavaScript
                self.driver.execute_script("arguments[0].click();", comment_button)
                print("Clicked 'Comment' button via JS.")
            except Exception as js_click_error:
                print(f"JS click failed: {js_click_error}, retrying with ActionChains.")

                # Fallback to ActionChains if JS click fails
                actions = ActionChains(self.driver)
                actions.move_to_element(comment_button).click().perform()
                print("Clicked 'Comment' button using ActionChains.")

            time.sleep(0.5)  # Short pause to allow any UI changes
        except TimeoutException:
            print("No 'Comment' button found.")
        except Exception as e:
            print(f"Error: {e}")

    def click_translate_buttons(self):
        try:
            # Find all translate buttons for comments
            translate_buttons = self.driver.find_elements(By.XPATH, "//div[@role='button' and contains(text(), 'See translation')]")
            print(translate_buttons)
            for button in translate_buttons:
                try:
                    # Scroll the button into view
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    # Allow time for the scroll to complete

                    # Click the translate button using JavaScript
                    self.driver.execute_script("arguments[0].click();", button)
                    print("Clicked 'Translate' button.")
                    # Wait for translation to load

                except Exception as e:
                    print(f"Error clicking translate button: {e}")

        except Exception as e:
            print(f"Could not find translate buttons: {e}")

    def change_to_all_comments(self):
        #looks and clicks on most relevant
        try:
                print("Looking for Most relevant tab")
                # Look for the div with role="button" that contains the 'View more comments' text inside nested spans
                load_comments = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//span[contains(text(), 'Most relevant')]]"))
                )

                self.driver.execute_script("arguments[0].scrollIntoView(true);", load_comments)  # Ensure it's visible
                time.sleep(0.5)

                try:
                    self.driver.execute_script("arguments[0].click();", load_comments)
                    print("Clicked 'View more comments' button via JS.")
                except Exception as js_click_error:
                    print(f"JS click failed: {js_click_error}, retrying with ActionChains.")

                    # If the JavaScript click fails, use ActionChains as a fallback
                    actions = ActionChains(self.driver)
                    actions.move_to_element(load_comments).click().perform()
                    print("Clicked 'View more comments' button using ActionChains.")

                time.sleep(0.5)  # Short pause to allow comments to load
        except TimeoutException:
            print("No more 'View more comments' button found.")
        except Exception as e:
            print(f"Error: {e}")
        #looks and clicks on all comments
        try:
                print("Looking for all comments")
                # Look for the div with role="button" that contains the 'View more comments' text inside nested spans
                load_comments = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='menuitem' and .//span[contains(text(), 'All comments')]]"))
                )

                self.driver.execute_script("arguments[0].scrollIntoView(true);", load_comments)  # Ensure it's visible

                try:
                    self.driver.execute_script("arguments[0].click();", load_comments)
                    print("Clicked 'View more comments' button via JS.")
                except Exception as js_click_error:
                    print(f"JS click failed: {js_click_error}, retrying with ActionChains.")

                    # If the JavaScript click fails, use ActionChains as a fallback
                    actions = ActionChains(self.driver)
                    actions.move_to_element(load_comments).click().perform()
                    print("Clicked 'View more comments' button using ActionChains.")

                # Short pause to allow comments to load
        except TimeoutException:
            print("No more 'View more comments' button found.")
        except Exception as e:
            print(f"Error: {e}")

    def load_bottom_comments(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for comments to load
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
                last_height = new_height

    def load_side_comments(self):
        i = 0
        while i < 2000:
            try:
                print(f"Looking for 'View more comments' button... {i}")
                # Look for the div with role="button" that contains the 'View more comments' text inside nested spans
                load_comments = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//span[contains(text(), 'View more comments')]]"))
                )
                i = i + 6

                self.driver.execute_script("arguments[0].scrollIntoView(true);", load_comments)  # Ensure it's visible
                time.sleep(0.1)

                try:
                    self.driver.execute_script("arguments[0].click();", load_comments)
                    print("Clicked 'View more comments' button via JS.")
                except Exception as js_click_error:
                    print(f"JS click failed: {js_click_error}, retrying with ActionChains.")

                    # If the JavaScript click fails, use ActionChains as a fallback
                    actions = ActionChains(self.driver)
                    actions.move_to_element(load_comments).click().perform()
                    print("Clicked 'View more comments' button using ActionChains.")

                time.sleep(0.1)  # Short pause to allow comments to load
            except TimeoutException:
                print("No more 'View more comments' button found.")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

    # ************* Storing Comment Data Methods *****************

    '''Extracts comments from Web Elements and stores result
        param1: comments --> list obj of WebElements from selenium
        param2: storage --> any list to store dictionary of comments in
        ** Note: this is essential before storing comments in json'''
    def clean_and_store_comments(self, comments: list, storage:list):
        for comment in comments:
            comment_data = {}
            # Extract and split the comment text
            text_parts = comment.text.split("\n")
            offset = 0
            try:
                if text_parts[2] == "Follow":
                    offset += 2

            except:
                continue
            comment_data['author'] = text_parts[0] if len(text_parts) > 0 else "Unknown"
            comment_data['content'] = text_parts[1+offset] if len(text_parts) > 1 else ""
            comment_data['time_posted'] = text_parts[2+offset] if len(text_parts) > 2 else "Unknown"
            comment_data['reactions'] = text_parts[-1]
            print(text_parts)
            print(comment_data)
            if (comment_data['time_posted'] != 'Like'):
                storage.append(comment_data)

    # ************* Extracting Comment Data Methods *****************

    ''' Returns comments from a FaceBook post as WebElements using selenium
        ** Note: does not store comments in json'''
    def extract_content_from_link(self,link)->dict:
        super().extract_content_from_link(link)
        comments = []
        try:
            print(f"is post a watch live: {'facebook.com/watch/live' in link}")
                #  load comments
            if ('facebook.com/reel' in link):
                self.click_comment_button()
            elif ('facebook.com/watch/live' in link):
                print('run run run')
                self.click_comment_button_live_case()

            self.change_to_all_comments()
            self.load_side_comments()

            # find and press a translation button
            self.click_translate_buttons()
                # Find all comments
            comments = self.driver.find_elements(By.XPATH, '//*[starts-with(@aria-label, "Comment by")]')
        except:
            print(f"Failed to load post: {link}")
        all_comments = {link:[]}
        self.clean_and_store_comments(comments, all_comments[link])
        return all_comments
