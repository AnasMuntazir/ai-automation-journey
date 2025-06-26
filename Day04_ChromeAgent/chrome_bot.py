import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

# Setup Chrome driver
service = Service('./chromedriver.exe')  # Make sure chromedriver.exe is here
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    # Example: go to Wikipedia and search "AI"
    driver.get("https://www.wikipedia.org/")
    time.sleep(2)

    search_box = driver.find_element(By.NAME, "search")
    ai_input = ask_ai("Search something interesting about AI for me.")
    print(f"AI suggested search: {ai_input}")
    search_box.send_keys(ai_input)
    
    search_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    search_button.click()
    time.sleep(5)

    print("Search completed successfully.")
    driver.quit()

if __name__ == "__main__":
    main()
