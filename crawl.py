# from firecrawl import FirecrawlApp, ScrapeOptions
# import dotenv
# app = FirecrawlApp(api_key=dotenv.get_key('.env', 'FIRECRAWL_API_KEY'))

# # Scrape a website:
# scrape_status = app.scrape_url(
#   'https://www.linkedin.com/in/caseywinters/', 
#   formats=['markdown']
# )
# print(scrape_status)

from playwright.sync_api import sync_playwright
from markdownify import markdownify as md
import time
import os
from dotenv import load_dotenv
import re

load_dotenv()

EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def convert_to_markdown(html):
    return re.sub(r'^`.*\n?', '', md(html), flags=re.MULTILINE) 

def linkedin_login():
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Go to LinkedIn login page
    page.goto("https://www.linkedin.com/login")

    # Fill in login credentials
    page.fill('input#username', EMAIL)
    page.fill('input#password', PASSWORD)
    page.click('button[type="submit"]')

    # Optional: wait for login success
    page.wait_for_url("https://www.linkedin.com/feed/", timeout=10000)
    
    return page

def scrape_page(page, url):
    # Go to target profile
    page.goto(url, wait_until="load")
    time.sleep(3)  # Give time for content to load
    html = page.content()
    browser.close()
    return html

