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
url = "https://web.archive.org/web/20150111134355/http://streeteasy.com/building/loft-14/2?featured=1"
   
#r = requests.get(url) # reuse if getting blocked by website
r = requests_session.get(url)
soup = BeautifulSoup(r.text, 'lxml')  

# get a list of links in the page

page_link_lst = []

# create an empty data Frame
# ----------------------------------------
df_single_search = pd.DataFrame()

# insert data to dataFrame
# ----------------------------------------
# details:
details = soup.find("div", {"class": "details"})

# short description of the listing
details_describe = details.find_all('span', attrs={'class':re.compile(r'detail_cell')})
description_short = "".join(re.findall(r'\>(.*?)\<' , str(details_describe))) # DESC_SHORT > to file
#print(description_short)
df_single_search['des_short'] = [description_short] # notice passing as list 

# detailed description (by owner)
describe_soup = soup.find("blockquote", {"class": "description_togglable hidden"})
description_long = describe_soup.get_text() # DESC_LONG > to file
df_single_search['des_long'] = [description_long] # notice passing as list 

# the price asked:
price = re.findall(r'(?=\$).+', str(details))[0]  # RENT PRICE > to df
df_single_search['price'] = [price] # notice passing as list 


# description of rooms
details_a = details.find_all('span', attrs={'class':'nobreak'})
rooms = "".join(re.findall(r'\>(.*?)\<' , str(details_a))) # ROOMS > to df
df_single_search['des_rooms'] = [rooms] # notice passing as list 


# amenities included
amenities_soup = soup.find('div', attrs={'class':re.compile(r'amenities')})
amenities = amenities_soup.get_text().replace("Amenities", "").replace("\n\n", " ")
df_single_search['amenities'] = [amenities] # notice passing as list 

# save each second line under the name of the line above ---------------------

# building address:
address = soup.select_one('h2 ~ p').get_text()

# seperate address, city, zipcode
address_dirty = "".join(re.findall(r'(?!  ).?', ''.join(address.split('\n'))))
address_dirty = address_dirty.split('  ')[0].replace(u'\xa0', u' ').split('  ') # the encoding ('utf-8') casuses space to be written as '\xa0'
    # zip code
zip_code = re.findall(r'[0-9]*$', address_dirty[1].strip())[0]
df_single_search['zip'] = [zip_code] # notice passing as list 

    # address
address = address_dirty[0]
df_single_search['address'] = [address] # notice passing as list 


facts_dirty = soup.select('h6 ~ *')
for i in facts_dirty:
# Days On Market
    #print(i.get_text(), "\n")
    #print("end\n")
    if "days on StreetEasy" in i.get_text():
       days_on_market = i.get_text().strip()
       df_single_search['days_on_market'] = [days_on_market] # notice passing as list 

# Last Price Change
    if "days ago" in i.get_text():
        last_price_change = i.get_text().strip()
        last_price_change = " ".join([i.strip() for i in last_price_change.split('\n')])
        df_single_search['last_price_change'] = [last_price_change] # notice passing as list 

# Price change history
price_change_dirty = soup.select('h2 ~ table')
history_table = pd.read_html(str(price_change_dirty))[0] # save into a pandas DataSet 

print(",".join(list(history_table[0])),'\n')
df_single_search['price_history'] = "|".join(list(history_table[0]))
df_single_search['lister'] = "|".join(list(history_table[1]))
df_single_search['price_at_point'] = "|".join(list(history_table[2]))

print(df_single_search)