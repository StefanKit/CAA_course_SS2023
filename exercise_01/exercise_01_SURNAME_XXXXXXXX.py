# This script fetches data from the Blockstream API, computes summary
# statistics about a specific BTC address and saves the data into a JSON file

# Please, see Blockstream documentation here:
# https://github.com/Blockstream/esplora/blob/master/API.md
import requests
from argparse import ArgumentParser
import json
import pandas as pd

BASE_URL = 'https://blockstream.info/api/'


def get_address_info(address):
    # return info about address a
    url = BASE_URL + 'address/' + str(address)
    r = requests.get(url)
    d = json.loads(r.text)
    return d


def get_address_txs(address):
    txs = []
    # return list txs of all transactions for address
    # if a has more than 25 txs, we need to fetch all of them


    #################################

    # Implement this part

    #################################

    return txs


def main(args):

    addr = args.address
    output_file = args.output

    # Fetch address info and txs
    addr_info = get_address_info(addr)
    addr_txs = get_address_txs(addr)

    # Given the address addr, compute the following values:

    # satoshi_in: amount of satoshi received by addr [int] (0.4 points)
    # satoshi_out: amount of satoshi spent by addr [int] (0.4 points)
    # balance: amount of satoshi unspent by addr [int] (0.2 points)
    # fees: amount of txs fees where addr spend coins [int] (1 point)
    # b_in_first: block height of the first block where addr received coins [int] (0.5 points)
    # b_out_first: block height of the first block where addr spend coins [int] (0.5 points)
    # n_neighbours_in: number of unique addresses that received coins from addr (include addr, if present) [int] (1 point)
    # n_neighbours_out: number of unique addresses that send coins to addr (include addr, if present) [int] (1 point)


    #################################
    # Implement this part
    
    
    results = dict()

    # numeric results should be integer values

    # results['satoshi_in']
    # results['satoshi_out']
    # results['balance']
    # results['fees']
    # results['b_in_first']
    # results['b_out_first']
    # results['n_neighbours_in']
    # results['n_neighbours_out']

    #################################

    with open(output_file, 'w') as fp:
        json.dump(results, fp)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-a', '--address',
                        help='BTC address for computing statistics statistics',
                        type=str, required=True)
    parser.add_argument('-o', '--output',
                        help='Output file path (JSON)', type=str,
                        required=True)
    args = parser.parse_args()

    main(args)
