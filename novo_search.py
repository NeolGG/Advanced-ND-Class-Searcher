#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import os
import time

url = "https://bxeregprod.oit.nd.edu/StudentRegistration/ssb/searchResults/searchResults"
json_folder = "jsons/novo"

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

def _create_params(page_offset:int = 0, max_page: int = 100):
    params = {
        "txt_campus": "M",
        # "chk_include_0": "false", # sunday
        # "chk_include_1": "false",  # monday
        # "chk_include_2": "false", # tuesday
        # "chk_include_3": "false",  # wednesday
        # "chk_include_4": "false", # thursday
        # "chk_include_5": "false", # friday
        # "chk_include_6": "false", # saturday
        "txt_term": "202410", # fall
        "startDatepicker": "",
        "endDatepicker": "",
        "uniqueSessionId": "", # IGNORE
        "pageOffset": f"{page_offset}",
        "pageMaxSize": f"{max_page}",
        "sortColumn": "subjectDescription",
        "sortDirection": "asc"
    }
    
    return params

def get_all_classes():
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)
        
    t = time.time()
    session = _create_session()
    data = []
    
    for i in range(0,16):
        params = _create_params(i*500,500)
        print(f"getting page {i+1}")
        response = session.get(url,params=params)
        
        data.append(response.json())

    with open(f"{json_folder}/all_classes{t}.json", 'w') as file:
        json.dump(data, file, indent=4)

def set_filters():
    buildings = ['"O\'Shaughnessy Hall"', '"Geddes Hall"', '"Haggar Hall"', '"Decio Faculty Hall"',
     '"Stinson Remick Hall"', '"Biolchini Hall (LAW)"', '"Remick Family Hall"', '"Fitzpatrick Hall of Eng."',
     '"Grace Hall"', '"Hammes Mowbray Hall"', '"Washington Hall"', '"Walsh Hall of Architecture"',
     '"Coleman Morse Center"', '"McCourtney Hall"', '"Hayes Healy Center"', '"Innovation Park"',
     '"Eck Hall of Law"', '"Galvin Life Science Center"', '"DeBartolo Performing Arts Ctr."', '"Crowley Hall"',
     '"Riley Hall"', '"Corbett Family Hall"', '"Mendoza College of Business"', '"Cushing Hall of Engineering"',
     '"Bond Hall"', '"Malloy Hall"', '"Ricci Band Building"', '"Jenkins and Nanovic Hall"', '"Jordan Hall of Science"',
     '"Hesburgh Library"', '"DeBartolo Hall"', '"West Lake Hall"', '"Pasquerilla Center"', '"West Lake Design Studio"',
     '"Nieuwland Science Hall"', '"Flanner Hall"', '"O\'Neill Hall of Music"', '"Stayer Center"', '"Main Building"']
    
    





