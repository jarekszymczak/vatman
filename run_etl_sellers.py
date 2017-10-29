import json
import multiprocessing as mp
import pathlib

import click

from commons.config import ALLEGRO_USERS_DIRECTORY, ALLEGRO_USERS_JSON
from etl.allegro.about_seller import extract_data_from_seller


@click.command()
@click.option('--processes', default=4, help='number of processes')
def run(processes):
    process_pool = mp.Pool(processes)
    paths = []
    for filepath in pathlib.Path(ALLEGRO_USERS_DIRECTORY).glob('**/*'):
        paths.append(filepath.absolute())

    jsons = process_pool.map(extract_data_from_seller, paths)
    # jsons = [jextract_data_from_seller(path) for path in paths]
    with open(ALLEGRO_USERS_JSON, 'w') as f:
        json.dump(jsons, f)


if __name__ == '__main__':
    run()
