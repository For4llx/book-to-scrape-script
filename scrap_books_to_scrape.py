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

category_index_url = 'https://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
response = requests.get(category_index_url)

if response.ok:
    category_index_page = response.content
    soup = BeautifulSoup(category_index_page, "html.parser")

    pages = soup.find('li', class_='current').text.split()[-1]

catalogue_url = "https://books.toscrape.com/catalogue/"

for page in range(int(pages)+1):
    category_url = 'https://books.toscrape.com/catalogue/category/books/mystery_3/page-{page}.html'.format(page=page)
    response = requests.get(category_url)

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

                print(product_title)
