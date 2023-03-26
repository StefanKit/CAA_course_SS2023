# Exercise 2

## Prerequisites

Make sure you have Python 3 and [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) installed.
Please use the python and package version defined in the `env.yml`-file, 
the program will be tested in this environment and the specified versions.

Install dependencies

	conda install conda=23.1.0
	conda env create -f env.yml

Activate the environment

	conda activate caa_venv

## Address Clustering

In this exercise, you will learn how to cluster addresses based on the 
Co-Spent (Multiple-Input) Heuristics [1]. The principle has been also been expressed in the homework paper [2] 
and in the course notes (1-Analyzing-UTXO-Ledgers.pdf).

Your task is to complete the code in `exercise_02_SURNAME_XXXXXXXX.py` so that you can compute,
for a given set of transactions, the corresponding clusters and write into a specified JSON file.

First, you need to query the input addresses for each transaction.
The input addresses are corresponding addresses of transactions that have been co-spent.
Then you need to cluster the addresses, there are at least two ways to perform the clustering task: 
using the union-find data structure or building a graph and finding connected components 
(each tx (a node) is connected to all its input addresses (also nodes) 
through undirected edges). Both options lead to the same result.

When running the script, you need to specify as arguments the path of the transactions' input
file (`-t`) and the path of the output file (`-o`) when running the script.

    python exercise_02.py -t <YOUR_TX_INPUT_PATH> -o <YOUR_OUTPUT_PATH>

Example:

    python ./exercise_02_SURNAME_XXXXXXXX.py -t "./input_txs.json" -o "./out

The input file is a list of tx hashes with the corresponding input addresses, e.g., 

    ["tx_hash_1", "tx_hash_2", "tx_hash_3", ...]

Given the example above, your output file should look like this:

    [
        ["address_1", "address_2", "address_3"],
        ["address_4", "address_5"]
    ]

which is a list of clusters and each cluster is a list of (unique) addresses.

## Evaluation

The script should work for any transaction input file,
but we will test it with an extended version of `input_txs.json`, 
including a complete set of all transactions from the corresponding entities, 
defined by the co-spend heuristic.

Note that there won't be p2pk addresses in the evaluation set,
so you can use the `scriptpubkey_address` field of the query result.


## References

[1] Sarah Meiklejohn, Marjori Pomarole, Grant Jordan, Kirill Levchenko,
Damon McCoy, Geoffrey M Voelker, and Stefan Savage. “A fistful of
bitcoins: characterizing payments among men with no names”. In: Internet
Measurement Conference. ACM. 2013, pp. 127–140.

[2] Möser, Malte, and Arvind Narayanan. "Resurrecting address clustering in bitcoin." 
Financial Cryptography and Data Security: 26th International Conference, 
FC 2022, Grenada, May 2–6, 2022, Revised Selected Papers. 
Cham: Springer International Publishing, 2022.

