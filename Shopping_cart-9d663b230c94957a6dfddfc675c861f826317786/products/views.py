# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shopping_cart.models import Order
from .models import Product
import sys

import requests

CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key=003b01314d6b90a73531d0a20b6e625e'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key=003b01314d6b90a73531d0a20b6e625e'
KEY = '003b01314d6b90a73531d0a20b6e625e'
DESC = 'http://api.themoviedb.org/3/movie/{imdbid}?api_key=003b01314d6b90a73531d0a20b6e625e'


def _get_json(url):
    r = requests.get(url)
    return r.json()



def get_poster_urls(imdbid):
    """ return image urls of posters for IMDB id
        returns all poster images from 'themoviedb.org'. Uses the
        maximum available size.
        Args:
            imdbid (str): IMDB id of the movie
        Returns:
            list: list of urls to the images
    """
    config = _get_json(CONFIG_PATTERN.format(key=KEY))
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']

    """
        'sizes' should be sorted in ascending order, so
            max_size = sizes[-1]
        should get the largest size as well.        
    """

    def size_str_to_int(x):
        return float("inf") if x == 'original' else int(x[1:])

    max_size = max(sizes, key=size_str_to_int)

    posters = _get_json(IMG_PATTERN.format(key=KEY, imdbid=imdbid))['posters']
    poster_urls = []
    for poster in posters:
        rel_path = poster['file_path']
        url = "{0}{1}{2}".format(base_url, max_size, rel_path)
        poster_urls.append(url)

    return poster_urls


def tmdb_posters(imdbid, count=None, outpath='.'):
    urls = get_poster_urls(imdbid)
    return urls[0]

def tmdb_desc(imdbid, count=None, outpath='.'):
    desc = _get_json(DESC.format(key=KEY, imdbid=imdbid))['overview']
    print(desc)
    return desc



@login_required()
def product_list(request):
    object_list = Product.objects.all()
    url_list = []
    for x in object_list:
        x.url = tmdb_posters(x.poster)
        #x.desc = tmdb_desc(x.poster)
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products,
        'url_list': url_list
    }

    return render(request, "products/product_list.html", context)