from googlesearch import search
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=OPENAI_KEY,
)


# Given a person's name, find an account owned by them which provides a profile
def establishProfile(fullName):
    results = search(fullName, num_results=10, unique=True, advanced=True)
    return [{'url': r.url, 'title': r.title, 'description': r.description} for r in results]

def getDescriptionFromProfileUrl(url):
    results = list(search(url, num_results=1, advanced=True))
    print(url)
    print('getDescriptionFromProfileUrl', results)
    return results[0].description

def findAccounts(personInfo):
    print('findAccounts', personInfo)
    if 'url' in personInfo and personInfo['url'] != '':
        personInfo['profileDescription'] = getDescriptionFromProfileUrl(personInfo['url'])

    personInfo['url'] = personInfo['title'] = personInfo['description'] = None
    instructionsString = f"""You are given some information about a person: their \
name and profile description, and possibly some more. You will have to predict \
if a given Google search result is an account that belongs to the person, \
or a different person with the same name.\n\
The information is:\n"""
    
    for key, value in personInfo.items():
        if value:
            instructionsString += f"{key}: {value}\n"
    
    
    results = list(search(personInfo['fullName'], num_results=10, unique=True, advanced=True))
    messages = [{"role": "system", "content": instructionsString}]
    print('instructions:', instructionsString, end='\n\n')
    for result in results:
        questionString = f"""Is this an account owned by the person? \n\
title: {result.title}\n\
description: {result.description}\n\
url: {result.url}\n\
Respond with only Yes or No."""

        messages.append({"role": "user", "content": questionString})
        # response = ""
        # response = client.responses.create(
        #     model="gpt-4o",
        #     instructions=instructionsString,
        #     input=questionString,
        # )
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        print('question:', questionString, end='\n\n')
        print('response:', response.choices[0].message.content, end='\n\n')
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
    return {}