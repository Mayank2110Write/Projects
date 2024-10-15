import requests
from bs4 import BeautifulSoup

with open("sample.html", "r") as f:
    html_doc = f.read()
    
soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.prettify())
# print(type(soup.find_all("div")[0]))

for link in soup.find_all("a"):
    print(link.get("href"))

