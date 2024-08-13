#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

url = "https://bxeregprod.oit.nd.edu/StudentRegistration/ssb/searchResults/searchResults"

def _get_cookies() -> dict:
    '''
    Uses selenium to open an instance of the novo website to generate cookies for novo class queries
    
    returns: dictionary of cookies
    '''
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--window-size=1920x1080")  
    # chrome_options.add_argument("--disable-gpu") 
    # chrome_options.add_argument("--no-sandbox") 
    # chrome_options.add_argument("--disable-dev-shm-usage")  

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://bxeregprod.oit.nd.edu/StudentRegistration/ssb/term/termSelection?mode=search")

    drop_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="s2id_txt_term"]')))
    drop_button.click()

    fall_2024 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="202410"]')))
    fall_2024.click()

    submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="term-go"]')))
    submit.click()

    cookies = driver.get_cookies()
    session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}
    driver.quit()
    
    return session_cookies

def _create_session() ->requests.Session:
    '''
    Creates a session with the valid cookies for novo class queries
    
    returns: Session instance
    '''
    session = requests.Session()
    session_cookies = _get_cookies()
    for cookie in session_cookies:
        session.cookies.set(cookie,session_cookies[cookie])
    
    return session

def _create_params():
    params = {
        "txt_campus": "M",
        "chk_include_0": "false", # sunday
        "chk_include_1": "true",  # monday
        "chk_include_2": "false", # tuesday
        "chk_include_3": "false",  # wednesday
        "chk_include_4": "false", # thursday
        "chk_include_5": "false", # friday
        "chk_include_6": "false", # saturday
        "txt_term": "202410", # fall
        "startDatepicker": "",
        "endDatepicker": "",
        "uniqueSessionId": "", # IGNORE
        "pageOffset": "0",
        "pageMaxSize": "500",
        "sortColumn": "subjectDescription",
        "sortDirection": "asc"
    }
    
    return params

session = _create_session()
params = _create_params()
response = session.get(url,params=params)

data = response.json()

print(json.dumps(data, indent=4))
