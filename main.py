import requests
import sys
from bs4 import BeautifulSoup

HEADERS = {
        "User-Agent" : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
}


def get_price(url):
    page = requests.get(url, headers=HEADERS)
    print(page)
    soup = BeautifulSoup(page.content, 'html.parser')
    product_title = soup.find(id='productTitle').get_text().strip()
    print('Title - ', product_title)
    try:
        product_price = soup.find('span', class_='a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P').get_text()[2:]
    except:
        try:
            product_price = soup.find('span', class_='a-size-medium a-color-price priceBlockBuyingPriceString').get_text()[2:]
        except:
            sys.exit('Unable to find price!')
    print('Price - ', product_price)


if __name__ == '__main__':
    product_url = sys.argv[1]
    get_price(product_url)
