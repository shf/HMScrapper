from django.shortcuts import render
from .models import Item, Item_men, Item_women, Item_divided
from django.utils import timezone

import logging
import requests
import uuid
from bs4 import BeautifulSoup
import re
import datetime

class Hedgehog(object):

    def __init__(self, url, pk):
        self.headers = { 'user-agent': 'Chrome/56.1.2924.87' }
        self.url = url
        self.pk = pk

    def completeLoad(self):
        r = requests.get(self.url, headers = self.headers)

        status = r.status_code
        content = BeautifulSoup(r.content, 'html.parser')
        html = list(content.children)[2]
        num_of_products = html.find_all('h2', class_='load-more-heading')[0].get('data-total')
        return num_of_products

    def crawl(self):

        num_of_products = self.completeLoad()
        r = requests.get(self.url + f'?sort=stock&image-size=small&image=stillLife&offset=0&page-size={num_of_products}', headers = self.headers)
        content = BeautifulSoup(r.content, 'html.parser')
        html = list(content.children)[2]
        product_list = html.find_all('ul', class_='products-listing small')[0].find_all('li', class_='product-item')
        for product in product_list:
            on_sale = False
            sanity = True
            category = product.find('article', class_='hm-product-item').get('data-category')
            link = product.find('div', class_='image-container').findChildren("a" , recursive=False)[0].get('href')
            title = product.find('div', class_='image-container').findChildren("a" , recursive=False)[0].get('title')
            prices = product.find('div', class_='item-details').findChildren("strong")[0]
            try:
                regular_price = float(re.findall(r">.*<", str(prices.find('span', class_='price regular')))[0][2:-1])
            except:
                regular_price = None
            try:
                sale_price = float(re.findall(r">.*<", str(prices.find('span', class_='price sale')))[0][2:-1])
                on_sale = True
            except:
                regular_price = None
                sanity = False
            if on_sale and sanity:
                discount = 100*(regular_price - sale_price)/regular_price
            else:
                discount = None

            if self.pk == 0:
                item = Item_men.objects.create(link=link, category=category, title=title, 
                    regular_price=regular_price, sale_price = sale_price, discount=discount)
            elif self.pk == 1:
                item = Item_women.objects.create(link=link, category=category, title=title, 
                    regular_price=regular_price, sale_price = sale_price, discount=discount)
            elif self.pk == 2:
                item = Item_divided.objects.create(link=link, category=category, title=title, 
                    regular_price=regular_price, sale_price = sale_price, discount=discount)


def home(request):
    return render(request, 'home.html')

def men(request):
    try:
        delta = timezone.localtime() - Item_men.objects.all()[1].date
        if delta.days > 1:
            Item_men.objects.all().delete()
            men_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductmen/view-all.html', 0)
            men_sales.crawl()
    except:
        men_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductmen/view-all.html', 0)
        men_sales.crawl()
    items = Item_men.objects.all().order_by('-discount')
    return render(request, 'men.html', {'items': items})

def women(request):
    try:
        delta = timezone.localtime() - Item_women.objects.all()[1].date
        if delta.days > 1:
            Item_women.objects.all().delete()
            women_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductladies/view-all.html', 1)
            women_sales.crawl()
    except:
        women_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductladies/view-all.html', 1)
        women_sales.crawl()
    items = Item_women.objects.all().order_by('-discount')
    return render(request, 'women.html', {'items': items})

def divided(request):
    try:
        delta = timezone.localtime() - Item_divided.objects.all()[1].date
        if delta.days > 1:
            Item_divided.objects.all().delete()
            divided_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductdivided/view-all.html', 2)
            divided_sales.crawl()
    except:
        divided_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductdivided/view-all.html', 2)
        divided_sales.crawl()
    items = Item_divided.objects.all().order_by('-discount')
    return render(request, 'divided.html', {'items': items})
