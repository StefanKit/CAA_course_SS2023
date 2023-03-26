# Exercise 3

# Sextortion Case Study

For this exercise, we will use Bitcoin addresses that were collected as part of a 
[Sextortion Spam](https://arxiv.org/abs/1908.01051) study.
We will analyze some basic aspects of this activity to gain some insight into the attacks
and practice the usage of the entity abstraction of Bitcoin transactions.

## Address statistics

The input data `spam_addresses.json` consists of a set of Bitcoin addresses,
that have been collected as part of the campaign.
You should filter those addresses that have been used in transactions, 
e.g. using a blockchain explorer API (make sure not run into request exceeds).

- How many addresses have been used in total? (0.5 points)

For those who have received transactions, 
you should query their transactions and compute the following statistics:

- How much has each address received in total? (0.5 points)
- How long has each address received coins? (0.5 point)
  Difference between the last and the first transaction received in seconds.
- What is the in- and out-degree to unique neighbor addresses? (1 points)
Be careful, the definitions might vary in comparison with the neighbors nodes.
The in-degree is the number of unique addresses that have sent coins to the address.
The out-degree is the number of unique addresses that have received coins from the address.

# Entity neighbors analysis

In addition, the input file `entities.json` contains a set of entities,
extracted from an entity abstraction of the Bitcoin's sextortion campaign network.
Each entity is either a receiving campaign address or a neighbor entity sending money.
The input file `entity_relation.json` contain directed relations between entities.
All entities' relations represend monetary flow to campaign addresses in one or multiple hops
and are therefore (direct or indirect) neighbors of the receiving campaign address.
The entities are identified by integer id numbers, which have no meaning in the real world.

The task is to find out which entities are associated with a known category and 
retrieve the number of hops they are away from the champion address.

- Which are known neighbor entities that have sent coins to a sextortion entity? (2.5 points) 

List all categorised entities that have sent coins to a sextortion entity and 
the (minimal) number of hops they are away from the champion address.
The output should be a dictionary with the entity id as key and the number of hops as value.

Write all results into a specified JSON output file (`-o`).

For running the script, you also need to specify either the JSON input paths for addresses (`-a`) or 
the entities (`-e`) together with their relations (`-r`). 

Example:

    python ./exercise_03_SURNAME_XXXXXXXX.py -a "./addrs_response.json" -o "output.json"

    python ./exercise_03_SURNAME_XXXXXXXX.py -e "./entities.json" -r "./entity_relation.json" -o "output.json"

The script should also work and might be tested with another input of the sextortion data set.