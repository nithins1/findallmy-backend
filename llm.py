from googlesearch import search
from openai import OpenAI
from dotenv import load_dotenv
import os
from log_util import log
from urllib.parse import urlparse

NUM_RESULTS_FOR_ESTABLISHING_PROFILE = 10
NUM_RESULTS_FOR_FINDING_ACCOUNTS = 10
NUM_RESULTS_FOR_CONTENT_SEARCH = 10

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=OPENAI_KEY,
)


# Given a person's name, find an account owned by them which provides a profile
def establishProfile(fullName):
    results = search(fullName, num_results=NUM_RESULTS_FOR_ESTABLISHING_PROFILE, unique=True, advanced=True)
    return [{'url': r.url, 'title': r.title, 'description': r.description} for r in results]

def getDescriptionFromProfileUrl(url):
    results = list(search(url, num_results=1, advanced=True))
    # print(url)
    # print('getDescriptionFromProfileUrl', results)
    return results[0].description

def findContent(personInfo):
    # print('findContent', personInfo)
    if 'url' in personInfo and personInfo['url'] != '':
        personInfo['profileDescription'] = getDescriptionFromProfileUrl(personInfo['url'])

    personInfo['url'] = personInfo['title'] = personInfo['description'] = None
    instructionsString = f"""You are given some information about a person: their \
name and profile description, and possibly some more. You will have to predict \
if a given Google search result is an account that belongs to the person, \
or a different person with the same name.\n\
The information about the person is:\n"""
    
    for key, value in personInfo.items():
        if value:
            instructionsString += f"{key}: {value}\n"
    
    
    results = list(search(personInfo['fullName'], num_results=NUM_RESULTS_FOR_FINDING_ACCOUNTS, unique=True, advanced=True))
    print('results', results)
    print('results length', len(results))
    log(f'instructions: {instructionsString}')
    userAccounts = []
    for result in results:
        questionString = f"""Is this an account owned by the person? \n\
title: {result.title}\n\
description: {result.description}\n\
url: {result.url}\n\
Respond with only Yes or No."""

        # response = ""
        response = client.responses.create(
            model="gpt-4o",
            instructions=instructionsString,
            input=questionString,
        )
        log(f'question: {questionString}')
        log(f'response: {response.output_text}')
        
        if 'yes' in response.output_text.lower():
            userAccounts.append(result)
    
    print('userAccounts:', userAccounts)
    print('userAccounts length:', len(userAccounts))
    contentList = {}
    for account in userAccounts:
        parsed_url = urlparse(account.url)
        print('parsed_url:', parsed_url.netloc)
        contentList[parsed_url.netloc] = searchSite(account, personInfo)
    return contentList

def searchSite(account, personInfo):
    instructionsString = f"""You are given some information about a person: their \
name and profile description, and possibly some more. You will be given a numbered list \
of Google search results and you have to predict if each one is content created by the person. \
Respond with a numbered list of Yes or No, one for each result. Yes means the content was created by \
the person, or features the person's voice, content, etc. No means the content was created by someone \
else, possibly someone with the same name.\n\
The information about the person is:\n"""
    
    for key, value in personInfo.items():
        if value:
            instructionsString += f"{key}: {value}\n"
            
    log(f'instructions: {instructionsString}')
    # print(account)
    parsed_url = urlparse(account.url)
    # improvement would be to search with person's alias instead of full name if appropriate
    results = list(search(f'site:{parsed_url.netloc} {personInfo['fullName']}', num_results=NUM_RESULTS_FOR_CONTENT_SEARCH, advanced=True))
    
    questionString = ""
    for i in range(1, NUM_RESULTS_FOR_CONTENT_SEARCH + 1):
        questionString += f"{i}. Title: {results[i - 1].title}, Description: {results[i - 1].description}, {results[i - 1].url}\n"
        
    response = client.responses.create(
            model="gpt-4o",
            instructions=instructionsString,
            input=questionString,
    )
    log(f'question: {questionString}')
    log(f'response: {response.output_text}')
    content = []
    for i, line in enumerate(response.output_text.split('\n')):
        if 'yes' in line.lower():
            content.append(results[i].url)
    return content