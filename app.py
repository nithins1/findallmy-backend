from flask import Flask
from flask_cors import CORS
from playwright.sync_api import sync_playwright
from markdownify import markdownify as md
import time
import os
from dotenv import load_dotenv
import re
import crawl
from flask import Flask, request, json
import llm

app = Flask(__name__)
CORS(app)

@app.route("/start", methods=["POST"])
def start():
    # url = "https://www.linkedin.com/in/caseywinters/"
    # page = crawl.linkedin_login()
    # html = crawl.scrape_page(page, url)
    # markdown = crawl.convert_to_markdown(html)
    # print(markdown)
    data = json.loads(request.data)
    print('start', data)
    if 'url' not in data or data['url'] == '':
        results = llm.establishProfile(data['fullName'])
        return {'results': results}
    else:
        llm.findAccounts(data)
        return {}
    
@app.route("/find_accounts", methods=["POST"])
def findAccountsFromProfile():
    data = json.loads(request.data)
    print('findAccountsFromProfile', data)

    return llm.findAccounts(data)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5001)
