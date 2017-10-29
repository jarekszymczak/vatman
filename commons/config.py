import os

from etl.allegro.item_etl import AllegroItemETL
from etl.allegro.user_etl import AllegroUserETL

ROOT_DIRECTORY = os.getenv('ROOT_DIRECTORY') or '/Users/Shared/vatman'
ALLEGRO_ITEMS_DIRECTORY = os.path.join(ROOT_DIRECTORY, 'items')
ALLEGRO_USERS_DIRECTORY = os.path.join(ROOT_DIRECTORY, 'users')

ALLEGRO_ITEMS_JSON = os.path.join(ROOT_DIRECTORY, 'items.json')
ALLEGRO_USERS_JSON = os.path.join(ROOT_DIRECTORY, 'users.json')

ITEMS_COLLECTION = 'items'
USERS_COLLECTION = 'users'

MONGO_DB_HOST = 'localhost'
MONDO_DB_NAME = 'vatman'

os.makedirs(ALLEGRO_ITEMS_DIRECTORY, exist_ok=True)
os.makedirs(ALLEGRO_USERS_DIRECTORY, exist_ok=True)

CATEGORIES_URL = [
    "https://allegro.pl/kategoria/telefony-komorkowe-165?ref=electronics-layer-popular&order=t",  # cellphones
    "https://allegro.pl/kategoria/laptopy-491?order=t",  # computers
    "https://allegro.pl/kategoria/tablety-89253?order=t"  # tablets
    # sorted from both sides to cover all the items
    "https://allegro.pl/kategoria/telefony-komorkowe-165?ref=electronics-layer-popular&order=n",
    "https://allegro.pl/kategoria/komputery?order=n",
    "https://allegro.pl/kategoria/tablety-89253?order=n",
    # additional categories
    "https://allegro.pl/kategoria/konsole-i-automaty?order=t&price_from=400",
    "https://allegro.pl/kategoria/komputery?order=t&price_from=500",
    "https://allegro.pl/kategoria/dyski-i-pamieci-przenosne-4475?price_from=300&order=t",
    "https://allegro.pl/kategoria/dzwiek-4395?price_from=300&order=t",
    "https://allegro.pl/kategoria/komputery-stacjonarne-486?price_from=500&order=t",
    "https://allegro.pl/kategoria/obraz-i-grafika-4312?price_from=500&order=t",
    "https://allegro.pl/kategoria/podzespoly-bazowe-4226?price_from=500&order=t",
    "https://allegro.pl/kategoria/fotografia?order=t&price_from=500",
    "https://allegro.pl/kategoria/akcesoria-gsm-348?order=t&price_from=400"
]

ETL_PROCESSOR_TO_DATA_MAPPING = (
    {
        "source": ALLEGRO_ITEMS_DIRECTORY,
        "destination_collection": ITEMS_COLLECTION,
        "etl_process_object": AllegroItemETL(),
        "identifier_field": "item_id"
    },
    {
        "source": ALLEGRO_USERS_DIRECTORY,
        "destination_collection": USERS_COLLECTION,
        "etl_process_object": AllegroUserETL(),
        "identifier_field": "user_id"
    },
)
