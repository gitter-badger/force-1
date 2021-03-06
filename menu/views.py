# -*- coding: utf-8 -*-

from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from models import Menu
from models import Category
from models import Product
from models import XLStructure

from classes.manager import MenuManager
from classes.downloader import download_menu_files


def load_menu_from_file(menu_file):
    manager = MenuManager()
    manager.add_menus_from_file(menu_file)

    menus = manager.menus
    for date, products_json in menus.iteritems():
        menu, menu_created = Menu.objects.get_or_create(date=date)

        products = []
        for product_json in products_json:
            category, category_created = Category.objects.get_or_create(
                name=product_json.get('category', 'default_category'))

            product, product_created = Product.objects.get_or_create(
                hash=Product.calculate_hash(
                    product_json.get('name', ''),
                    product_json.get('compound', ''),
                    product_json.get('weight', '')
                ),
                defaults={
                    'cost': product_json.get('cost', ''),
                    'name': product_json.get('name', ''),
                    'category': category,
                    'weight': product_json.get('weight'),
                    'compound': product_json.get('compound'),
                    'added': date
                }
            )

            xls, xls_created = XLStructure.objects.get_or_create(
                menu=menu,
                product=product,
                position=product_json.get('row')
            )

            products.append(product)

        menu.products = products
        menu.save()


def fetch_menu():
    # get provider, provider->get_fresh_menus
    menu_files = download_menu_files()
    for menu_file in menu_files:
        load_menu_from_file(menu_file)

    # TODO return not only boolean
    return True


@login_required
def load_menu(request):
    if fetch_menu():
        response = JsonResponse({
            'success': u'Menu successfully loaded'
        })
        response.status_code = 200
    else:
        response = JsonResponse({
            'error': u'Unable to load menu'
        })
        response.status_code = 503

    return response
