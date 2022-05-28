from cgitb import text
from dataclasses import replace
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import uuid
import requests

s = HTMLSession()


def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def getnextpage(soup):
    page = soup.find('ul', {'class' : 'pagination'})
    
    # Finding the next button in the ul element
    a_list = []
    for a in page.find_all('a', href=True):
        a_list.append(a['href'])
    length = len(a_list)
    next_button = a_list[length-1]
    #print('Next button = ', next_button)
    if next_button is not None:
        url = 'https://www.proshop.dk' + next_button
        return url
    else:
        return

def parse(soup, shopname, shopurl):
    productPost = "http://localhost:8080/product/post"
    webpagePost = "http://localhost:8080/webpage/post"
    results = soup.find_all('li', {'class': 'toggle'})
    for item in results:
        productid = uuid.uuid4()
        productIdentifier = int(productid)
        product = {
            'id' : productIdentifier,
            'productname' : item.find({'h2': 'product-display-name'}).text,
            'picture' : 'stringOfPicture'
        }
        webpageid = uuid.uuid4()
        webpageIdentifier = int(webpageid)
        webpage = {
            'id' : webpageIdentifier,
            'webpagename' : shopname,
            'url' : shopurl + item.find('a', {'class': 'site-product-link'})['href'],
            'price' : float(item.find('span', {'class': 'site-currency-lg'}).text.replace('.', '').replace(',', '.').replace('kr', '')),
            'logo': 'stringOfLogo',
            'productid' : int(productid)
            }
        #print(product)
        #print(webpage)
        x = requests.post(productPost, json=product, timeout=2.50)
        y = requests.post(webpagePost, json=webpage, timeout=2.50)
        print('x status : ', x)
        print('y status : ', y)
    return

def scrape(url, shopname, shoplink):
    while True:
        soup = getdata(url)
        parse(soup, shopname, shoplink)
        prev_url = url
        url = getnextpage(soup)
        if not url:
            break
        print('URL = ', url)
        #print('Previous URL : ', prev_url)
        if prev_url == url:
            break

shopname = 'Proshop'
shoplink = 'https://www.proshop.dk'
url = 'https://www.proshop.dk/?s=ASUS'
scrape(url, shopname, shoplink)