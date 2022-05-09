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
    product_page_url = []
    universal_product_code = []
    product_title = []
    price_including_tax = []
    price_excluding_tax = []
    number_available = []
    product_description = []
    category = []
    review_rating = []
    image_url = []
    current_page = 'index.html'

    while True:
        soup_category = get_soup(category_url)
        products_url = ['https://books.toscrape.com/catalogue/' + h3.find_next('a')['href'].replace('../', '') for h3 in soup_category.findAll('h3')]

        for product_url in products_url:
            soup = get_soup(product_url)
            product_information = [td.text for td in soup.find('table', class_='table table-striped').findAll('td')]
            product_description_info = soup.find('div', id='product_description')
            product_page_url.append(product_url)
            universal_product_code.append(product_information[0])
            price_including_tax.append(product_information[2])
            price_excluding_tax.append(product_information[3])
            number_available.append(product_information[5])
            product_title.append(soup.find('h1').text)
            if product_description_info:
                product_description.append(product_description_info.find_next('p').text)
            category.append(soup.find('ul', class_='breadcrumb').findAll('a')[2].text)
            category_name = soup.find('ul', class_='breadcrumb').findAll('a')[2].text
            review_rating.append(soup.find('p', class_='star-rating')['class'][1])
            image_url.append('https://books.toscrape.com/' + soup.find('img')['src'].replace('../',''))
            print(soup.find('h1').text)

        next_page = get_next_page(soup_category)
        print(next_page)

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

        for url, upc, title, price_tax_inc, price_tax_ex, number, description, category, rating, img_url in zip(
            product_page_url,
            universal_product_code,
            product_title,
            price_including_tax,
            price_excluding_tax,
            number_available,
            product_description,
            category,
            review_rating,
            image_url):

            writer.writerow([url, upc, title, price_tax_inc, price_tax_ex, number, description, category, rating, img_url])
