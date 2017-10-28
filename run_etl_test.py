import os
import pprint

import etl.test.allegro.resources
from etl.allegro.item_selling import extract_data_from_item

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    item_extractor = extract_data_from_item
    ad_price_sold_available = os.path.join(os.path.dirname(etl.test.allegro.resources.__file__),
                                           'ad_price_sold_available.html')

    ad_price_sold_available_json = extract_data_from_item(ad_price_sold_available)
    pp.pprint(ad_price_sold_available_json)
