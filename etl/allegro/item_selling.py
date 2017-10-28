from bs4 import BeautifulSoup

from commons.utils import cleanup_contact_data_field, remove_non_numeric_data_from_line

is_new_selector = '#showitem-main > section.attributes-block > div > ul:nth-of-type(1) > li:nth-of-type(1) > span.attribute-value'
is_invoice_selector = "#showitem-main > section.attributes-block > div > ul:nth-of-type(1) > li:nth-of-type(2) > span.attribute-value"
buy_now_price_selector = "#purchase-form > div.col-sm-7.col-xs-12 > div:nth-child(1) > div.price"
item_price_and_quantity_field = "#purchase-form > div.col-sm-7.col-xs-12"
how_many_people_bough_how_many_items_field = "#preinfo-container > div > div.col-xs-12.col-sm-4.col-md-4.buyers-count > span"
seller_name_field = "#seller-details > div.btn.btn-default.btn-user > a > span"
item_name = "#showitem-main > section:nth-child(6) > div > h1" # substract element in small which is id
