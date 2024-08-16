#!/usr/bin/env python3

import requests
import json
from urllib.parse import quote
import os
import time
import sys
import re
import html


from modules.colors import Colors

__all__ = ["course_search","detailed_course"]

url = "https://classsearch.nd.edu/api/?page=fose&route=search&camp=M&stat=A%2CF"
details_url = "https://classsearch.nd.edu/api/?page=fose&route=details"
json_folder = "jsons/class_search"
class_json_file = None

def _fetch_courses(query: str) -> dict:
    '''
    creates encoded payload for post request.
    payload includes data for:\n
    - fall 2024 ("srcdb": "202410")\n
    - main campus("field": "camp","value": "M")\n
    
    returns: dict of raw courses
    '''
    api_query = quote(query)
    headers = {'Content-Type': 'application/json',  'Accept': 'application/json',}
    payload = {
        "other": {"srcdb": "202410"},
        "criteria": [
            {"field": "camp","value": "M"},
            {"field": "keyword","value": f"{api_query}"},
            {"field": "stat","value": "A,F"}
        ]
    }
    
    encoded_payload = json.dumps(payload)
    
    response = requests.post(url, headers=headers, data=encoded_payload)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.status_code} - {response.reason}")
    
    return response.json()


def _fetch_detailed(code: str,crn: str) -> list:
    '''
    payload includes data for specific semester, default is:\n
    - fall 2024 ("srcdb": "202410")\n
    '''
    payload = {"group": f"code:{code}",
               "key": f"crn:{crn}",
               "srcdb": "202410",
               "matched": f"crn:{crn}"}
    
    encoded_payload = json.dumps(payload)
    headers = {'Content-Type': 'application/json',  'Accept': 'application/json, text/javascript, */*; q=0.01',}
    response = requests.post(details_url, headers=headers, data=encoded_payload)
    
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.status_code} - {response.reason}")
    
    return response.json()

def _parse_course_data(json_data: list) -> list:
    '''
    parses through queried data and returns a list of courses found
    
    if no courses found, returns an empty list,otherwise\n
    
    returns: list of courses found
    
    '''
    courses = list()
    
    if json_data['count'] == 0:
        print("No course data found")
        return courses

    for r in json_data['results']:
        listing = (f"{r["code"]} {r["title"]} #{r["no"]} - {r["instr"]}")
        key = r["code"], r["crn"]
        courses.append((key,listing))

    return courses

def _save_course_data(query:str, data: list,subfolder: str):
    if subfolder.endswith('/'):
        subfolder = subfolder[:-1]
        
    destination = json_folder + '/' + subfolder
    
    if not os.path.exists(destination):
        os.makedirs(destination)
        
    t = time.time()
    
    q_query = quote(query)
    global class_json_file
    class_json_file = f'{destination}/class_search{t}_{q_query}.json'
    
    with open(class_json_file, 'w') as file:
        json.dump(data, file, indent=4)
        
def _remove_html_tags(text:str):
    """Remove HTML tags from a string using regular expressions."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def _clean_sections(raw:str) -> list:
    '''
    cleans the 'all_sections' entry\n
    return: list of all sections
    '''
    raw = _remove_html_tags(raw).strip()
    raw = html.unescape(raw)
    raw = raw.replace("VIEW CALENDAR","")
    raw = raw.replace("Section #CRNCampusTypeMeetsHoursInstructorDatesSeats","^")
    sections = list()
    key_value_dict = {}
    keys = ["Section #", "CRN", "Campus", "Type", "Meets", "Hours", "Instructor", "Dates", "Seats"]
    
    
    while(1):
        for key in keys[::-1]:
            pattern = rf"({key}:.*?)(?={key}:|$)"
            matches = list(re.finditer(pattern, raw))
            if matches:
                last_match = matches[-1]
                value = last_match.group(1).strip()
                key_value_dict[key] = value
                raw = raw[:last_match.start()] + raw[last_match.end():]
        
        sections.append(key_value_dict)
        
        if raw == "^":
            break
        
        key_value_dict = dict()
    
    return sections

def _clean_cannot_have_taken(raw:str) -> list:
    raw_clean = _remove_html_tags(raw)
    raw_clean = html.unescape(raw_clean).strip()
    return raw_clean.split('\n\n\n')

def _clean_attributes(raw:str):
    raw_clean = _remove_html_tags(raw)
    raw_clean = html.unescape(raw_clean).strip()
    raw_clean = raw_clean.replace(')',')^')
    return raw_clean.split('^')[:-1]

def _clean_inner_meeting_times(raw):
    raw_clean = _remove_html_tags(raw)
    raw_clean = html.unescape(raw_clean).strip()
    return json.loads(raw_clean)

def course_search(query: str) -> list:
    '''
    searches class search database and returns a list of courses 
    '''
    data = _fetch_courses(query)
    _save_course_data(query,data,"course_search")
    
    return _parse_course_data(data)

def detailed_course(key_tuple: tuple) -> dict:
    code,crn = key_tuple
    q_code = quote(code)
    expand = list()
    
    def _display_json(data: dict):
        for key, value in data.items():
            # cleaning 
            if key == "all_sections":
                value = _clean_sections(value)
            elif key == "cannot_have_taken":
                value = _clean_cannot_have_taken(value)
            elif key == "attribute_description":
                value = _clean_attributes(value)
            
            if isinstance(value, dict,) and value: # if value is dict 
                string = f"{Colors.BOLD}{Colors.OKCYAN}[{len(expand)}] {key}: {len(value)} pair(s){Colors.ENDC}"
                print(string)
                expand.append((string,value))
            elif isinstance(value, list) and value: #if value is list
                string = f"{Colors.BOLD}{Colors.OKCYAN}[{len(expand)}] {key}: {len(value)} item(s){Colors.ENDC}"
                print(string)
                expand.append((string,value))     
            elif value is not None:
                if isinstance(value, str): # cleaning if string only
                    v = _remove_html_tags(value)
                    v = html.unescape(v).strip()
                
                print(f"{Colors.BOLD}{key}:{Colors.ENDC} {Colors.OKGREEN}{v}{Colors.ENDC}")
                
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
                #cleaning
                if key == "meetingTimes":
                    new = _clean_inner_meeting_times(value)
                    _walk(new,level + 1)
                    continue
                
                print('\t' * level + f"{Colors.BOLD}{Colors.OKCYAN}{key}:{Colors.ENDC} ", end="")
                if isinstance(value, (dict,list)): # if value is dict or list
                    print()
                    _walk(value,level+1)
                else: # else
                    print(f"{Colors.BOLD}{value}{Colors.ENDC}")
        # if list
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                print('\t' * level + f"{Colors.BOLD}{Colors.OKCYAN}[{index}]:{Colors.ENDC} ",end="")
                if isinstance(item, (dict,list)): # if list item is either a dict or list
                    print()
                    _walk(item, level + 1)
                else: # else
                    if isinstance(item, str): # cleaning if string only
                        item = _remove_html_tags(item)
                        item = html.unescape(item).strip()
                    print(f"{Colors.BOLD}{item}{Colors.ENDC}")
        # if something else
        else:
            print('\t' * level + str(obj))
    
    data = _fetch_detailed(code,crn)
    _save_course_data(f"{q_code}_{crn}",data,"detailed")
    
    _display_json(data)

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
                print()
                _walk(expand[index][1])
            else:
                print(f"Please enter a number between 0 and {len(expand) - 1}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    pass
    
    

