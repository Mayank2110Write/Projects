import requests
from bs4 import BeautifulSoup

def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")


    estates = soup.find_all("article", class_="StyledPropertyCard-c11n-8-100-8__sc-g2ckw9-0 gZYqpV StyledPropertyCard-srp-8-100-8__sc-1o67r90-0 edEmYz property-card list-card_not-saved")

    print(estates)
    # for estate in estates:
    #     price = 
