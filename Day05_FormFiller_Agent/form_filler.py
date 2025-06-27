import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from faker import Faker
import time

# Load environment
load_dotenv()
fake = Faker()

# Setup Chrome Driver
chrome_driver_path = "./chromedriver.exe"
options = Options()
options.add_experimental_option("detach", True)
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open the test form page
driver.get("https://www.techlistic.com/p/selenium-practice-form.html")
time.sleep(2)

# Fill in fake name and email
driver.find_element(By.NAME, "firstname").send_keys(fake.first_name())
driver.find_element(By.NAME, "lastname").send_keys(fake.last_name())

# Click gender (Male)
driver.find_element(By.ID, "sex-0").click()

# Select experience (1 year)
driver.find_element(By.ID, "exp-1").click()

# Fill in date
driver.find_element(By.ID, "datepicker").send_keys("21-06-2025")

# Check profession
driver.find_element(By.ID, "profession-1").click()

# Upload a dummy file (optional)
# driver.find_element(By.ID, "photo").send_keys("C:/path/to/your/file.jpg")

# Click automation tool
driver.find_element(By.ID, "tool-2").click()

# Scroll and submit
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(1)
# Submit button is commented out in that form

print("✅ Form filled successfully!")
