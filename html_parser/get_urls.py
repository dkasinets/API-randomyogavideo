from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium import webdriver
import os
from os import path
import datetime
import re
import platform
import random


def filter_urls_to_be_yt_videos(urls):
    """
    Regex match and remove duplicates to get valid youtube links
    """
    regex = re.compile(r'^https://www\.youtube\.com/watch\?v=.{11}$', re.IGNORECASE)
    yt_urls_str = list(map(str, urls))
    yt_urls_filtered = list(filter(regex.search, yt_urls_str))
    yt_urls_no_duplicates = list(dict.fromkeys(yt_urls_filtered))
    url_ids = []
    for url in yt_urls_no_duplicates:
        m = re.match(r'^https://www\.youtube\.com/watch\?v=(.{11})$', url)
        url_id = m.groups()[0]
        url_ids.append(url_id)
    return url_ids


def get_selenium_driver():
    """
        Initialize selenium driver object
    """
    # Initialize ChromeDriver 
    if platform.system() == 'Darwin':
        driver = Chrome(executable_path="./chromedriver_macos")
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") # (headless) Google Chrome
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('--no-sandbox')
        driver = Chrome(executable_path="./chromedriver_linux", chrome_options=chrome_options)
    return driver


def get_urls(textToSearch, driver):
    """
    Get links from youtube that match textToSearch
    """
    
    url = f"https://www.youtube.com/results?search_query={textToSearch}"
    # go to page 
    driver.get(url)

    # wait for youtube videos to load
    timeout = 3
    element_present = EC.presence_of_element_located((By.ID, 'contents'))
    WebDriverWait(driver, timeout).until(element_present)
    
    # get the video links
    url_elements = driver.find_elements_by_css_selector("a.yt-simple-endpoint")
    video_urls = []
    for el in url_elements:
        video_urls.append(el.get_attribute("href"))
    
    # regex match links to make sure they're from youtube
    video_urls = filter_urls_to_be_yt_videos(video_urls)
    
    # return random url in a list 
    return [random.choice(video_urls)]
