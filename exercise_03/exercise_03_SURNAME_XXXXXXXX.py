# This script reads addresses collected from spam mail in a sextortion study.
# It filters used addresses that do have transactions and computes statistics of their transactions.
# The result will be stored in a defined file.
# If no address file is provided, the script will read entities and their relations from files.
# It retrieves the information about the entity neighbor network and stores them in an outfile.

import pandas as pd
import requests
from argparse import ArgumentParser
import json
import time
import networkx as nx  # you might wanna use the networkx library


def main(args):
    # an output file is required
    output_file = args.output

    # write results to output file
    results = dict()

    if (args.addresses is not None):
        addresses_file = args.addresses

        #################################
        # Implement this part:

        # read addresses json file
        # filter for used addresses that do have transactions
        # for each used address, compute some statistics

        # return a dictionary with the following keys:
        # results = {
        #     "n_used_addr": int(0), # - total number of addresses with at least one tx
        #     "addresses":
        #         {addr_used_1: {
        #             "satoshi_in" = int(0) # - total amount of satoshi received by used addresses
        #             "t_received": int(0), # - seconds between first and last received tx
        #             "in_degree": int(0), # - number of unique senders to addr_used_1
        #             "out_degree": int(0) # - number of unique receivers from addr_used_1
        #                   }, ...
        #         }
        #    }
        #################################
    else:
        if (args.entities is not None) & (args.relations is not None):
            entities_file = args.entities
            relations_file = args.relations

            #################################
            # Implement this part
            # - read entities and relations json file
            # - construct a directed graph from the relations, if needed
            # - retrieve the hops to the target entity

            # return a dictionary with the following keys:
            # results = {
            #     "entity_1": int(2), # - number of hops to target entity_1
            #     "entity_2": int(1), # - number of hops to target entity_2
            #     ...}

            #################################

    with open(output_file, 'w') as fp:
        json.dump(results, fp)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-a', '--addresses',
                        help='Output file path (JSON)', type=str,
                        required=False)
    parser.add_argument('-e', '--entities',
                        help='Input file path (JSON)', type=str,
                        required=False)
    parser.add_argument('-r', '--relations',
                        help='Input file path (JSON)', type=str,
                        required=False)
    parser.add_argument('-o', '--output',
                        help='Output file path (JSON)', type=str,
                        required=True)
    args = parser.parse_args()

    main(args)
