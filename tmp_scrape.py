# scrape streeteasy.com for 
# https://streeteasy.com/for-sale/nyc
# fiscal Quarters : 
 #January, February, and March (Q1)
  #  April, May, and June (Q2)
   # July, August, and September (Q3)
    #October, November, and December (Q4)
# January 1, April 1, July 1, and October 1


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

import pandas as pd

# Define functions:
# ------------------------------------------------------------------------------------------------------------------------------------

import re
import lxml 
import cchardet # to assit in charecter detection

#requests_session = requests.Session() # to make the scrape fastser - use the same connection (risk of being blocked)

# og tester = inside page
#url = "https://web.archive.org/web/20170809034313/http://streeteasy.com/building/199-water-street-manhattan/2100"
url = "https://web.archive.org/web/20170724225251/http://streeteasy.com/distil_r_captcha.html?requestId=70e79418-3ef3-4ce2-88dd-cae6bbd17ec4&httpReferrer=%2Fbuilding%2F199-water-street-manhattan%2F2100"
# second tester = outside page
#url = "https://web.archive.org/web/20150111134355if_/http://streeteasy.com/for-rent/manhattan"
   
#r = requests.get(url) # reuse if getting blocked by website
#r = requests_session.get(url)
#soup = BeautifulSoup(r.text, 'lxml')  


import re
 # building address:

page_list = list(range(5))

print(page_list,"\n")
scrape_page = random.choice(page_list) # select a random page number value from the list of posible pages
print(scrape_page,"\n")

page_list.remove(scrape_page) # take out p. number of the current scraped page from the list of possible pages
print(page_list,"\n")

