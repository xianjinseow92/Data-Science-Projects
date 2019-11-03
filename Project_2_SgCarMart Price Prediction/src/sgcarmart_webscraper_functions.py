from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime

# All retriever functions take a parsed individual car lsting url and returns a desired attribute named after the function


# Brand Retriever Function
def brand_retrieval(parsed_url):

    brand_name = parsed_url.find(class_='link_redbanner').text.split()[0]
    return brand_name

# Price Retriever Function
def price_error_handling(data_value):
    # Try-Exception error handling
    
    try:   # First try to deal with values higher than 1000
        price = data_value[1]  # will fail on IndexError if retrieves ['na'] scenario
        price = int(price.split(',')[0] + price.split(',')[1]) # Will fail on IndexError if tries to split '900' with a ',' in ['',900]
        
    except IndexError:  # Dealing with ['na'] and ['', 900'] scenarios
        try: 
            price = int(data_value[1]) # Will fail on IndexError if ['na'] scenario
        except IndexError:  # Deals with ['na'] scenarios
            price = np.nan  # Stores NA values as nan
    
    return price

def price_retrieval(parsed_listing_url):
    
    data_value = parsed_listing_url.find_all(class_='font_red')[0].text.strip()
    data_value = data_value.split('$')
    price = price_error_handling(data_value)
    return price



# Deprecration Value Per Year Retriever Function
def depreciation_value_per_year_error_handler(data_value):
    if len(data_value) < 2:
        data_value = np.nan

    else: 
        data_value = data_value[1].split('/yr')
        try:                 
            desired_value = int(data_value[0].split(',')[0] +\
                                data_value[0].split(',')[1]) # Will fail on IndexError if tries to split '900' with a ',' in ['900','']
        except IndexError: 
            desired_value = int(data_value[0])
        
        return desired_value
    
def depreciation_value_per_year_retrieval(parsed_listing_url):
    data_value = parsed_listing_url.find_all(class_="label")[1].findNextSibling().text.strip().split('$')
    depreciation_value_per_year = depreciation_value_per_year_error_handler(data_value)
    return depreciation_value_per_year

# Road Tax Per Year Retriever
def road_tax_error_handler(string_data):
    if '/yr' in string_data: # Only takes in scenarios that are not NA
        try:
            # Removes '$" character and splits string_data into a list of ['', 1,000] or ['', 900]
            road_tax_per_year = \
            string_data.replace('/yr','').strip().split('$') 

            # Accesses the second item in the list
            road_tax_per_year = road_tax_per_year[1] 


            road_tax_per_year = int(road_tax_per_year.split(',')[0] +\
                                    road_tax_per_year.split(',')[1])  # Will fail on IndexError if value is above 1000

        except IndexError: # Handles values that are below 1000. (i.e. ['',900])
            road_tax_pear_year = int(road_tax_per_year[1])

    else: # Deals with 'NA' scenario
        road_tax_per_year = np.nan
    
    return road_tax_per_year

def road_tax_retrieval(parsed_listing_url):
    string_data = parsed_listing_url.find_all(class_='row_info')[1].text.strip()
    road_tax_yearly = road_tax_error_handler(string_data)
    
    return road_tax_yearly
    

# Registered Date Retriever
def registered_date_retrieval(parsed_listing_url):
    reg_date = parsed_listing_url.find_all(class_='row_bg')[1].find_all('td')[3].text.split()[0].split('(')[0]
    return reg_date

# Days of COE Retriever
def days_of_coe_retrieval(parsed_listing_url):
    days_of_coe_left_yy_mm_dd_format_for_cleaner_function=\
    parsed_listing_url.find_all(class_='row_bg')[1].find_all('td')[3].text.split('(')[1].split('COE')[0].strip()
    
    return yr_mm_dd_cleaner(days_of_coe_left_yy_mm_dd_format_for_cleaner_function)


# Define a function to calculate days of COE left
def yr_mm_dd_cleaner(str1):
    """Accepts a string that may or may include the elements yr mths days and 
    converts the whole string into number of days.
    ----
    Input: single string
    output: number of days in integer form
    ----
    Example string inputs:
    - 4yrs 2mths 23days
    - 5yrs
    - 2 mths 23 days
    - 50 days
    """
    
    # Convert days_of_coe_left_yy_mm_dd to days    
    year_index = str1.find('yr')
    if year_index == -1:
        year = 0
    else:
        year = int(str1[year_index-1])

        
    mth_index = str1.find('mth')
    if mth_index == -1:
        mth = 0
    else:
        mth = int(str1[mth_index-1])

        
    day_index = str1.find('day')
    if day_index == -1:
        day = 0
    else:
        day = int(str1[day_index-1])
       
    days_of_coe_left = (year * 365) + (mth * 30) + day 
    return days_of_coe_left


# Mileage Retriever
def mileage_error_handler(data_value):
    if len(data_value) < 2:  # Deals with ['na'] scenarios
        mileage_km = np.nan  # Stores NA values as nan

    else:  
        try:                 
            mileage_km = int(data_value[0].strip().split(',')[0] + data_value[0].strip().split(',')[1])
        except IndexError: # Will fail on IndexError if tries to split '900' with a ',' in ['',900]
            mileage_km = int(data_value[0].strip())
    
    return mileage_km

def mileage_retrieval(parsed_listing_url):
        
    data_value = parsed_listing_url.find_all(class_='row_info')[0].text.strip()
    data_value = data_value.split('km')
    mileage_km = mileage_error_handler(data_value)
    
    return mileage_km

# Manufactured Year Retriever
def manufactured_year_retrieval(parsed_listing_url):
    manufactured_year = parsed_listing_url.find_all(class_='row_info')[6].text
    return manufactured_year

# Transmission Retriever
def transmission_retrieval(parsed_listing_url):
    transmission = parsed_listing_url.find_all(class_='row_info')[7].text
    return transmission

# Deregistration Value Retriever
def dereg_value_retrieval(parsed_listing_url):
    # Splits into ['NA'], or ['$11,026', 'as', 'of', 'today', '(change)'] or ['$900', 'as', 'of', 'today', '(change)']
    data_value = parsed_listing_url.find_all(class_='row_info')[2].text.strip().split() 
    
    dereg_value_from_scrape_date = dereg_value_error_handler(data_value)
    return dereg_value_from_scrape_date
    

def dereg_value_error_handler(data_value):
    if len(data_value) < 2:  # Deals with ['NA'] scenario
        dereg_value_from_scrape_date = np.nan

    else: 
        data_value = data_value[0].split('$')[1] # Puts input into '11,026' or '900' format
        try:                 
            dereg_value_from_scrape_date = \
            int(data_value.split(',')[0] +\
                data_value.split(',')[1]) # Will fail on IndexError if tries to split '900' with a ',' in ['',900]
        except IndexError: 
            dereg_value_from_scrape_date = int(data_value.strip())

        return dereg_value_from_scrape_date


# Open Market Value Retriever
def omv_error_handler(data_value):
    if len(data_value) < 2:  # deals iwth ['NA'] input
        omv = np.nan

    else:
        try:
            omv = int(data_value[1].split(',')[0] +\
                      data_value[1].split(',')[1])  # Will fail on index error if try to split 900
        except IndexError:
            omv = int(data_value[1])
    return omv


def omv_retrieval(parsed_listing_url):    
    data_value = parsed_listing_url.find_all(class_='row_info')[8].text.split('$') 
    # Splits data into ['', '21,967'], ['','900'] or ['NA'] format for input into error function
    
    omv = omv_error_handler(data_value)
    return omv     

# ARF Retriever
def error_handler(data_value):
    if len(data_value) < 2:  # deals iwth ['NA'] input
        desired_value = np.nan

    else:
        try:
            desired_value = int(data_value[1].split(',')[0] +\
                                data_value[1].split(',')[1])   # Will fail on index error if try to split 900
        except IndexError:
            desired_value = int(data_value[1])
    return desired_value


def arf_retrieval(parsed_listing_url):
    data_value = parsed_listing_url.find_all(class_='row_info')[9].text.split('$')
    arf = error_handler(data_value)
    return arf

# COE Price retriever 
def coe_error_handler(data_value):
    if len(data_value) < 2:  # deals iwth ['NA'] input
        coe_from_scrape_date = np.nan

    else:
        try:
            coe_from_scrape_date = int(data_value[1].split(',')[0] +\
                                       data_value[1].split(',')[1])  # Will fail on index error if try to split 900
        except IndexError:
            coe_from_scrape_date = int(data_value[1])
    return coe_from_scrape_date


def coe_retrieval(parsed_listing_url):
    data_value = parsed_listing_url.find_all(class_='row_info')[3].text.split('$')
    coe_from_scrape_date = coe_error_handler(data_value)
    return coe_from_scrape_date

# Engine Capacity Retriever
def engine_capacity_error_handler(data_value):
    if len(data_value) < 2:  # deals iwth ['NA'] input
        desired_value = np.nan

    else:
        try:
            desired_value = int(data_value[0].split(',')[0] +\
                                       data_value[0].split(',')[1])  # Will fail on index error if try to split 900
        except IndexError:
            desired_value = int(data_value[0])
    return desired_value


def engine_capacity_retrieval(parsed_listing_url):
    data_value = parsed_listing_url.find_all(class_='row_info')[4].text.strip().split('cc')
    engine_capacity = engine_capacity_error_handler(data_value)
    return engine_capacity

# Curb Weight Retriever
def curb_weight_error_handler(data_value):
    if len(data_value) < 2:  # deals iwth ['NA'] input
        desired_value = np.nan

    else:
        try:
            desired_value = int(data_value[0].split(',')[0] +\
                                       data_value[0].split(',')[1])  # Will fail on index error if try to split 900
        except IndexError:
            desired_value = int(data_value[0])
    return desired_value


def curb_weight_retrieval(parsed_listing_url):
    data_value = parsed_listing_url.find_all(class_='row_info')[5].text.split()
    curb_weight = curb_weight_error_handler(data_value)
    return curb_weight

# Number of owners retriever
def number_of_owners_retrieval(parsed_listing_url):
    no_of_owners = int(parsed_listing_url.find_all(class_='row_info')[-1].text)
    return no_of_owners


# Type of Vehicle Retriever
def type_of_vehicle_retrieval(parsed_listing_url):
    type_of_vehicle = parsed_listing_url.find(class_='row_bg1').find_all('a')[0].text 
    return type_of_vehicle