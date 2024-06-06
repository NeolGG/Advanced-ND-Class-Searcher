from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def click_search(driver):
    button = driver.find_element(By.XPATH,"/html/body/main/div[1]/div/div[2]/form/div[2]/div/div[5]/button")
    button.click()

def wait_for_element(driver, locator):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

def get_classes(driver):
    panel_body = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div[3]")
    classes = panel_body.find_elements(By.CSS_SELECTOR,".result.result--group-start")
    print(len(classes))
    return classes

def parse_class(class_ND: WebElement):
    class_ND.click()


driver = webdriver.Chrome()

driver.get("https://classsearch.nd.edu/")

print(driver.title)
print(driver.window_handles)
print(driver.current_window_handle)

click_search(driver)
class_list_locator = (By.CSS_SELECTOR,".result.result--group-start")
wait_for_element(driver,class_list_locator)
classes = get_classes(driver) # each is a webelement

parse_class(classes[0])

time.sleep(10)