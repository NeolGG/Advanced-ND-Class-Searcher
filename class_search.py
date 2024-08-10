#!/usr/bin/env python3

import requests
import json
from urllib.parse import quote
import os

url = "https://classsearch.nd.edu/api/?page=fose&route=search&camp=M&stat=A%2CF"
json_folder = "jsons"

def fetch_data(query: str):
    api_query = quote(query)
    headers = {'Content-Type': 'application/json',  'Accept': 'application/json',}
    payload = _create_payload(api_query)
    
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.status_code} - {response.reason}")
        
    data = response.json()
    
    return data

def _create_payload(keyword:str):
    '''
    creates encoded payload for post request
    payload includes data for:\n
    - fall 2024 ("srcdb": "202410")\n
    - main campus("field": "camp","value": "M")\n
    '''
    payload = {
        "other": {"srcdb": "202410"},
        "criteria": [
            {"field": "camp","value": "M"},
            {"field": "keyword","value": f"{keyword}"},
            {"field": "stat","value": "A,F"}
        ]
    }
    
    encoded_payload = json.dumps(payload)

    return encoded_payload

def parse_course_data(json_data: list) -> list:
    courses = list()
    
    if json_data['count'] == 0:
        print("No user data found")
        return courses

    for r in json_data['results']:
        listing = (f"{r["code"]} {r["title"]} - {r["instr"]}")
        if listing not in courses:
            courses.append(listing)

    return courses

def save_data(query:str, data: list):
    if not os.path.exists(json_folder) or not os.path.isdir(json_folder):
        os.mkdir(json_folder)
        
    count = len(os.listdir(json_folder))
    
    q_query = quote(query)
    
    with open(f'{json_folder}/classsearch_response{count}_{q_query}.json', 'w') as file:
        json.dump(data, file, indent=4)
        
def full_course_search(query: str) -> list:
    '''
    searches class search database and returns a list of courses 
    '''
    data = fetch_data(query)
    save_data(query,data)
    users = parse_course_data(data)
    
    return users

if __name__ == "__main__":
    query = "joanna"
    
    data = fetch_data(query)
    
    courses = parse_course_data(data)
    
    save_data(query,data)
    
    print(courses)
    

