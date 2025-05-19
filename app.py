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

# Initial contact with frontend
@app.route("/start", methods=["POST"])
def start():
    data = json.loads(request.data)
    
    # We consider a profile to be necessary. A name alone is insufficient.
    if 'url' not in data or data['url'] == '':
        # If the user doesn't provide a profle URL, we will search their name on Google 
        # and ask them to identify which one is theirs.
        results = llm.establishProfile(data['fullName'])
        return {'results': results}
    else:
        # Otherwise the provided data is enough to start searching.
        return llm.findContent(data)

# Given profile URL and name, return all contenet URLs for the person
@app.route("/find_content", methods=["POST"])
def findContentFromProfile():
    # User-provided info now includes name and profile URL
    data = json.loads(request.data)

    return llm.findContent(data)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5001)
    reset_log()
