from django.shortcuts import render
from .models import Item
from django.utils import timezone
from django.db.utils import OperationalError
from django.http import Http404


import logging
import requests
import uuid
from bs4 import BeautifulSoup
import re
import datetime

class Hedgehog(object):

    def __init__(self, url, pk):
        self.headers = { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36', 'referer': 'https://www.google.com'}
        self.url = url
        self.pk = pk

    def completeLoad(self):
        r = requests.get(self.url, headers = self.headers)

        status = r.status_code
        if status == 403:
            raise Http404("Website refused connection.")
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
            try:
                prices = product.find('div', class_='item-details').findChildren("strong")[0]
            except:
                sanity = False
            if sanity:
                try:
                    regular_price = float(re.findall(r">.*<", str(prices.find('span', class_='price regular')))[0][2:-1])
                except:
                    regular_price = None
                try:
                    sale_price = float(re.findall(r">.*<", str(prices.find('span', class_='price sale')))[0][2:-1])
                    on_sale = True
                except:
                    on_sale = False
            if on_sale:
                discount = 100*(regular_price - sale_price)/regular_price
            else:
                discount = None

            item = Item.objects.create(link=link, group = self.pk, category=category, title=title, 
                    regular_price=regular_price, sale_price = sale_price, discount=discount)


def home(request):
    return render(request, 'home.html')

def men(request):
    try:
        items_men = Item.objects.get(group=0)
        print('here')
        delta = timezone.localtime() - items_men[0].date
        if delta.days > 1:
            Item.objects.filter(group=0).delete()
            men_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductmen/view-all.html', 0)
            men_sales.crawl()
    except:
        men_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductmen/view-all.html', 0)
        men_sales.crawl()
    items = Item.objects.filter(group=0).order_by('-discount')
    return render(request, 'men.html', {'items': items})

def women(request):
    try:
        items_women = Item.objects.filter(group=1)
        delta = timezone.localtime() - items_women[0].date
        if delta.days > 1:
            Item.objects.filter(group=1)().delete()
            women_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductladies/view-all.html', 1)
            women_sales.crawl()
    except:
        women_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductladies/view-all.html', 1)
        women_sales.crawl()
    items = Item.objects.filter(group=1).order_by('-discount')
    return render(request, 'women.html', {'items': items})

def divided(request):
    try:
        items_divided = Item.objects.filter(group=2)
        delta = timezone.localtime() - items_divided[0].date
        if delta.days > 1:
            Item.objects.filter(group=2).delete()
            divided_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductdivided/view-all.html', 2)
            divided_sales.crawl()
    except:
        divided_sales = Hedgehog('https://www2.hm.com/en_ca/sale/shopbyproductdivided/view-all.html', 2)
        divided_sales.crawl()
    items = Item.objects.filter(group=2).order_by('-discount')
    return render(request, 'divided.html', {'items': items})
