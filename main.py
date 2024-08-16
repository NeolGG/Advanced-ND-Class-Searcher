import os
import sys

from class_search import course_search,detailed_course
from user_directory import user_search,detailed_user


def find_room():
    print("Not Done")
    return 

def specific_search():
    print("Not Done")
    return

def full_search():
    u_input = input("Enter phrase to search in Notre Dame's databases: ")
    
    users = user_search(u_input)
    courses = course_search(u_input)

    def print_listings():
        nonlocal listings
        nonlocal index_map
        
        if users: 
            print("-----------Users-----------")
            for i, user in enumerate(users):
                print(f"{i}. {user[1]}")
            index_map[(len(listings), len(users) + len(listings) - 1)] = detailed_user
            listings += users
        
        if courses: 
            print("----------Courses----------")
            for i, course in enumerate(courses, len(listings)):
                print(f"{i}. {course[1]}")
            index_map[(len(listings), len(courses) + len(listings) - 1)] = detailed_course
            listings += courses
    
    while True:
        listings = list()
        index_map = dict()
        print_listings()
        
        if not index_map:
            print("No results found.")
            return
        
        print(f"{len(listings)}. RETURN")
        
        while True:
            try:
                index = int(input("Choose a result: "))
                if 0 <= index < len(listings):
                    chosen = listings[index]
                    for range_tuple, function in index_map.items():
                        if range_tuple[0] <= index <= range_tuple[1]:
                            function(chosen[0])  
                    break
                elif index == len(listings):
                    return
                else:
                    print("Invalid selection. Please choose a valid index.")
            except ValueError:
                print("Please enter a valid number.")
    
options = [("Full search",full_search), ("Find a free room",find_room), ("Specific search",specific_search), ("Exit",sys.exit)]

def main():
    while(1):
        print("Welcome to the ND OSINT Tool.")
        
        for i,o in enumerate(options):
            print(f"{i}. {o[0]}")
        while True:
            try:
                selection = int(input("Choose an option: "))
                if 0 <= selection < len(options):
                    break
                else:
                    print(f"Please enter a number between 0 and {len(options) - 1}.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        print(f"You selected: {options[selection][0]}")
        
        options[selection][1]()
        print()
    
    
if __name__ == "__main__":
    main()
    
    
    
    
'''

full search

displays all options

user_search
class_search


each one handles their one detailed search



'''