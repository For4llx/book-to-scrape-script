import requests, os, csv
from bs4 import BeautifulSoup
from helpers import get_soup, get_next_page, parse_product

count = 1
home_url = 'https://books.toscrape.com/index.html'
headers = [
  'product_page_url',
  'universal_ product_code',
  'product_title',
  'price_including_tax',
  'price_excluding_tax',
  'number_available',
  'product_description',
  'category',
  'review_rating',
  'image_url'
]

soup = get_soup(home_url)
#categories_url = ['https://books.toscrape.com/' + a['href'] for a in soup.find('div', class_='side_categories').findAll('ul')[1].findAll('a')]
categories_url = ['https://books.toscrape.com/catalogue/category/books/travel_2/index.html']

for category_url in categories_url:
    products = []
    current_page = 'index.html'

    while True:
        soup_category = get_soup(category_url)
        products_url = ['https://books.toscrape.com/catalogue/' + h3.find_next('a')['href'].replace('../', '') for h3 in soup_category.findAll('h3')]

        for product_url in products_url:
            soup = get_soup(product_url)
            products.append(parse_product(soup, product_url))

        category_name = soup.find('ul', class_='breadcrumb').findAll('a')[2].text.replace(' ', '_')
        product_title = soup.find('h1').text.replace(' ', '_')
        next_page = get_next_page(soup_category)

        if next_page:
            category_url = category_url.replace(current_page, next_page)
            current_page = next_page
        else:
            break

    csv_data = 'data/' + 'csv/' + category_name + '_' + str(count) + '.csv'
    os.makedirs(os.path.dirname(csv_data), exist_ok=True)

    with open(csv_data, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(headers)

        for product in [*products]:
            writer.writerow([*product])

    print(category_name + ' ' + 'succefully scraped.' + ' ' + str(count) + '/' + str(len(categories_url)))
    count = count + 1
