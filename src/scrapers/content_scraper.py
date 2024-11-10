from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
from enum import Enum
import os,json

'''
*** ContentScraperInterface: ***

An superclass that defines and partially implements methods for subclasses of ContentScraper:

** Purpose: Defines methods/qualities for web scrapers for various platforms
that can derive the likes/shares/comments from social media content. 


** Parameters: 

Can scrape web content for the various inputs:
-  given a social media link
- given a file of social media links
- given a folder with several files of social media links

'''

class ContentScraperInterface(ABC):
    def __init__(self, driver=None):
        self.driver = driver

    def set_driver(self, driver):
        self.driver = driver

    def clean_metric(self, count_label:str)->float:
        count = count_label
        if 'K' in count_label:
            i = count_label.index('K')
            count = count_label[0:i]
            count = float(count)
            count *= 1000
        else:
            if " " in count:
                count = count_label.split(' ')[0]
            if ',' in count:
                count = count.replace(',','')
            count = float(count)
        return count
    
    def extract_links_from_file(self,filepath:str) ->list[str]:
        with open(filepath, 'r') as file:
            # cleans out \n and then empty space in list of links
            file_links = [line.strip() for line in file.readlines()]
            file_links = [link for link in file_links if link != '']
        return file_links


    def extract_content_from_link(self, link:str):
        content = {'LINK':link}
        self.driver.get(link)
        return content

   
    def extract_content_from_files(self, output_folderpath, content_name)->dict:
        for file in os.listdir(dir):
            all_posts_links = self.extract_links_from_file(dir + '/' + file)
            file_insights = []
            
            for post_link in all_posts_links:

                post_insights = self.extract_content_from_link(post_link)
                # add dictionary of each post info frome each file 
                file_insights.append(post_insights)
                
            filename = file.split('.')
            with open(output_folderpath + '/' + filename[0] + '_' + content_name + '.json', 'w', encoding='utf-8') as engagement_file:
                json.dump(file_insights, engagement_file, ensure_ascii=False, indent=4)
   





