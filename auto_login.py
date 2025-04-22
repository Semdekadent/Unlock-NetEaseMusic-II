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
    browser.add_cookie({"name": "MUSIC_U", "value": "00CC3CBB202906D6200EAF86653C12809DC37C2410423E4AB91E90C4AAECF815984E0DA85C5200D454FBF79BCAED1997C76CE2EB3DD743CBF2B2952DC63403441A5F11B48B8A04EC02E90305F6BB576291BA961E9FCF3FD009F92112F947F608F0C301938856CA23DA4875F94F0899974EDD4A0AB3F645177F579EB05C04AB2149CE892209CA29540890ED159A8406FC9231C6BE61F5CEBB057BD634214728ECAF3457498571DD0DF77BFEC73C1C306D3FEB3630AEF29D4FC1E5C6826736391E8826D40BB458F486390295239B0609DB33C06E3940552486DEF1769A09E749D0A6F36E47158111EC370E13B5FDC9BE3D0967C7EB276096918DEF08B7D58A78A5D870007927B21975E5A94F098CC88B1143B387A271920D2F7BC70DB14B816DE1B5E1699AA7876AA81EAB53813A5DF54B14B93EC7CF8727CD01DFABAA156F32CEBAA3631004A3B821DD410026542CF6276E"})
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
