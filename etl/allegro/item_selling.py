import json
import re

from bs4 import BeautifulSoup

from commons.utils import text_from_soup

# "num_items_available": None,
buyers_count_selector = ".buyers-count strong:nth-of-type(1)"
bought_items_count_selector = ".buyers-count strong:nth-of-type(2)"
available_items_count_selector = "#quantity ~ span"
parameters_keys_selector = "section.attributes-block > div li > span:nth-of-type(1)"
parameters_values_selector = "section.attributes-block > div li > span:nth-of-type(2)"


def get_parameters(soup):
    try:
        parameters_keys = [e.text[:-1].strip() for e in
                           soup.select(parameters_keys_selector)]
        parameters_values = [e.text.strip() for e in
                             soup.select(parameters_values_selector)]
        parameters = dict(zip(parameters_keys, parameters_values))
        return parameters
    except:
        return dict()


def get_data_layer(soup):
    try:
        data_layer = json.loads(re.search("dataLayer = \[(.*)\]", soup.text, re.MULTILINE).groups()[0])
        return data_layer
    except:
        return dict()


def get_item_id(data_layer):
    return data_layer.get('idItem')


def get_category_id(data_layer):
    return data_layer.get('idCategory')


def get_category_name(data_layer):
    return data_layer.get('nameCategory')


def get_category_tree(data_layer):
    return data_layer.get('headNavigation')


def get_price(data_layer):
    return data_layer.get('price')


def get_nick(data_layer):
    return data_layer.get('sellerName')


def get_description(soup):
    try:
        return text_from_soup(soup)
    except:
        return None


def get_title(soup):
    try:
        return re.search("(.*)\s\(\d+\) - Allegro.pl - Więcej niż aukcje.", soup.find("title").text).groups()[0]
    except:
        return None


def get_item_condition(parameters):
    try:
        return parameters.pop('stan')
    except:
        return None

def get_item_invoice(parameters):
    try:
        return parameters.pop('faktura')
    except:
        return None


def get_buyers_count(soup):
    try:
        # noinspection PyUnresolvedReferences
        return int(re.search("(\d+)", soup.select_one(buyers_count_selector).text)[0])
    except:
        return None


def get_bought_items_count(soup):
    try:
        # noinspection PyUnresolvedReferences
        return int(re.search("(\d+)", soup.select_one(bought_items_count_selector).text)[0])
    except:
        return None


def get_available_items_count(soup):
    try:
        # noinspection PyUnresolvedReferences
        return int(re.search("(\d+)", soup.select_one(available_items_count_selector).text)[0])
    except:
        return None

def extract_data_from_item(ad_file):
    with open(ad_file, 'r') as myfile:
        print("Processing file: {}".format(ad_file))
        data = myfile.read()

    soup = BeautifulSoup(data, 'html.parser')

    data_layer = get_data_layer(soup)
    parameters = get_parameters(soup)

    item_id = get_item_id(data_layer)
    category_id = get_category_id(data_layer)
    category_name = get_category_name(data_layer)
    category_tree = get_category_tree(data_layer)
    price = get_price(data_layer)
    nick = get_nick(data_layer)
    description = get_description(soup)
    title = get_title(soup)
    item_condition = get_item_condition(parameters)
    item_invoince = get_item_invoice(parameters)
    buyers_count = get_buyers_count(soup)
    bought_items_count = get_bought_items_count(soup)
    available_items_count = get_available_items_count(soup)

    return {
        "item_id": item_id,
        "title": title,
        "description": description,
        "category_id": category_id,
        "category_name": category_name,
        "category_tree": category_tree,
        "price": price,
        "available_items_count": available_items_count,
        "buyers_count": buyers_count,
        "bought_items_count": bought_items_count,
        "parameters": parameters,
        "item_condition": item_condition,
        "item_invoice": item_invoince,
        "nick": nick,
    }

