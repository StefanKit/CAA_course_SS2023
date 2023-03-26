import graphsense
from graphsense.api import addresses_api, blocks_api, entities_api, general_api, bulk_api, txs_api
import yaml
import requests
from argparse import ArgumentParser
import json
import pandas as pd
import time

BASE_URL = 'https://blockstream.info/api/'

from pprint import pprint

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

configuration = graphsense.Configuration(
    host = "https://api.graphsense.info",
    api_key = {'api_key': config['keys']['graphsense_apikey']})

def get_txs_from_entity(entity):
    with graphsense.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = entities_api.EntitiesApi(api_client)
        try:
            # Get an address, optionally with tags
            list_entity_txs = api_instance.list_entity_txs("BTC",entity).to_dict()['address_txs']
            return [txs['tx_hash'] for txs in list_entity_txs]
        except graphsense.ApiException as e:
            print("Exception when calling AddressesApi->get_address: %s\n" % e)

def get_addrs_from_entity(entity):
    with graphsense.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = entities_api.EntitiesApi(api_client)
        try:
            # Get an address, optionally with tags
            list_entity_addresses = api_instance.list_entity_addresses("BTC",entity).to_dict()['addresses']
            return [addr['address'] for addr in list_entity_addresses]
        except graphsense.ApiException as e:
            print("Exception when calling AddressesApi->get_address: %s\n" % e)

def get_in_addrs_from_tx(tx_hash):
    url = BASE_URL + f'/tx/{str(tx_hash)}'
    r = requests.get(url)
    d = json.loads(r.text)
    return [vin['prevout']['scriptpubkey_address'] for vin in d['vin']]

def get_in_txs_from_entity(entity):
    d = dict()

    txs = get_txs_from_entity(entity)
    a = get_addrs_from_entity(entity)
    txs_in = [get_in_addrs_from_tx(tx) for tx in txs]

    for i,b in enumerate([(len(set(a).intersection(set(tx_i))) > 0 ) for tx_i in txs_in]):
        if(b):
            d.update({txs[i]: list(set(txs_in[i]))})
    return (d)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    d = dict()

    entities = [20805223, 8361735, 693379588, 131036, 520608]

    for e in entities:
        d.update(get_in_txs_from_entity(e))

    with open("./input_txs.json", 'w') as fp:
        json.dump(d, fp)
