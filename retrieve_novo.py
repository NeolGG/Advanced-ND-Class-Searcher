from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time


driver = webdriver.Chrome(options=options)

driver.get("https://bxeregprod.oit.nd.edu/StudentRegistration/ssb/term/termSelection?mode=search")