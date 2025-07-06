import time
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup


SBR_WEBDRIVER = 'https://brd-customer-hl_815e11a3-zone-datahawk:t2v1xurwlh62@brd.superproxy.io:9515'
# This is the URL for the SuperBrowser Remote WebDriver service.


def scrape_website(website):
    print("Launching browser... Please wait.")

    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
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
        return html
    
def extract_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    body_content = soup.find('body')
    if body_content:
        return str(body_content)
    else:
        return "No body content found."
    
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()  
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return[
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]