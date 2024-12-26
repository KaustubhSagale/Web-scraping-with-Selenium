import uuid
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import pymongo
import time

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["twitter_trends"]
collection = db["trending_topics"]

API_KEY = 'edfcb4ee62a468be893270ed4e33980c'  

proxy = f'http://api.scraperapi.com?api_key={API_KEY}&url=https://twitter.com'
chrome_options = Options()
chrome_options.add_argument(f"--proxy-server={proxy}")
service = Service("/opt/homebrew/bin/chromedriver") 

def scrape_twitter_trends():
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://twitter.com/login")
        time.sleep(5)

        username = driver.find_element(By.NAME, "text")
        username.send_keys("Enter ur Twitter username")  # Replace with your Twitter username
        username.send_keys(Keys.RETURN)
        time.sleep(5)

        password = driver.find_element(By.NAME, "password")
        password.send_keys("Enter UR twitter Password")  # Replace with your Twitter password
        password.send_keys(Keys.RETURN)
        time.sleep(10)

        trends = driver.find_elements(By.XPATH, "//span[contains(text(),'Trending')]/ancestor::div/following-sibling::div//span")[:5]
        trending_topics = [trend.text for trend in trends]

        scrape_id = str(uuid.uuid4())
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_address = requests.get("http://api64.ipify.org").text

        record = {
            "_id": scrape_id,
            "trend1": trending_topics[0] if len(trending_topics) > 0 else None,
            "trend2": trending_topics[1] if len(trending_topics) > 1 else None,
            "trend3": trending_topics[2] if len(trending_topics) > 2 else None,
            "trend4": trending_topics[3] if len(trending_topics) > 3 else None,
            "trend5": trending_topics[4] if len(trending_topics) > 4 else None,
            "end_time": end_time,
            "ip_address": ip_address
        }

        collection.insert_one(record)
        print("Data inserted:", record)
        return record

    finally:
        driver.quit()

scrape_twitter_trends()
