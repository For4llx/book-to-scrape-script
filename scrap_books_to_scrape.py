import requests, os
from bs4 import BeautifulSoup
import csv

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

home_url = 'https://books.toscrape.com/index.html'
response = requests.get(home_url)

if response.ok:
    home_page = response.content
    soup = BeautifulSoup(home_page, "html.parser")
    categories_url = ['https://books.toscrape.com/' + a['href'] for a in soup.find('div', class_='side_categories').findAll('ul')[1].findAll('a')]

    for category_url in categories_url:
        page = 1
        pages = 2
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
                        product_information = [td.text for td in soup.find('table', class_='table table-striped').findAll('td')]
                        product_description_info = soup.find('div', id='product_description')
                        product_page_url.append(product_url)
                        universal_product_code.append(product_information[0])
                        price_including_tax.append(product_information[2])
                        price_excluding_tax.append(product_information[3])
                        number_available.append(product_information[5])
                        product_title.append(soup.find('h1').text)
                        if product_description_info is not None:
                            product_description.append(product_description_info.find_next('p').text)
                        category.append(soup.find('ul', class_='breadcrumb').findAll('a')[2].text)
                        review_rating.append(soup.find('p', class_='star-rating')['class'][1])
                        image_url.append('https://books.toscrape.com/' + soup.find('img')['src'].replace('../',''))
                        print(soup.find('h1').text)

                page = page+1
                if pagination is not None:
                    next_ = pagination.find('li', class_='next')
                    pages = pagination.find('li', class_='current').text.split()[-1]

                    if next_ is not None:
                        next_ = next_.a['href']
                        category_url = category_url.replace('index.html', next_)

        data = 'data/' + category[page] + '.csv'
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
