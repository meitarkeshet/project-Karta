



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

import pandas as pd # for dataFrames

import re
import lxml 
import cchardet # to assit in charecter detection

# in order to not expose our password we will use 'getpass'
import getpass
# To connect to mysql use:
from sqlalchemy import create_engine

# Define functions:
# ------------------------------------------------------------------------------------------------------------------------------------

# January 1, April 1, July 1, and October 1

# the function gets a url for a webpage and returns a list of links (for each rental proposal) on that page 
def outisde_scrape_links(url):  
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')  
        
    page_link_lst = []
    for link in soup.findAll("div", {"class": "details-title"}) :
        page_link_lst.append("https://web.archive.org"+link.find("a")['href']) # find the link attached 
    return(page_link_lst)

# TAKES a url including detaild information on a rental proposal and RETURNS a single row'de dataFrame
def inside_scrape(url):
    print(url,'\n') # see where did you get to 
    #requests_session = requests.Session() # to make the scrape fastser - use the same connection (risk of being blocked)

    r = requests.get(url) # reuse if getting blocked by website
    #r = requests_session.get(url)
    soup = BeautifulSoup(r.text, 'lxml')  
    
    # create an empty data Frame
    df_single_search = pd.DataFrame()

    # insert data to dataFrame
    # ----------------------------------------
     # error handling - initialize columns as nulls
   
    scrape_hour, scrape_year, scrape_day, scrape_month, description_short, description_long, price, rooms, amenities, zip_code, address, days_on_market, price_history, lister, price_at_point,last_price_change = 'NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN','NaN'
    
    
    
    # details:
    details = soup.find("div", {"class": "details"})
   
    
    if details:
        # short description of the listing
        details_describe = details.find_all('span', attrs={'class':re.compile(r'detail_cell')})
        if details_describe:
            description_short = "".join(re.findall(r'\>(.*?)\<' , str(details_describe))) # DESC_SHORT > to file
        #print(description_short)
         # description of rooms
        details_a = details.find_all('span', attrs={'class':'nobreak'})
        if details_a:
            rooms = "".join(re.findall(r'\>(.*?)\<' , str(details_a))) # ROOMS > to df
    # the price asked:
        price = re.findall(r'(?=\$).+', str(details))[0]  # RENT PRICE > to df
    
    
    df_single_search['price'] = [price] # notice passing as list 
    df_single_search['des_short'] = [description_short] # notice passing as list 
    df_single_search['des_rooms'] = [rooms] # notice passing as list 

    # detailed description (by owner)
    describe_soup = soup.find("blockquote", {"class": "description_togglable hidden"})
    if describe_soup:
        description_long = describe_soup.get_text() # DESC_LONG > to file
    df_single_search['des_long'] = [description_long] # notice passing as list 

    # amenities included
    amenities_soup = soup.find('div', attrs={'class':re.compile(r'amenities')})
    if amenities_soup:
        amenities = amenities_soup.get_text().replace("Amenities", "").replace("\n\n", " ")
    df_single_search['amenities'] = [amenities] # notice passing as list 

    # save each second line under the name of the line above ---------------------

    # building address:
    address = soup.select_one('h2 ~ p').get_text()
    if address:
    # seperate address, city, zipcode
        address_dirty = "".join(re.findall(r'(?!  ).?', ''.join(address.split('\n'))))
        if address_dirty:
            address_dirty = address_dirty.split('  ')[0].replace(u'\xa0', u' ').split('  ') # the encoding ('utf-8') casuses space to be written as '\xa0'
            if len(address_dirty) == 2:
        # zip code
                if address_dirty[1]:
                    zip_code = re.findall(r'[0-9]*$', address_dirty[1].strip())[0]
        # address
                if address_dirty[0]:
                    address = address_dirty[0]
    
    df_single_search['zip'] = [zip_code] # notice passing as list 
    df_single_search['address'] = [address] # notice passing as list 


    facts_dirty = soup.select('h6 ~ *')
    if facts_dirty:
        for i in facts_dirty:
        # Days On Market
            #print(i.get_text(), "\n")
            #print("end\n")
            if "days on StreetEasy" in i.get_text():
                days_on_market = i.get_text().strip()

        # Last Price Change
            if "days ago" in i.get_text():
                last_price_change = i.get_text().strip()
                last_price_change = " ".join([i.strip() for i in last_price_change.split('\n')])
                
    df_single_search['last_price_change'] = [last_price_change] # notice passing as list 
    df_single_search['days_on_market'] = [days_on_market] # notice passing as list 


    # Price change history
    #print("\n Before price change history:\n")
    price_change_dirty = soup.select('h2 ~ table')
 # Price change history
    if price_change_dirty:
        history_table = pd.read_html(str(price_change_dirty))[0].fillna(method='ffill', axis=0) # save into a pandas DataSet - fill NaN!
        if history_table.shape[1] == 3:
            print("\nhistory_table: \n",history_table)
            
            if not history_table.iloc[:,0].empty:
                price_history = "|".join(list(history_table.iloc[:,0])) # notice - before added 'str' line
                #print("\nprice_history: ", price_history)

            if not history_table.iloc[:,1].empty:
                lister = "|".join(list(history_table.iloc[:,1]))
                #print("\nlister: ", lister)

            if not history_table.iloc[:,2].empty:
                price_at_point = "|".join(list(history_table.iloc[:,2]))
    df_single_search['price_history'] = price_history
    df_single_search['lister'] = lister
    df_single_search['price_at_point'] = price_at_point
    
    #print("out of scrape\n")
    # moment of scrape
    archive_dates = re.findall(r'(?<=FILE ARCHIVED ON ).*(?=AND)' , str(soup))
    if archive_dates:
        archive_dates = archive_dates[0]
        print(archive_dates,"\n")
        scrape_hour = re.findall(r'\d\d:\d\d:\d\d' , archive_dates)[0].strip()
        scrape_year =  re.findall(r'\d{4}.*$' , archive_dates)[0].strip()
        scrape_day =  re.findall(r'\d+(?=,)' , archive_dates)[0].strip()
        scrape_month =  re.findall(r'(?<=\d\d:\d\d:\d\d).+?(?= )' , archive_dates)[0].strip()
    
    df_single_search['scrape_year'] = scrape_year
    df_single_search['scrape_day'] = scrape_day
    df_single_search['scrape_month'] = scrape_month
    df_single_search['scrape_hour'] = scrape_hour

    scrape_year, scrape_day, scrape_month

    print(df_single_search)
    return(df_single_search)

# takes the first page 
#def scrape_():

# takes a url, opens it and checks if the words Hrm. exist in the first h2 object
def check_archived(web_page):
    requests_session = requests.Session()
    r = requests_session.get(web_page)
    soup = BeautifulSoup(r.text, 'lxml') 
    top_h2 = soup.select_one('h2').get_text()
    print (top_h2)
    if 'Hrm.' in top_h2:
        print("Page not archived")
        return (False)
    else:
        print("Page archived")
        return (True)
    
# takes a first page and retuns the url of the last page
def check_next_page(current_page):
    r = requests.get(current_page)
    soup = BeautifulSoup(r.text, 'html.parser')  
    next_page_url = soup.find("a", {"class": "next_page"})['href']
    print(next_page_url)
    if next_page_url:
        return (next_page_url)
    else:
        return (False)

def check_last_page_nbr(first_page):
    r = requests.get(first_page)
    soup = BeautifulSoup(r.text, 'html.parser')  
    last_page_num = soup.select('a:nth-last-child(2)')[-2].get_text()
    return (int(last_page_num))


def check_last_page(first_page):
    r = requests.get(first_page)
    soup = BeautifulSoup(r.text, 'html.parser')  
    last_page_url = soup.find("a", {"class": "next_page"})['href']
    return (last_page_url)
    
# takes the first page of a "website screenshot" (already by area, e.g Manhattan)
def scrape_moment(first_page):
    current_page_url = first_page # on the first round - use first page as current
    last_page_num = check_last_page_nbr(first_page)
    
    #print(page_link_lst,'\n')
    dfObj = pd.DataFrame(columns=['scrape_day','scrape_month','scrape_year','scrape_hour','des_short', 'des_long', 'price', 'des_rooms', 'amenities', 'zip', 'address', 'days_on_market', 'price_history', 'lister', 'price_at_point','last_price_change'])
    # notice needing to change dfobj name
    scrape_page = current_page_url # on the first round - use first page as current
    page_list = list(range(last_page_num))
    pages_success_scrape = set()
    print (page_list)
    page_num = 1 
    while page_num < last_page_num:
        page_link_lst = outisde_scrape_links(current_page_url) # get links on current page
        for link in page_link_lst:
            time.sleep(random.randint(10, 20)) # avoid getting blocked
            # check if the page was archived
            if check_archived(link):
                dfObj = dfObj.append(inside_scrape(link)) 
                pages_success_scrape.add(scrape_page) # add 
            print("Scraped: ",page_num, " out of : ", last_page_num)

        scrape_page = random.choice(page_list) # select a random page number value from the list of posible pages
        print("\nLooking into: ",scrape_page)
        page_list.remove(scrape_page) # take out p. number of the current scraped page from the list of possible pages

        dfObj.to_sql("temp_streeteasy", engine, index=False, if_exists='append')
        print("\n", current_page_url,"\n")
        page_num = page_num+1 # for counting pages scraped
        #current_page_url = str(first_page)+"?page={}".format(page_num)# change to the next page
        current_page_url = str(first_page)+"?page={}".format(scrape_page)# change to the next page
        
        print("\nafter:", current_page_url,"\n")
        print("\nScraped the following pages: ",pages_success_scrape)
        print("\nWhich makes a total of :",len(pages_success_scrape))
        time.sleep(random.randint(10, 120)) # avoid getting blocked

    return (dfObj)
    

# for 2014
url = "https://web.archive.org/web/20150111134355if_/http://streeteasy.com/for-rent/manhattan"

#print(scrape_moment(url))
# ------------------------------------------------------------------------------------------------------
# pushes a dataFrame into sql

# Connect to my local SQL server
hostname = "localhost"
username = "root"
password = getpass.getpass()
database = "karta"
engine = create_engine(f"mysql+pymysql://{username}:{password}@{hostname}/{database}")

base_df = pd.DataFrame(columns=['scrape_day','scrape_month','scrape_year','scrape_hour','des_short', 'des_long', 'price', 'des_rooms', 'amenities', 'zip', 'address', 'days_on_market', 'price_history', 'lister', 'price_at_point','last_price_change'])
# clean exsiting frame 
base_df.to_sql("temp_streeteasy", engine, index=False, if_exists='replace')
#push to sql
scrape_moment(url)


    # check are there more pages ahead?
    # if yes - move to the next page
    # if not - finish

# open a page V

# get a list of links in the page V

# for each link in the list of links - open and extract the data 

# move to next list

# move to next page