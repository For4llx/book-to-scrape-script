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

home_url = 'https://books.toscrape.com/index.html'
response = requests.get(home_url)
if response.ok:
    home_page = response.content
    soup = BeautifulSoup(home_page, "html.parser")
    categories_url = ['https://books.toscrape.com/' + a['href'] for a in soup.find('div', class_='side_categories').findAll('ul')[1].findAll('a')]

    for category_url in categories_url:
        page = 0
        pages = 1
        while int(page) < int(pages):
            response = requests.get(category_url)

            if response.ok:
                category_page = response.content
                soup = BeautifulSoup(category_page, "html.parser")
                products_url = ['https://books.toscrape.com/catalogue/' + h3.find_next('a')['href'].replace('../', '') for h3 in soup.findAll('h3')]
                pagination = soup.find('ul', class_='pager')

                for product_url in products_url:
                    response = requests.get(product_url)

                    if response.ok:
                        product_page = response.content
                        soup = BeautifulSoup(product_page, "html.parser")
                        product_page_url = product_url
                        product_information = [td.text for td in soup.find('table', class_='table table-striped').findAll('td')]
                        product_title = soup.find('h1').text
                        product_description = soup.find('div', id='product_description').find_next('p').text
                        category = soup.find('ul', class_='breadcrumb').findAll('a')[2].text
                        review_rating = soup.find('p', class_='star-rating')['class'][1]
                        image_url = soup.find('img')['src']
                        print(product_title)

            page = page+1
            if pagination is not None:
                next_ = pagination.find('li', class_='next')
                pages = pagination.find('li', class_='current').text.split()[-1]
                if next_ is not None:
                    next_ = next_.a['href']
                    category_url = category_url.replace('index.html', next_)

