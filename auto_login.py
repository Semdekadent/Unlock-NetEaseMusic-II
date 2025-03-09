# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00D31E5EAABDB7209CD5F743F53EE51F9771339568C51D2CDFD85896962479090824843C0EFE234321BA5E31FFF9FDFEDE11DA437F0E32CD22418B5ED1EE0DA3140DF2312623CBDA50CA336B4019125571C482E5516EFF6F96BD6A24B24097266C38EEF6C0378D83D38326FF246AAA4886FDE9447BBCA27B8839D210F9334D5F05A4999E53C491A8ABC2ABC085F375CE7A80A3EDB097479F7060686F394741BEA1A71A0810E1B30BDE87A946C64EE32393E736E474A5BD6235A2320A75EBA74C413D64D32AA49BF11A6F85432AA7DD84BF57AD40804382E5598641E8C66DC58A2AB794631699A2506A6AE1C55BEDDAB5068820B354C08248472D50B90FD89C893108AFDCFFF647B36BF6751DE8823C58F78A49CEA03968919190512A1CB112327A703D4E6A23AFC446E30BA8609FF0E688C0B673AF37FD2F0EB1A51E9FBC0C2E6F26B21E34836265E5BB53BE00DD9F25E5"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
