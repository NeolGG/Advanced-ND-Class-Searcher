#!/usr/bin/env python3

import requests
from urllib.parse import quote
import json
import os
import time

from modules.colors import Colors

__all__ = ["user_search","detailed_user"]

url = "https://api.identity.nd.edu/api/v1/user/_search?q="
json_folder = "jsons/users"
user_json_file = None

def _fetch_data(query: str):
    '''
    queries data from public api using query string
    
    returns: data in json format, dictionary
    '''
    api_query = quote(query)
    query_url = url + api_query
    
    response = requests.get(query_url)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.status_code} - {response.reason}")
    
    return response.json()

def _parse_user_data(json_data: list) -> list:
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
        unique_key = d["email"]
        users.append((unique_key,f"{d["firstName"]} {d["lastName"]} - {d["email"]} ({d["ndPrimaryAffiliation"]}{classification})"))
        
    return users
        
def _save_data(query:str, data: list, subfolder:str):
    if subfolder.endswith('/'):
        subfolder = subfolder[:-1]
    
    destination = json_folder + '/' + subfolder
    
    if not os.path.exists(destination):
        os.makedirs(destination)
        
    t = time.time()
    
    q_query = quote(query)
    global user_json_file
    user_json_file = f'{destination}/user{t}_{q_query}.json'
    
    with open(user_json_file, 'w') as file:
        json.dump(data, file, indent=4)
        
def user_search(query: str) ->list:
    '''
    searches ND user directory and returns a list of users 
    '''
    data = _fetch_data(query)
    _save_data(query,data,"user_search")
    
    return _parse_user_data(data)

def detailed_user(netid:str):
    '''
    fetches detailed user information
    '''
    
    expand = list()
    
    def _display_json(data: dict): 
        for key, value in data.items():
            if isinstance(value, dict,) and value: # if value is dict 
                string = f"{Colors.BOLD}{Colors.OKCYAN}[{len(expand)}] {key}: {len(value)} pair(s){Colors.ENDC}"
                print(string)
                expand.append((string,value))
            elif isinstance(value, list) and value: #if value is list
                string = f"{Colors.BOLD}{Colors.OKCYAN}[{len(expand)}] {key}: {len(value)} item(s){Colors.ENDC}"
                print(string)
                expand.append((string,value))     
            elif value:
                print(f"{Colors.BOLD}{key}:{Colors.ENDC} {Colors.OKGREEN}{value}{Colors.ENDC}")
                    
    def _walk(obj, level=0):
        """
        Recursively walks through a list or dictionary, printing each non-None item
        with the correct indentation.
        
        :param obj: The object to walk through (list or dict).
        :param level: The current level of indentation (used internally).
        """
        # if dict
        if isinstance(obj, dict):
            for key, value in obj.items():
                print('\t' * level + f"{Colors.BOLD}{Colors.OKCYAN}{key}:{Colors.ENDC} ", end="")
                if isinstance(value, (dict,list)):
                    print()
                    _walk(value,level+1)
                else:
                    print(f"{Colors.BOLD}{value}{Colors.ENDC}")
        # if list
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                print('\t' * level + f"{Colors.BOLD}{Colors.OKCYAN}[{index}]:{Colors.ENDC} ",end="")
                if isinstance(item, (dict,list)):
                    print()
                    _walk(item, level + 1)
                else:
                    print(f"{Colors.BOLD}{item}{Colors.ENDC}")
        # if something else
        else:
            print('\t' * level + str(obj))
                
    data = _fetch_data(netid)
    _save_data(netid,data,"detailed")
    
    _display_json(data[0])
    
    length = len(expand)
    expand.append((f"{Colors.BOLD}[{length}] RETURN{Colors.ENDC}",None))
    
    while True:
        print()
        for e in expand:
            print(e[0])
            
        try:
            index = int(input("\nChoose one of the options: "))
            if index == len(expand) - 1:
                return
            elif 0 <= index < len(expand):
                _walk(expand[index][1])
            else:
                print(f"Please enter a number between 0 and {len(expand) - 1}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    pass