import multiprocessing as mp
import pathlib

import click
from pymongo import MongoClient

from commons.config import MONGO_DB_HOST, ETL_PROCESSOR_TO_DATA_MAPPING, MONDO_DB_NAME


@click.command()
@click.option('--processes', default=4, help='number of processes')
def run(processes):
    mongo_client = MongoClient(MONGO_DB_HOST)

    for etl_process in ETL_PROCESSOR_TO_DATA_MAPPING:
        paths = []
        for filepath in pathlib.Path(etl_process['source']).glob('**/*'):
            paths.append(filepath.absolute())

        process_pool = mp.Pool(processes)
        etl_process_object = etl_process['etl_process_object']
        jsons = process_pool.map(etl_process_object.extract_data, paths)
        destination_collection = etl_process['destination_collection']
        identifier_field = etl_process['identifier_field']
        mongo_db = mongo_client[MONDO_DB_NAME]
        for json_ in jsons:
            mongo_db[destination_collection].replace_one({identifier_field: json_[identifier_field]}, json_,
                                                         upsert=True)


if __name__ == '__main__':
    run()
