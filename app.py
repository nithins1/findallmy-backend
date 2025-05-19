from flask import Flask
from flask_cors import CORS
from playwright.sync_api import sync_playwright
from markdownify import markdownify as md
import time
import os
from dotenv import load_dotenv
import re
from flask import Flask, request, json
import llm
from log_util import log, reset_log

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
    # print('start', data)
    if 'url' not in data or data['url'] == '':
        results = llm.establishProfile(data['fullName'])
        return {'results': results}
    else:
        return llm.findContent(data)
    
@app.route("/find_content", methods=["POST"])
def findContentFromProfile():
    data = json.loads(request.data)
    # print('findContentFromProfile', data)

    return llm.findContent(data)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5001)
    reset_log()
