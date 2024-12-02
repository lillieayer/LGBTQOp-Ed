import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
from enum import Enum

class Test_FB_Engagement_Scraper(unittest.TestCase):
    def setUp(self):
        self.chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)

        
    def test_lakewood_posts(self):

       pass

if __name__ == '__main__':
    unittest.main()