import requests, os, csv
from bs4 import BeautifulSoup

def get_soup(url):
    response = requests.get(url)

    if response.ok:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print('Error: response is not 200')

def get_next_page(soup):
    next_page = soup.find('li', class_='next')

    if next_page:
        return str(next_page.a['href'])
    else:
        return False

def get_product(soup, url):
    product_information = [td.text for td in soup.find('table', class_='table table-striped').findAll('td')]
    product_description_info = soup.find('div', id='product_description')
    product_page_url = url
    universal_product_code = product_information[0]
    price_including_tax = product_information[2]
    price_excluding_tax = product_information[3]
    number_available = product_information[5]
    product_title = soup.find('h1').text
    category = soup.find('ul', class_='breadcrumb').findAll('a')[2].text
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = 'https://books.toscrape.com/' + soup.find('img')['src'].replace('../','')

    if product_description_info:
        product_description = product_description_info.find_next('p').text
    else:
        product_description = 'no data'

    return [
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
    ]

def save_products(products, index_category):
        category = products[0][7].replace(' ', '_').lower()

        csv_data = 'data/' + 'csv/' + str(index_category) + '_' + category + '.csv'
        os.makedirs(os.path.dirname(csv_data), exist_ok=True)

        with open(csv_data, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(
                [
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
            )
            for product in products:
                writer.writerow(product)

def get_image(image_url):
    response = requests.get(image_url)

    if response.ok:
        return response.content
    else:
        print('Error: response is not 200')

def save_images(products, index_category):
    index = 1
    category = products[0][7].replace(' ', '_').lower()

    for product in products:
        image_url = product[9]
        image_name = product[5].replace(' ', '_').lower()
        image = get_image(image_url)

        images_data = 'data/' + 'images/' + str(index_category) + '_' + category +  '/' + str(index) + '_' + image_name + '.jpg'
        os.makedirs(os.path.dirname(images_data), exist_ok=True)

        open(images_data, "wb").write(image)
        index = index + 1
