# This script fetches data from the Blockstream API, computes summary
# statistics about a specific BTC address and saves the data into a JSON file

# Please, see Blockstream documentation here:
# https://github.com/Blockstream/esplora/blob/master/API.md
import requests
from argparse import ArgumentParser
import json
import pandas as pd
import time

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
    repeat = True
    url = BASE_URL + f'/address/{str(address)}/txs'
    while(repeat):
        r = requests.get(url) # get request from url
        d = json.loads(r.text) # extract txs-dict
        for di in d: # add all txs from dict
            txs.append(di)
        if(len(d)>=25):
            url = BASE_URL + "/address/"+str(address) + "/txs"+ "/chain/" + d[-1]['txid'] # extract latest index
            time.sleep(0.2) # avoid to many requests per time
        else:
            repeat = False
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
    # b_in_first: block height of first block where addr received coins [int] (0.5 points)
    # b_out_first: block height of first block where addr spend coins [int] (0.5 points)
    # n_neighbours_in: number of unique addresses that received coins from addr (include addr, if present) [int] (1 point)
    # n_neighbours_out: number of unique addresses that send coins to addr (include addr, if present) [int] (1 point)


    #################################
    # Implement this part
    
    
    df = pd.json_normalize(addr_txs) # import json to pandas data frame

    # incoming transactions
    vin = pd.concat(df.apply(lambda tx: pd.json_normalize(tx.loc["vin"]).assign(tx_0=tx['txid']), axis=1).tolist(),ignore_index=True)
    # transaction outs
    vout = pd.concat(df.apply(lambda tx: pd.json_normalize(tx.loc["vout"]).assign(tx_0=tx['txid']), axis=1).tolist(),ignore_index=True)
    
    n_txs_in =  len(vout[vout.loc[:,'scriptpubkey_address'] == addr].tx_0.unique()) # addr_info['chain_stats']['funded_txo_count']
    n_txs_out = len(vin[vin.loc[:,'prevout.scriptpubkey_address'] == addr].tx_0.unique()) # addr_info['chain_stats']['spent_txo_count']
    n_txs_out_alternative =  addr_info['chain_stats']['spent_txo_count']

    n_neighbors_in = len(vin.loc[vin.tx_0.isin(vout.loc[vout["scriptpubkey_address"] == addr,"tx_0"]),"prevout.scriptpubkey_address"].unique())
    n_neighbors_out = len(vout.loc[vout.tx_0.isin(vin.loc[vin["prevout.scriptpubkey_address"] == addr,"tx_0"]),"scriptpubkey_address"].unique())

    satoshi_in =  vout[vout.loc[:, 'scriptpubkey_address'] == addr]['value'].sum() # addr_info['chain_stats']['funded_txo_sum']
    satoshi_out =  vin[vin.loc[:, 'prevout.scriptpubkey_address'] == addr]['prevout.value'].sum() # addr_info['chain_stats']['spent_txo_sum'] 

    balance = satoshi_in - satoshi_out

    activity_period = max(df['status.block_time']) - min(df['status.block_time'])

    fees_spend = df.loc[df.txid.isin(vin[vin.loc[:, 'prevout.scriptpubkey_address'] == addr].tx_0),"fee"].sum()

    try:
        b_in_first = df.loc[df.txid.isin(vout[vout.loc[:, 'scriptpubkey_address'] == addr].tx_0), "status.block_height"].min()
    except:
        b_in_first = 0

    try:
        b_out_first = df.loc[df.txid.isin(vin[vin.loc[:, 'prevout.scriptpubkey_address'] == addr].tx_0), "status.block_height"].min()
    except:
        b_out_first = 0

    try:
        b_out_last = df.loc[df.txid.isin(vin[vin.loc[:, 'prevout.scriptpubkey_address'] == addr].tx_0), "status.block_height"].max()
    except:
        b_out_last = 0

    n_addr_reused = len(set(vout[vout.loc[:, 'scriptpubkey_address'] == addr].tx_0).intersection(
                        set(vin[vin.loc[:, 'prevout.scriptpubkey_address'] == addr])))


    results = dict()

    results['satoshi_in'] = int(satoshi_in)
    results['satoshi_out'] = int(satoshi_out)
    results['balance'] = int(balance)
    results['fees'] = int(fees_spend)
    results['b_in_first'] = int(b_in_first)
    results['b_out_first'] = int(b_out_first)
    results['n_neighbours_in'] = int(n_neighbors_in)
    results['n_neighbours_out'] = int(n_neighbors_out)


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
