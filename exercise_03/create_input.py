import graphsense
from graphsense.api import addresses_api, blocks_api, entities_api, general_api, bulk_api, txs_api
import pandas as pd
import yaml
import json

from pprint import pprint

# read config files for keys
with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# read spam addresses
# https://arxiv.org/pdf/1908.01051.pdf
# https://github.com/MatteoRomiti/Sextortion_Spam_Bitcoin
# https://zenodo.org/record/3515199#.Yjdikjwo9H5
# https://github.com/cryptoassetanalyticsnet/CAA-TheWebConf2022/blob/master/data/sextortion_addresses.json
spam_addrs = pd.read_csv("./addresses.csv", header=None)[0]
# create sample
input_addresses = spam_addrs.sample(200).to_list()

# GraphSense API configs
currency = 'btc'
configuration = graphsense.Configuration(
    host = "https://api.graphsense.info",
    api_key = {'api_key': config['keys']['graphsense_apikey']})


with graphsense.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bulk_api.BulkApi(api_client)
    currency = "btc" # str | The cryptocurrency (e.g., btc)

    # example passing only required values which don't have defaults set
    try:
        # Get data as JSON in bulk
        addrs_response = api_instance.bulk_json(currency, operation='get_address',
                                              body={'address':input_addresses},
                                              num_pages=1)
        #print(addrs_response)
    except graphsense.ApiException as e:
        print("Exception when calling BulkApi->bulk_json: %s\n" % e)

with open("spam_addresses.json", 'w') as fp:
    json.dump(input_addresses, fp)

df_addr = pd.json_normalize(addrs_response)
# filter addresses that have been used
df_addr = df_addr.loc[~df_addr.address.isna()]

# get entity
with graphsense.ApiClient(configuration) as api_client:
    api_instance = bulk_api.BulkApi(api_client)
    # Retrieve all entities in bulk
    entities_response = api_instance.bulk_json("btc",
                                           operation='get_address_entity',
                                           num_pages=1,
                                           body={'address': df_addr.address.to_list()})

df_entities = pd.json_normalize(entities_response)


def get_neighbors(entity_list):
    nbrs_list = list()

    for e in set(entity_list):
        try:
            with graphsense.ApiClient(configuration) as api_client:
                api_instance = entities_api.EntitiesApi(api_client)
                #nbrs_list.append(pd.json_normalize(
                #    api_instance.list_entity_neighbors("btc", e, direction='out', include_labels=True).to_dict()[
                #        'neighbors']).assign(entity=e, direction = "out"))
                nbrs_list.append(pd.json_normalize(
                    api_instance.list_entity_neighbors("btc", e, direction='in', include_labels=True).to_dict()[
                        'neighbors']).assign(entity=e, direction = "in"))
        except graphsense.ApiException as e:
            print("Exception when calling EntitiesApi->list_entity_neighbors: %s", e)
    df_nbrs = pd.concat(nbrs_list, ignore_index = True)
    return df_nbrs

df_neighbors = get_neighbors(df_entities.entity.astype(int)).\
    loc[:,["entity.entity","entity.best_address_tag.category","entity","direction","entity.out_degree","entity.in_degree"]].\
    rename(columns={"entity.best_address_tag.category":"category","entity.out_degree":"out_degree","entity.in_degree":"in_degree"})
df_neighbor_entities = df_neighbors.loc[:,["entity.entity","category","out_degree","in_degree"]].rename(columns={"entity.entity":"entity"})
df_neighbors_in = df_neighbors.loc[df_neighbors.direction == "in"].\
    rename(columns={"entity":"to_entity","entity.entity":"from_entity"}).drop(columns=["direction","category"])
df_neighbors_out = df_neighbors.loc[df_neighbors.direction == "out"].\
    rename(columns={"entity":"from_entity","entity.entity":"to_entity"}).drop(columns=["direction","category"])


df_neighbors_2 = get_neighbors(
    pd.concat([df_neighbor_entities.loc[(df_neighbor_entities["in_degree"]<10) |
                                        (df_neighbor_entities["out_degree"]<10)].entity.astype(int)], ignore_index = True).tolist()).\
    loc[:,["entity.entity","entity.best_address_tag.category","entity","direction","entity.out_degree","entity.in_degree"]].\
        rename(columns={"entity.best_address_tag.category":"category","entity.out_degree":"out_degree","entity.in_degree":"in_degree"})
df_neighbor_entities_2 = df_neighbors_2.loc[:,["entity.entity","category","in_degree","out_degree"]].rename(columns={"entity.entity":"entity"})
df_neighbors_in_2 = df_neighbors_2.loc[df_neighbors_2.direction == "in"].\
    rename(columns={"entity":"to_entity","entity.entity":"from_entity"}).drop(columns=["direction","category"])
df_neighbors_out_2 = df_neighbors_2.loc[df_neighbors_2.direction == "out"].\
    rename(columns={"entity":"from_entity","entity.entity":"to_entity"}).drop(columns=["direction","category"])

df_neighbors_3 = get_neighbors(
    pd.concat([ df_neighbor_entities_2.loc[(df_neighbor_entities_2["in_degree"]<10) |
                                             (df_neighbor_entities_2["out_degree"]<10)].entity.astype(int)], ignore_index = True).tolist()).\
    loc[:,["entity.entity","entity.best_address_tag.category","entity","direction","entity.out_degree","entity.in_degree"]].\
        rename(columns={"entity.best_address_tag.category":"category","entity.out_degree":"out_degree","entity.in_degree":"in_degree"})
df_neighbor_entities_3 = df_neighbors_3.loc[:,["entity.entity","category","in_degree","out_degree"]].rename(columns={"entity.entity":"entity"})
df_neighbors_in_3 = df_neighbors_3.loc[df_neighbors_3.direction == "in"].\
    rename(columns={"entity":"to_entity","entity.entity":"from_entity"}).drop(columns=["direction","category"])
df_neighbors_out_3 = df_neighbors_3.loc[df_neighbors_3.direction == "out"].\
    rename(columns={"entity":"from_entity","entity.entity":"to_entity"}).drop(columns=["direction","category"])


df_neighbor_entities_all = pd.concat([df_entities,
    df_neighbor_entities,df_neighbor_entities_2,df_neighbor_entities_3]).copy()
df_neighbor_entities_all.loc[:,"entity"] = df_neighbor_entities_all.entity.astype(int)
df_neighbor_entities_all.\
    loc[:,["entity","category"]].\
    drop_duplicates().to_json("./entities.json", orient="records")

df_neighbor_relations_all = pd.concat([
    df_neighbors_in,df_neighbors_in_2,df_neighbors_in_3], ignore_index=True).copy()
df_neighbor_relations_all.loc[:,"from_entity"] = df_neighbor_relations_all.from_entity.astype(int)
df_neighbor_relations_all.loc[:,"to_entity"] = df_neighbor_relations_all.to_entity.astype(int)
df_neighbor_relations_all.\
    loc[:,["from_entity","to_entity"]].\
    drop_duplicates().to_json("./entity_relations.json", orient="records")
