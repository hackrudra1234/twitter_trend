#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd


# In[4]:


from selenium import webdriver
from selenium.webdriver.common.by import By


# In[5]:


from selenium import webdriver
import streamlit as st
import time
import os
from selenium.webdriver.common.by import By
import pandas as pd
import datetime
import re
@st.cache
def scrape_twitter_trending_data():
    
    #get current_date
    current_date = datetime.datetime.now().strftime('%d/%m/%Y')
    # Initialize the WebDriver
    browser = webdriver.Chrome()
    
    try:
        # Open the URL
        browser.get('https://www.twitter-trending.com/india/statistics')
        time.sleep(20) 
        # Extract data from the last 24 hours
        last_24_hours = browser.find_element(By.XPATH, '//*[@id="hepsitablo"]/div[4]/div').text
        
        # Split the input text into lines
        lines = last_24_hours.split('\n')
        
        # Extract volume and hashtag using regular expressions
        data = []
        for line in lines[2:]:  # Start from index 3 to skip the first 3 lines of the input text
            match = re.match(r'\d+\s+(\d+k)\s+(.+)', line)
            if match:
                volume, hashtag = match.groups()
                data.append((current_date, volume, hashtag))
        
        # Create a DataFrame
        df = pd.DataFrame(data, columns=["Date","Volume", "Word-Hashtag"])
        df['Date'] =pd.to_datetime(df['Date'])
        # Save the DataFrame to a CSV file
        df.to_csv('twitter_trending_data.csv', mode='a', index=False, header=not os.path.exists('twitter_trending_data.csv'))
        return df
    
    finally:
        # Close the WebDriver
        browser.quit()

# Call the function to scrape data and create the DataFrame
df = scrape_twitter_trending_data()

# Print the DataFrame
print(df)

# Main Streamlit app
def main():
    st.title("Twitter Trending Data Scraper")
    
    # Button to scrape data
    if st.button("Scrape Twitter Trending Data"):
        st.info("Scraping data. Please wait...")
        df = scrape_twitter_trending_data()
        st.success("Data scraped and appended to twitter_trending_data.csv.")
        print(df)
    # Date selection for data retrieval
    selected_date = st.date_input("Select Date", datetime.date.today())
    if st.button("Get Data for Selected Date"):
        # Read data from CSV and filter for the selected date
        df = pd.read_csv('twitter_trending_data.csv')
        filtered_data = df[df['Date'] == selected_date.strftime('%d/%m/%Y')]
        st.dataframe(filtered_data)
    # Button to show full data
    if st.button("Show Full Data"):
        # Read and display the entire dataset
        df = pd.read_csv('twitter_trending_data.csv')
        st.dataframe(df)
       
# Run the app
if __name__ == "__main__":
    main()


# In[ ]:




