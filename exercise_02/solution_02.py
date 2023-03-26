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
    url = BASE_URL + 'tx/' + str(tx_hash)
    r = requests.get(url)  # get request from url
    d = json.loads(r.text)  # extract txs-dict

    l_addr_in = pd.json_normalize(d["vin"]).loc[:,"prevout.scriptpubkey_address"].to_list()  # extract input addresses

    #################################

    return l_addr_in

def main(args):

    tx_hashes_file = args.transactions  # contains tx hashes
    output_file = args.output  # will contain cluster id and cluster addresses


    with open(tx_hashes_file, 'r') as ft:
        tx_hashes = json.load(ft)



    #################################
    # Implement this part

    cluster_addresses = [] # [[...],[...],...]
    # cluster_addresses is a list of clusters, where each cluster is a list of (unique) addresses
    # therefore, cluster_addresses is a list of lists of strings

    # create empty dataframe
    df_cluster = pd.DataFrame(data = [], columns=["cluster", "address"])


    # iterate txs
    while(len(tx_hashes) > 0):
        tx = tx_hashes.pop()  # pop first tx
        l_addr_in = get_in_addr(tx)  # get input addresses

        addr_intersect = df_cluster.loc[df_cluster.address.isin(pd.Series(l_addr_in))] # find intersections
        # if intersection exists
        if (len(addr_intersect) > 0):
            # print("Intersection found")
            cluster_num = addr_intersect.cluster.min() # evaluate minimum (smallest) cluster number
            # if the intersections affects multiple clusters, merge them by assign an equal cluster number
            ## (gaps in the cluster range could appear, but that's not an issue since the numbers are only temporal)
            df_cluster.loc[df_cluster.cluster.isin(addr_intersect.cluster), "cluster"] = cluster_num
        else:
            if( len(df_cluster.cluster) > 0 ):
                cluster_num = df_cluster.cluster.max() + 1
            else:
                cluster_num = 0
        df_cluster = pd.concat([df_cluster, pd.DataFrame({
            'cluster': cluster_num,
            'address': l_addr_in
        })], ignore_index=True).drop_duplicates()

        # print(df_cluster.cluster.value_counts().to_list())

    cluster_addresses = df_cluster.groupby("cluster").address.apply(lambda s: pd.Series(s).to_list()).to_list()

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