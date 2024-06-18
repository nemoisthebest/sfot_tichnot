# Name: requests.py
# Author: emily h. (nemo) 
# Date: 30.04.24
# Description: webcralwer that receives a file with common file names on websites and tries to access them all.

import requests
from bs4 import BeautifulSoup
url = "https://example.com"
response = requests.get(url)

for link in url:
    href = link.get("href")
    if href.startswith("http"):
        response = requests.get(href)
