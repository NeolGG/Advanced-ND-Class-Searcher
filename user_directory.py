#!/usr/bin/env python3

import requests
from urllib.parse import quote
import json
import os


url = "https://api.identity.nd.edu/api/v1/user/_search?q="
json_folder = "jsons"

def fetch_data(query: str):
    api_query = quote(query)
    query_url = url + api_query
    
    print(query_url)
    
    response = requests.get(query_url)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.status_code} - {response.reason}")
        
    data = response.json()
    
    return data

def parse_user_data(json_data: list) -> list:
    '''
    looks through queried data and returns a list of users found
    
    if no users found, returns an empty list,otherwise\n
    
    returns: list of users found
    
    '''
    users = list()
    
    if len(json_data) == 0:
        print("No user data found")
        return users
        
    for d in json_data:
        classification = ": " + d["ndStudentClassification"] if d.get("ndStudentClassification") is not None else ""
        users.append(f"{d["firstName"]} {d["lastName"]} - {d["email"]} ({d["ndPrimaryAffiliation"]}{classification})")
        
    return users
        
def save_data(query:str, data: list):
    if not os.path.exists(json_folder) or not os.path.isdir(json_folder):
        os.mkdir(json_folder)
        
    count = len(os.listdir(json_folder))
    
    q_query = quote(query)
    
    with open(f'{json_folder}/response{count}_{q_query}.json', 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    query = "sylvia"
    
    data = fetch_data(query)
    
    user_list = parse_user_data(data)
    
    save_data(query, data)