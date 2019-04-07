import time              
import re
import urllib.request 
from bs4 import BeautifulSoup
import requests
import json
import time


headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }


# Put the web link into the query after setting conditions in search enigne 
query = "https://github.com/search?q=stars%3A%3E10000+size%3A%3C1000000&type=Repositories" + "&p="


def get_list(query):
    #time.sleep(120)
    repo_list = []
    for p in range(1, 101):
        url = query + str(p)
        #with urllib.request.urlopen(url) as u:
         #   content = u.read()
        content = requests.get(url=url, headers=headers).text
        
        soup = BeautifulSoup(content,"html.parser")
        title_tab = soup.find_all("div",class_="col-12 col-md-8 pr-md-3")
        for tab in title_tab:
            title = tab.find("h3")
            print(title.get_text())
            repo_list.append(title.get_text().strip('\n'))
        if p % 9 == 0:
            time.sleep(122)
        print("Finished collecting data from page " + str(p))
    
    return repo_list


repo_list = get_list(query)

Archived = []
for repo in repo_list:
    if '\n' in repo:
        Archived.append(repo_list.index(repo))
for i in Archived:
    repo_list[i] = repo_list[i].split('\n')[0]

with open('repo.list.txt', 'w') as f:
    for item in repo_list:
        f.write("%s\n" %item)