import json
import os
import pprint
import multiprocessing as mp
import click
import pathlib

import etl.test.allegro.resources
from commons.config import ALLEGRO_ITEMS_DIRECTORY, ALLEGRO_ITEMS_JSON
from etl.allegro.item_selling import extract_data_from_item


@click.command()
@click.option('--processes', default=4, help='number of processes')
def run(processes):
    process_pool = mp.Pool(processes)
    paths = []
    for filepath in pathlib.Path(ALLEGRO_ITEMS_DIRECTORY).glob('**/*'):
        paths.append(filepath.absolute())

    jsons = process_pool.map(extract_data_from_item, paths)
    with open(ALLEGRO_ITEMS_JSON, 'w') as f:
        json.dump(jsons, f)

if __name__ == '__main__':
    run()
