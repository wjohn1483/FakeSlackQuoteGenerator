import os
import time
import random

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


DOWNLOAD_FOLDER = "PATH_TO_DOWNLOAD_FOLDER"
DOWNLOAD_FILENAME = "quote.png"
OUTPUT_FOLDER = "outputs"


def random_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    if int(hour) < 12:
        am_pm = "AM"
    else:
        am_pm = "PM"
        hour -= 12
    if int(minute) < 10:
        minute = f"0{minute}"
    return f"{hour}:{minute} {am_pm}"


def rename_output_file(name: str):
    if OUTPUT_FOLDER not in os.listdir(os.getcwd()):
        os.mkdir(OUTPUT_FOLDER)

    while DOWNLOAD_FILENAME not in os.listdir(DOWNLOAD_FOLDER):
        print("Waiting for download...")
        print(f"Target file = {DOWNLOAD_FILENAME}")
        print(f"Current files = {os.listdir(DOWNLOAD_FOLDER)}")
        time.sleep(1)
    os.rename(f"{DOWNLOAD_FOLDER}/{DOWNLOAD_FILENAME}", f"{OUTPUT_FOLDER}/{name}.png")


def clear_form(browser: webdriver):
    browser.find_element(by=By.ID, value="name").clear()
    browser.find_element(by=By.ID, value="quote").clear()
    browser.find_element(by=By.ID, value="profilePic").clear()
    browser.find_element(by=By.ID, value="slackTime").clear()


def generate_fake_quote(browser: webdriver, name: str, quote: str, profile_picture_path: str, slack_time: str="08:33 AM"):
    if DOWNLOAD_FILENAME in os.listdir(DOWNLOAD_FOLDER):
        os.remove(f"{DOWNLOAD_FOLDER}/{DOWNLOAD_FILENAME}")

    browser.find_element(by=By.ID, value="name").send_keys(name)
    browser.find_element(by=By.ID, value="quote").send_keys(quote)
    browser.find_element(by=By.ID, value="profilePic").send_keys(profile_picture_path)
    browser.find_element(by=By.ID, value="slackTime").send_keys(slack_time)

    submit_button, download_button = browser.find_elements(by=By.CLASS_NAME, value="button.button-submit")
    submit_button.click()
    time.sleep(1)
    download_button.click()
    time.sleep(1)

    rename_output_file(name)


def main():
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(f"file://{os.getcwd()}/index.html")

    data = {
        "name": ["Hello", "World"],
        "quote": ["asdf", "qwer"],
        "profile": ["./profile picture.png", "./profile picture2.png"],
        "time": [random_time(), random_time()]
    }
    dataframe = pd.DataFrame(data)

    for _, row in dataframe.iterrows():
        clear_form(browser)
        generate_fake_quote(browser, row["name"], row["quote"], row["profile"], row["time"])

    print("Finish")


if __name__ == "__main__":
    main()