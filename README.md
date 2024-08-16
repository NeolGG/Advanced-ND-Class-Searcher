# ND-OSINT-Tool

ND_OSINT TOOL

gets data from

classsearch -- for detailed class information
novo - for surface level class information
directory.nd.edu -- for person information

POA

- gather titles and surface level information using a database received from novo
- to obtain more informationt the user selects and in the background it will open up classearch, look for the class, and give the user the information

possible options:

- general search
- person search
- class search

reason for making it

These api/search features are publicly available. However, they lack documentation and are hidden.
By inspecting website code and network traffic using google chrome, I found the public api links.
I messed around with these links to see how they work and what challenges were required.

#challenges for each:
```
classearch - no notes needed for this one, it was very accessible after a quick network tab inspection using google chrome's DevTools
novo -  this requires chromedriver to access the website and click a few buttons to generate cookies. then these cookies can be used to create a python session with the request library and make requests for data
directory.nd.edu - this requires notre dame user login to access the website. However, the api is publicly available by looking at network traffic. You can also search for users on notre dame's main website without a notre dame login, which I thought was funny.
```
By taking a quick look at Notre dame's website it's apparent that a version of this tool exists.
But, I made this to learn more about website reconnaissance and web services.
I also prefer command line access as it is quicker to read and more lightweight for a cybersecurity setting. This tool also provides other features and information that is not immediately available on these websites.

ALSO, this application has the 'find a room' feature, which is intended for notre dame students who want to a find study spot in an academic building
    One of the main reasons for making this tool was because many of the library rooms are always reserved and i think it would be convenient 
    to have a quick tool to find a unused room in one of the academic buildings.

Lastly, this isn't ONLY a OSINT tool but also a wrapper for a lot of the hidden public APIs for the user list, course list, and course details provided by Notre Dame.

