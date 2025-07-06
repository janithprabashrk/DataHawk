import streamlit as st
from scrape import scrape_website


st.title("DataHawk")

url = st.text_input("Enter Website URL : ")

if st.button("Fetch Data"):
    st.write(f"Fetching data from {url}...")
    result = scrape_website(url)
    print(result)


from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
AUTH = 'brd-customer-hl_815e11a3-zone-datahawk:t2v1xurwlh62'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'
def main():
    print('Connecting to Browser API...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get('https://example.com')
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print(html)
if __name__ == '__main__':
  main()