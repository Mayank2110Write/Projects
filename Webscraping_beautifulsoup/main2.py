import requests
from bs4 import BeautifulSoup
import numpy as np

no_of_books = []

def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    books = soup.find_all("article", class_= "product_pod")

    for book in books:
        name = book.find("h3").find("a")["title"]
        rate = book.find("div", class_="product_price").find("p").text
        no_of_books.append({name, rate})
        print(f"name: {name}, price: {rate}")
        
for i in range (0,4):
    scrape(f"https://books.toscrape.com/catalogue/page-{i}.html")


# scrape("https://books.toscrape.com/catalogue/page-1.html")
# scrape("https://books.toscrape.com/catalogue/page-2.html")
# scrape("https://books.toscrape.com/catalogue/page-3.html")

print(np.count_nonzero(no_of_books))


