import os
import time
import random

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


DOWNLOAD_FOLDER = "/Users/cwan01/Downloads"
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
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(f"file://{os.getcwd()}/index.html")

    my_quote = """剛從學校踏入職場的時候，只懂一點點關於學校課本上面教的東西，對於商業邏輯、數字分析、甚至是SQL怎麼寫都一竅不通，在剛開始工作時接到分析的任務使我一個頭兩個大也感到相當的挫折，那時候是曼如不厭其煩地教導小弟我，才逐漸步上軌道，摸到了曼如決策樹的冰山一角，感謝曼如的諄諄教誨。

除了在專業上，也很感謝曼如在各個團隊和各個專案裡面的各種斡旋，並把自己的正面能量注入給大家，使用屁話或是轉念的力量幫助我們維持士氣的穩定。

曼如即將要前往下一個旅程了，祝福妳在新的地方能繼續發光發熱，但好像也不用特別祝福，因為

我相信曼如
    """
    data = {
        "name": ["Chia-Hung Wan", "Tiffany Hsu"],
        "quote": [my_quote, "qwer"],
        "profile": ["/Users/cwan01/Downloads/profile picture.png", "/Users/cwan01/Downloads/星際艦長.jpg"],
        "time": [random_time(), random_time()]
    }
    dataframe = pd.DataFrame(data)

    for _, row in dataframe.iterrows():
        clear_form(browser)
        generate_fake_quote(browser, row["name"], row["quote"], row["profile"], row["time"])

    print("Finish")


if __name__ == "__main__":
    main()