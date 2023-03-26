# This script reads addresses collected from spam mails in a sextortion study.
# It filters used addresses and computes statistics of their transactions that will be stored in an outfile.
# If no addresses are provided, the script will read entities and their relations from a files.
# It retrieves the information about the entity neighbor network and stores them in an outfile.

import pandas as pd
import requests
from argparse import ArgumentParser
import json
import time
import networkx as nx # you might wanna use the networkx library


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
        # filter for used addresses
        # for each used address, compute statistics

        df_addresses = pd.read_json(addresses_file)[0]

        BASE_URL = 'https://blockstream.info/api/'

        def get_address_info(a):
            # return info about address a
            url = BASE_URL + 'address/' + str(a)
            r = requests.get(url)
            d = json.loads(r.text)
            return d

        def get_address_txs(a):
            txs = []
            # return all txs of address a
            # if a has more than 25 txs, we need to fetch all of them

            #################################

            # Implement this part
            repeat = True
            url = BASE_URL + f'/address/{str(a)}/txs'
            while (repeat):
                r = requests.get(url)  # get request from url
                d = json.loads(r.text)  # extract txs-dict
                for di in d:  # add all txs from dict
                    txs.append(di)
                if (len(d) >= 25):
                    url = BASE_URL + "/address/" + str(a) + "/txs" + "/chain/" + d[-1]['txid']  # extract latest index
                    time.sleep(0.2)  # avoid to many requests per time
                else:
                    repeat = False
            #################################

            return txs

        df_addresses = df_addresses.loc[df_addresses.apply(lambda a: get_address_info(a)['chain_stats']['tx_count'] > 0)]

        results['n_used_addr'] = len(df_addresses)

        for i,a in df_addresses.items():
            txs = get_address_txs(a)
            df = pd.json_normalize(txs)
            vout = pd.concat(
                df.apply(lambda tx: pd.json_normalize(tx.loc["vout"]).assign(tx_0=tx['txid']), axis=1).tolist(),
                ignore_index=True)
            vin = pd.concat(
                df.apply(lambda tx: pd.json_normalize(tx.loc["vin"]).assign(tx_0=tx['txid']), axis=1).tolist(),
                ignore_index=True)
            t_received = df.loc[df.txid.isin(vout.loc[vout["scriptpubkey_address"] == a, "tx_0"]),
                            "status.block_time"].max() - \
                         df.loc[df.txid.isin(vout.loc[vout["scriptpubkey_address"] == a, "tx_0"]),
                            "status.block_time"].min()
            satoshi_in = vout[vout.loc[:, 'scriptpubkey_address'] == a]['value'].sum()
            in_degree = len(vin.loc[vin.tx_0.isin(
                vout.loc[vout["scriptpubkey_address"] == a, "tx_0"]), "prevout.scriptpubkey_address"].unique())
            out_degree = len(vout.loc[vout.tx_0.isin(
                vin.loc[vin["prevout.scriptpubkey_address"] == a, "tx_0"]), "scriptpubkey_address"].unique())

            print(a,satoshi_in,out_degree,in_degree)
            results[a] = {"satoshis_in": int(satoshi_in), "t_received": int(t_received), "in_degree": int(in_degree),
                            "out_degree": int(out_degree)}

        # return a dictionary with the following keys:
        # result = {
        #     "n_used_addr": int(0), # - total amount of satoshi received by used addresses
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

            # return a dictionary in the following style:
            # result = {
            #     entity_1: int(2), # - number of hops to target entity_1
            #     entity_2: int(1), # - number of hops to target entity_2
            #     ...}

            df_relations = pd.read_json(relations_file)
            df_entities = pd.read_json(entities_file)

            g = nx.from_pandas_edgelist(df_relations, source='from_entity', target='to_entity', create_using=nx.DiGraph())

            d_attr = df_entities.loc[~df_entities.category.isna()].set_index("entity").to_dict()["category"]
            nx.set_node_attributes(g, d_attr, "category")

            df_out = pd.DataFrame.from_dict(g.out_degree)
            df_target = df_out.loc[df_out.values == 0,0]

            l_hop = []
            df_hop = df_target.to_frame("from_entity").assign(hop = 0)
            df_hop.loc[:,"target_entity"] = df_hop.loc[:,"from_entity"].astype(int)
            l_hop.append(df_hop)
            for i in range(1,10):
                if(sum(df_relations.to_entity.isin(df_hop.from_entity))>0):
                    df_next = pd.merge(df_relations,
                                       df_hop.loc[:,["from_entity","target_entity"]].rename(columns = {"from_entity":"to_entity"}),
                                      on = "to_entity", how = "inner")
                    df_hop = df_next.merge(df_entities.rename(columns = {"entity":"from_entity"}),
                                           on = "from_entity", how = "left").assign(hop = i)
                    l_hop.append(df_hop)
                else:
                    break
            df_hop_all = pd.concat(l_hop)

            results = df_hop_all.loc[~df_hop_all.category.isna()].groupby("from_entity").hop.min().to_dict()
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