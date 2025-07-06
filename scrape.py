import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time


def scrape_website(website):
    print("Launching browser... Please wait.")

    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print(f"Page loaded...")
        html = driver.page_source
        time.sleep(2)  # Wait for the page to load completely

        return html
    
    finally:
        driver.quit()