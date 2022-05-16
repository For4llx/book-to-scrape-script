import requests, os, csv
from bs4 import BeautifulSoup
from helpers import get_soup, get_next_page, get_product, save_products, get_image, save_images

home_url = 'https://books.toscrape.com/index.html'

soup = get_soup(home_url)
categories_url = ['https://books.toscrape.com/' + a['href'] for a in soup.find('div', class_='side_categories').findAll('ul')[1].findAll('a')]

index_category = 1
for category_url in categories_url:
    products = []
    current_page = 'index.html'

    while True:
        soup_category = get_soup(category_url)
        products_url = ['https://books.toscrape.com/catalogue/' + h3.find_next('a')['href'].replace('../', '') for h3 in soup_category.findAll('h3')]

        for product_url in products_url:
            soup = get_soup(product_url)
            product = get_product(soup, product_url)
            products.append(product)

        next_page = get_next_page(soup_category)

        if next_page:
            category_url = category_url.replace(current_page, next_page)
            current_page = next_page
        else:
            break

    save_products(products, index_category)
    save_images(products, index_category)

    print('Data:' + str(index_category) + '/' + str(len(categories_url)))
    index_category = index_category + 1

print('Done. All data are successfully retrieved.')