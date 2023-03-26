# This script reads txs data from a specified input JSON file and computes the
# clusters based on the multiple-input clustering heuristic and saves them into
# a JSON file

from argparse import ArgumentParser
import json
import pandas as pd

def main(args):

    input_file = args.input  # contains tx hashes and input addresses
    output_file = args.output  # will contain cluster id and cluster addresses

    with open(input_file, 'r') as fp:
        tx_addresses_dict = json.load(fp)

    #################################
    # Implement this part

    cluster_addresses = []

    # **** Remember ****
    # cluster_addresses is a list of clusters and each cluster is a list of
    # (unique) addresses
    df_cluster = ((pd.DataFrame(cluster_addresses). \
                   reset_index().rename(columns={'index': 'cluster'}))). \
        melt(id_vars="cluster", value_name="address").drop(columns=["variable"])
    df_cluster = df_cluster.loc[~df_cluster.address.isnull()]

    for tx in tx_addresses_dict.values():
        addr_intersect = df_cluster.loc[df_cluster.address.isin(pd.Series(tx))]
        df_cluster.loc[df_cluster.cluster.isin(addr_intersect.cluster), "cluster"] = addr_intersect.cluster.min()
        if (len(addr_intersect) > 0):
            cluster_num = int(pd.Series([addr_intersect.cluster.min(), 0]).max(skipna=True))
        else:
            cluster_num = int(pd.Series([df_cluster.cluster.max() + 1, 0]).max(skipna=True))
        df_cluster = pd.concat([df_cluster, pd.DataFrame({
            'cluster': cluster_num,
            'address': tx
        })], ignore_index=True).drop_duplicates()

    cluster_addresses = df_cluster.groupby("cluster").address.apply(lambda s: pd.Series(s).to_list()).to_list()

    #################################

    with open(output_file, 'w') as fp:
        json.dump(cluster_addresses, fp)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',
                        help='Output file path (JSON)', type=str,
                        required=True)
    parser.add_argument('-i', '--input',
                        help='Input file path (JSON)', type=str,
                        required=True)
    args = parser.parse_args()

    main(args)
