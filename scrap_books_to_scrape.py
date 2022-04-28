import requests
from bs4 import BeautifulSoup

product_page_url = []
universal_product_code = []
title = []
price_including_tax = []
price_excluding_tax = []
number_available = []
product_description = []
category = []
review_rating = []
image_url = []

catalogue_url = "https://books.toscrape.com/catalogue/"
travel_url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
response = requests.get(travel_url)

if response.ok:
    page = response.content
    soup = BeautifulSoup(page, "html.parser")
    product_page_url = [catalogue_url + h3.find_next('a')['href'].replace('../', '') for h3 in soup.findAll('h3')]

    for url in product_page_url:

        response = requests.get(url)

        if response.ok:
            page = response.content
            soup = BeautifulSoup(page, "html.parser")

            product_page_url = url
            product_information = [td.text for td in soup.find('table', class_='table table-striped').findAll('td')]
            product_title = soup.find('h1').text
            product_description = soup.find('div', id='product_description').find_next('p').text
            category = soup.find('ul', class_='breadcrumb').findAll('a')[2].text
            review_rating = soup.find('p', class_='star-rating')['class'][1]
            image_url = soup.find('img')['src']

            print(product_page_url)
