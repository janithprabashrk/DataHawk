import time
import os
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get BrightData configuration from environment variables
BRIGHTDATA_USERNAME = os.getenv('BRIGHTDATA_USERNAME', 'brd-customer-hl_815e11a3-zone-datahawk')
BRIGHTDATA_PASSWORD = os.getenv('BRIGHTDATA_PASSWORD', 't2v1xurwlh62')
BRIGHTDATA_ENDPOINT = os.getenv('BRIGHTDATA_ENDPOINT', 'brd.superproxy.io:9515')

SBR_WEBDRIVER = f'https://{BRIGHTDATA_USERNAME}:{BRIGHTDATA_PASSWORD}@{BRIGHTDATA_ENDPOINT}'


def scrape_website(website):
    """
    Scrape website content using BrightData proxy service.
    """
    if not website:
        return "Error: No website URL provided."
    
    if not website.startswith(('http://', 'https://')):
        website = 'https://' + website
    
    try:
        print("Launching browser... Please wait.")

        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            driver.get(website)
            
            # CAPTCHA handling: If you're expecting a CAPTCHA on the target page
            print('Waiting for CAPTCHA to solve...')
            solve_res = driver.execute('executeCdpCommand', {
                'cmd': 'Captcha.waitForSolve',
                'params': {'detectTimeout': 10000},
            })
            print('CAPTCHA solve status:', solve_res['value']['status'])
            print('Navigated! Scraping page content...')
            
            html = driver.page_source
            return html
            
    except Exception as e:
        error_msg = f"Error scraping website: {str(e)}"
        print(error_msg)
        return error_msg
    
def extract_body_content(html):
    """
    Extract body content from HTML.
    """
    if not html or html.startswith("Error:"):
        return html
        
    try:
        soup = BeautifulSoup(html, 'html.parser')
        body_content = soup.find('body')
        if body_content:
            return str(body_content)
        else:
            return "No body content found."
    except Exception as e:
        return f"Error extracting body content: {str(e)}"
    
def clean_body_content(body_content):
    """
    Clean HTML body content by removing scripts, styles and formatting text.
    """
    if not body_content or body_content.startswith("Error:") or body_content == "No body content found.":
        return body_content
        
    try:
        soup = BeautifulSoup(body_content, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.extract()  
            
        # Get text content with line separators
        cleaned_content = soup.get_text(separator="\n")
        
        # Clean up whitespace and empty lines
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )
        return cleaned_content
        
    except Exception as e:
        return f"Error cleaning content: {str(e)}"

def split_dom_content(dom_content, max_length=6000):
    """
    Split DOM content into chunks for AI processing.
    """
    if not dom_content or dom_content.startswith("Error:"):
        return [dom_content]
        
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]