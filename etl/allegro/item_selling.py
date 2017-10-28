import json
import re

from bs4 import BeautifulSoup

from commons.utils import text_from_soup

is_new_selector = '#showitem-main > section.attributes-block > div > ul:nth-of-type(1) > li:nth-of-type(1) > ' \
                  'span.attribute-value'
is_invoice_selector = "#showitem-main > section.attributes-block > div > ul:nth-of-type(1) > li:nth-of-type(2) > " \
                      "span.attribute-value"
buy_now_price_selector = "#purchase-form > div.col-sm-7.col-xs-12 > div:nth-child(1) > div.price"
item_price_and_quantity_field = "#purchase-form > div.col-sm-7.col-xs-12"
how_many_people_bough_how_many_items_field = "#preinfo-container > div > div.col-xs-12.col-sm-4.col-md-4.buyers-count" \
                                             " > span"
seller_name_field = "#seller-details > div.btn.btn-default.btn-user > a > span"
item_name = "#showitem-main > section:nth-of-type(6) > div > h1"  # substract element in small which is id

parameters_key_selector = "section.attributes-block > div li:nth-of-type(1)"
parameters_values_selector = "section.attributes-block > div"


def extract_data_from_item(ad_file):
    with open(ad_file, 'r') as myfile:
        data = myfile.read()

    soup = BeautifulSoup(data, 'html.parser')

    # parameters
    parameters_keys = [e.text[:-1].strip() for e in
                       soup.select("section.attributes-block > div li > span:nth-of-type(1)")]
    parameters_values = [e.text.strip() for e in soup.select("section.attributes-block > div li > span:nth-of-type(2)")]
    parameters = dict(zip(parameters_keys, parameters_values))

    # data layer
    data_layer = json.loads(re.search("dataLayer = \[(.*)\]", soup.text, re.MULTILINE).groups()[0])
    item_id = data_layer.get('idItem')
    category_id = data_layer.get('idCategory')
    category_name = data_layer.get('nameCategory')
    category_tree = data_layer.get('headNavigation')
    price = data_layer.get('price')
    nick = data_layer.get('sellerName')

    # description
    description = text_from_soup(soup)

    # title
    title = re.search("(.*)\s\(\d+\) - Allegro.pl - Więcej niż aukcje.", soup.find("title").text).groups()[0]

    return {
        "item_id": item_id,
        "title": title,
        # "description": description,
        "category_id": category_id,
        "category_name": category_name,
        "category_tree": category_tree,
        "price": price,
        "num_items_available": None,
        "bought_users": None,
        "bought_items": None,
        # "parameters": parameters,
        "nick": nick,
    }

    # data_layer_json

    # contact_data_field = soup.select_one(contact_data_selector)
    # phone_number_field = soup.select_one(phone_number_selector)
    # email_field = soup.select_one(email_selector)
    # username_field = soup.select_one(username_selector)
    # all_fields = soup.find(id=all_fields_id)
    #
    # nip = get_nip(contact_data_field)
    # phone_number = get_phone_number(phone_number_field)
    # username = get_username(username_field)
    # email = get_email(email_field)
    # other_candidate_numbers = get_other_candidate_numbers(all_fields, [phone_number, nip])
    #
    # return {
    #     "id": id,
    #     "nip": nip,
    #     "phone_number": phone_number,
    #     "username": username,
    #     "email": email,
    #     "other_candidate_numbers": other_candidate_numbers,
    # }
