# This script reads tx hashes, queries the related input addresses and computes the
# clusters based on the multiple-input clustering heuristic and saves them into a JSON file

from argparse import ArgumentParser
import json
import pandas as pd
import requests

BASE_URL = f'https://blockstream.info/api/'

def get_in_addr(tx_hash):

    l_addr_in = [] # list of input addresses

    #################################

    # Implement this part

    #################################

    return l_addr_in

def main(args):

    tx_hashes_file = args.transactions  # contains tx hashes
    output_file = args.output  # will contain cluster id and cluster addresses


    with open(tx_hashes_file, 'r') as ft:
        tx_hashes = json.load(ft)

    cluster_addresses = []  # [[...],[...],...]
    # cluster_addresses is a list of clusters, where each cluster is a list of (unique) addresses
    # therefore, cluster_addresses is a list of lists of strings

    #################################
    # Implement this part


    #################################

    with open(output_file, 'w') as fp:
        json.dump(cluster_addresses, fp)



if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',
                        help='Output file path (JSON)', type=str,
                        required=True)
    parser.add_argument('-t', '--transactions',
                        help='Input file path (JSON)', type=str,
                        required=True)
    args = parser.parse_args()

    main(args)