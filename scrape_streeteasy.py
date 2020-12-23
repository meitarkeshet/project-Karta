



# DEMO January 1 

# Load needed packages:
# -------------------------------------------------------------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# for waits:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# for printing current time when crashes
import time
import datetime
# for htmls:
from bs4 import BeautifulSoup
# for loading the page : start only after loading
from selenium.webdriver.chrome.options import Options
# import random for time
import random
# for loading sound directly in python (not working?)
from playsound import playsound
# for openning sound file from computer
import os
alarm = "C:\\Users\\meita\\Documents\\auto reservation\\fire.wav"
# for opening the web browser
PATH = "C:\\Program Files (x86)\\chromedriver.exe"
driver = webdriver.Chrome(PATH)
# for voicing errors 
from win32com.client import Dispatch
speak = Dispatch("SAPI.SpVoice")

import requests  # for soup
import lxml

# Define functions:
# ------------------------------------------------------------------------------------------------------------------------------------

# for 2014
url = "https://web.archive.org/web/20150111134355if_/http://streeteasy.com/for-rent/manhattan"


# January 1, April 1, July 1, and October 1

# the function gets a url for a webpage and returns a list of links (for each rental proposal) on that page 
def outisde_scrape_links(url):  
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')  
    page_link_lst = []
    for link in soup.findAll("div", {"class": "details-title"}) :
        page_link_lst.append("https://web.archive.org"+link.find("a")['href']) # find the link attached 

    return(page_link_lst)

#for link in page_link_lst:
    
# open a page V

# get a list of links in the page V

# for each link in the list of links - open and extract the data 

# move to next list

# move to next page