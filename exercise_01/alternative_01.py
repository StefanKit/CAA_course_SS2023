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
    while(repeat):
        r = requests.get(url) # get request from url
        d = json.loads(r.text) # extract txs-dict
        for di in d: # add all txs from dict
            txs.append(di)
        if(len(d)>=25):
            url = BASE_URL + "/address/"+str(a) + "/txs"+ "/chain/" + d[-1]['txid'] # extract latest index
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
    # n_txs_in: : number of txs where addr receives coins
    # n_txs_out: number of txs where addr spends coins
    # satoshi_in: amount of satoshi received by addr
    # satoshi_out: amount of satoshi spent by addr
    # balance: amount of satoshi unspent by addr
    # t_block_in_frist: unix timestamp of first block where addr received coins
    # t_block_out_last: unix timestamp of last block where addr spend coins
    # n_addr_reused: number of txs where addr has been reused
    # fees: amount of txs fees where addr spend coins


    #################################
    # Implement this part
    
    
    df = pd.json_normalize(addr_txs) # import json to pandas data frame

    vin = pd.concat(df.apply(lambda tx: pd.json_normalize(tx.loc["vin"]).assign(tx_0=tx['txid']), axis=1).tolist(),ignore_index=True)
    vout = pd.concat(df.apply(lambda tx: pd.json_normalize(tx.loc["vout"]).assign(tx_0=tx['txid']), axis=1).tolist(),ignore_index=True)
    
    n_txs_in =  len(vout[vout.loc[:,'scriptpubkey_address'] == addr].tx_0.unique()) # addr_info['chain_stats']['funded_txo_count']
    n_txs_out = len(vin[vin.loc[:,'prevout.scriptpubkey_address'] == addr].tx_0.unique()) # addr_info['chain_stats']['spent_txo_count']
    n_txs_out_alternative =  addr_info['chain_stats']['spent_txo_count']

    satoshi_in =  vout[vout.loc[:, 'scriptpubkey_address'] == addr]['value'].sum() # addr_info['chain_stats']['funded_txo_sum']

    satoshi_out =  vin[vin.loc[:, 'prevout.scriptpubkey_address'] == addr]['prevout.value'].sum() # addr_info['chain_stats']['spent_txo_sum'] 

    balance = satoshi_in - satoshi_out

    n_neighbors_out = len(vout.loc[vout.tx_0.isin(vin[vin.loc[:, 'prevout.scriptpubkey_address'] == addr].tx_0),"scriptpubkey_address"].unique())

    n_neighbors_in = len(vin.loc[vin.tx_0.isin(vout[vout.loc[:, 'scriptpubkey_address'] == addr].tx_0),"prevout.scriptpubkey_address"].unique())

    activity_period = max(df['status.block_time']) - min(df['status.block_time'])

    fees_spend = df.loc[df.txid.isin(vin[vin.loc[:, 'prevout.scriptpubkey_address'] == addr].tx_0),"fee"].sum()

    t_block_in = df.loc[df.txid.isin(vout[vout.loc[:, 'scriptpubkey_address'] == addr].tx_0), "status.block_time"].min()

    t_block_out = df.loc[df.txid.isin(vin[vin.loc[:, 'prevout.scriptpubkey_address'] == addr].tx_0), "status.block_time"].max()

    n_addr_reused = len(set(vout[vout.loc[:, 'scriptpubkey_address'] == addr].tx_0).intersection(
                        set(vin[vin.loc[:, 'prevout.scriptpubkey_address'] == addr])))


    results = dict()

    results['n_txs_in'] = int(n_txs_in)
    results['n_txs_out'] = int(n_txs_out_alternative)
    results['satoshi_in'] = int(satoshi_in)
    results['satoshi_out'] = int(satoshi_out)
    results['balance'] = int(balance)
    results['t_block_in_frist'] = int(t_block_in)
    results['t_block_out_last'] = int(t_block_out)
    results['n_addr_reused'] = int(n_addr_reused)
    results['fees'] = int(fees_spend)


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
