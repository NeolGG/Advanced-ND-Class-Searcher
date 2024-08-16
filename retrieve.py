from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time

def getHeadings(bodyPanel: WebElement) -> set:
    h3_elements = bodyPanel.find_elements(By.TAG_NAME, "h3")
    headings = set()
    
    for h3 in h3_elements:
        headings.add(h3.text)
    
    return headings

def click_search(driver):
    button = driver.find_element(By.XPATH,"/html/body/main/div[1]/div/div[2]/form/div[2]/div/div[5]/button")
    button.click()

def wait_for_element(driver, locator):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

def get_courses(driver) -> list:
    panel_body = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div[3]")
    courses = panel_body.find_elements(By.CSS_SELECTOR,".result.result--group-start")
    print(len(courses))
    return courses

def parse_course(course_ND: WebElement):
    print(course_ND.text)
    # class_ND.click()


options = Options()
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

driver.get("https://classsearch.nd.edu/")
print(f'scraping {driver.title}...')

titles = driver.find_element

click_search(driver)



# get list of courses
wait_for_element(driver,(By.CSS_SELECTOR,".result.result--group-start")) #waits for first class to appear
courses = get_courses(driver) # each is a webelement

#-------------for each course-------------------


# TEST
log = open("headings.txt","w")
head_code = None

courses[0].click()
wait_for_element(driver,(By.XPATH,"/html/body/main/div[3]/div/div[2]/div[1]")) #waits for first body block to appear
info_panel = driver.find_elements(By.CLASS_NAME,"panel__content")[2]

counter = 0

total_headings = set()

for c in courses:
    isMany = int("sections" in c.text) # checks if class has multiple sections aka 
    
    if isMany: continue
    
    course_code = c.find_element(By.CLASS_NAME, "result__code").text

    c.click()
    
    WebDriverWait(info_panel,10).until(EC.text_to_be_present_in_element((By.CLASS_NAME,"panel__head"), course_code))
    
    body_panel = info_panel.find_element(By.CLASS_NAME,"panel__body")
    
    
    counter+=1
    print(counter)
    
    # TEST - to see how what headings there in classsearch
    current_headings = getHeadings(body_panel)
    total_headings.update(current_headings)
    
    print(f"{course_code} - {str(current_headings)}")
    
    if counter == 500:
        break

print(total_headings)
log.write(str(total_headings))
log.close()
exit()

    
courses[0].click()
wait_for_element(driver,(By.XPATH,"/html/body/main/div[3]/div/div[2]/div[1]")) #waits for first body block to appear

info_panel = driver.find_elements(By.CLASS_NAME,"panel__content")[2]
body_panel = info_panel.find_element(By.CLASS_NAME,"panel__body")





course_details = driver.find_element(By.XPATH,"/html/body/main/div[3]/div/div[2]")
components = course_details.find_elements(By.XPATH, './*')

for comp in components:
    if comp.text == '': continue
    print(comp.text)
    print("-------------------------------")


def print_direct_children(root: WebElement, level=0):
    children = root.find_elements(By.XPATH, "./*")
    indent = "\t" * level
    for child in children:
        class_name = child.get_attribute('class')
        if class_name == '':
            print(f'{indent}{child.text}')
        else:
            print(f'{indent}{class_name}')
        print_direct_children(child, level + 1)

print_direct_children(course_details)

