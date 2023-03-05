from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import tweepy
from api import BEARER_TOKEN, API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import datetime
import time

class ISPComplainer:
    def __init__(self):
        self.speedtest()

    def speedtest(self):
        # Uncomment for Chrome
        service = ChromeService(executable_path="/chromedriver")
        driver = webdriver.Chrome(service=service)

        # Uncomment for Safari
        # driver = webdriver.Safari()

        driver.get("https://speedtest.net")
        time.sleep(5)

        # Start test and wait for completion
        driver.find_element(By.CLASS_NAME, value="start-text").click()
        time.sleep(60)

        # Get ISP name, down speed, up speed
        isp = driver.find_element(By.CLASS_NAME, value="js-data-isp")
        self.isp_name = isp.text

        down = driver.find_element(By.CLASS_NAME, value="download-speed")
        self.down_speed = down.text

        up = driver.find_element(By.CLASS_NAME, value="upload-speed")
        self.up_speed = up.text

        driver.quit()

    def compose_tweet(self):
        now = datetime.datetime.now()
        now_formatted = now.strftime("%I:%M %p on %m/%d/%Y")
        tweet_text = f"Current speeds at {now_formatted}:\nDown: {self.down_speed} mbps\nUp: {self.up_speed} mbps\nISP: {self.isp_name}"
        return tweet_text

    def send_tweet(self):
        client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        text = self.compose_tweet()
        client.create_tweet(text=text)

if __name__ == "__main__":
    isp_complainer = ISPComplainer()
    isp_complainer.send_tweet()
