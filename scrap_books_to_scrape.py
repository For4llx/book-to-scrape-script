import requests, os, csv
from bs4 import BeautifulSoup

def get_soup(url):
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        print('Error: response is not 200')

def get_next_page(soup):
    next_page = soup.find('li', class_='next')

    if next_page:
        next_page = str(next_page.a['href'])
        return next_page
    else:
        next_page = False
        return next_page

def get_products(array, soup, url):
    product_information = [td.text for td in soup.find('table', class_='table table-striped').findAll('td')]
    product_description_info = soup.find('div', id='product_description')
    product_page_url = url
    universal_product_code = product_information[0]
    price_including_tax = product_information[2]
    price_excluding_tax = product_information[3]
    number_available = product_information[5]
    product_title = soup.find('h1').text
    if product_description_info:
        product_description = product_description_info.find_next('p').text
    category = soup.find('ul', class_='breadcrumb').findAll('a')[2].text
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = 'https://books.toscrape.com/' + soup.find('img')['src'].replace('../','')

    products.append([
        product_page_url,
        universal_product_code,
        price_including_tax,
        price_excluding_tax,
        number_available,
        product_title,
        product_description,
        category,
        review_rating,
        image_url
    ])

    return products


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
categories_url = ['https://books.toscrape.com/' + a['href'] for a in soup.find('div', class_='side_categories').findAll('ul')[1].findAll('a')]

for category_url in categories_url:
    products = []
    current_page = 'index.html'

    while True:
        soup_category = get_soup(category_url)
        products_url = ['https://books.toscrape.com/catalogue/' + h3.find_next('a')['href'].replace('../', '') for h3 in soup_category.findAll('h3')]

        for product_url in products_url:
            soup = get_soup(product_url)
            products = get_products(products, soup, product_url)

        category_name = soup.find('ul', class_='breadcrumb').findAll('a')[2].text
        next_page = get_next_page(soup_category)

        if next_page:
            category_url = category_url.replace(current_page, next_page)
            current_page = next_page
        else:
            break

    data = 'data/' + category_name + '.csv'
    os.makedirs(os.path.dirname(data), exist_ok=True)

    with open(data, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(headers)

        for product in [*products]:
            writer.writerow([*product])
