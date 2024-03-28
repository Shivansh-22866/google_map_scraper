from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time
import json
import re

firefox_options = webdriver.FirefoxOptions()

service = Service(
    GeckoDriverManager().install()
)

driver = webdriver.Firefox(
    service=service, options=firefox_options
)

keyword = "doctors"

driver.get(f"https://www.google.com/maps/search/{keyword}")

try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2)"))).click()
except Exception:
    pass

time.sleep(50)