from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint

def click_search(driver):
    button = driver.find_element(By.XPATH,"/html/body/main/div[1]/div/div[2]/form/div[2]/div/div[5]/button")
    button.click()

def wait_for_element(driver, locator):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

def get_courses(driver):
    panel_body = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div[3]")
    courses = panel_body.find_elements(By.CSS_SELECTOR,".result.result--group-start")
    print(len(courses))
    return courses

def parse_course(course_ND: WebElement):
    print(course_ND.text)
    # class_ND.click()


# headless options
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()

# driver get
driver.get("https://classsearch.nd.edu/")
print(f'scraping {driver.title}...')

# click search
click_search(driver)

# get list of courses
wait_for_element(driver,(By.CSS_SELECTOR,".result.result--group-start")) #waits for first class to appear
courses = get_courses(driver) # each is a webelement

courses[0].click()
wait_for_element(driver,(By.XPATH,"/html/body/main/div[3]/div/div[1]/a[2]/span")) #waits for home button to appear

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