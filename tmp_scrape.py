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

requests_session = requests.Session() # to make the scrape fastser - use the same connection (risk of being blocked)

# og tester = 
#url = "https://web.archive.org/web/20150205011808/http://streeteasy.com/building/696-2-avenue-manhattan/2b"
 
# second tester = 
url = "https://web.archive.org/web/20150111134355/http://streeteasy.com/building/trump-tower/35e"
   
#r = requests.get(url) # reuse if getting blocked by website
r = requests_session.get(url)
soup = BeautifulSoup(r.text, 'lxml')  


import re

archive_dates = re.findall(r'(?<=FILE ARCHIVED ON ).*(?=AND)' , str(soup))[0]
if archive_dates:
    print(archive_dates,"\n")
    hour = re.findall(r'\d\d:\d\d:\d\d' , archive_dates)[0].strip()
    year =  re.findall(r'\d{4}.*$' , archive_dates)[0].strip()
    day =  re.findall(r'\d+(?=,)' , archive_dates)[0].strip()
    month =  re.findall(r'(?<=\d\d:\d\d:\d\d).+?(?= )' , archive_dates)[0].strip()

    print("hour: ",hour, "\n")
    print("year: ",year, "\n")
    print("day: ",day, "\n")
    print("month: ", month, "\n")


