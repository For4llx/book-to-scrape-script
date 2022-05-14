import requests, os
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

def parse_product(soup, url):
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
    else:
        product_description = 'no data'
    category = soup.find('ul', class_='breadcrumb').findAll('a')[2].text
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = 'https://books.toscrape.com/' + soup.find('img')['src'].replace('../','')

    images_data = 'data/' + 'images/' + category + '/' + product_title + '.jpg'
    os.makedirs(os.path.dirname(images_data), exist_ok=True)

    response = requests.get(image_url)
    open(images_data, "wb").write(response.content)

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
