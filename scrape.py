import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time


from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection

SBR_WEBDRIVER = 'https://brd-customer-hl_815e11a3-zone-datahawk:t2v1xurwlh62@brd.superproxy.io:9515'
# This is the URL for the SuperBrowser Remote WebDriver service.


def scrape_website(website):
    print("Launching browser... Please wait.")

    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating to https://example.com...')
        driver.get('https://example.com')
        # CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Browser API's automatic CAPTCHA solver
        print('Waiting captcha to solve...')
        solve_res = driver.execute('executeCdpCommand', {
            'cmd': 'Captcha.waitForSolve',
            'params': {'detectTimeout': 10000},
        })
        print('Captcha solve status:', solve_res['value']['status'])
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print(html)
