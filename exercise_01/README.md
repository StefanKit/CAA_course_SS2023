# Exercise 1

## Prerequisites

Make sure you have Python 3 and [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) installed.
Please use the python and package version defined in the `env.yml`-file, 
the program will be tested in this environment and the specified versions.

Install dependencies

	conda install conda=23.1.0
	conda env create -f env.yml

Activate the environment

	conda activate caa_venv

## Exercise: Address Statistics

In this exercise, you will learn how to compute basic summary statistics for an
address in the UTXO model (e.g., Bitcoin).

Your task is to complete the code in `exercise_01.py` so that you can compute,
for a given address `addr`, the following values:

- `satoshi_in`: amount of satoshi received by `addr` [int] (0.4 points)
- `satoshi_out`: amount of satoshi spent by `addr` [int] (0.4 points)
- `balance`: amount of satoshi unspent by `addr`  [int] (0.2 points)
- `fees`: amount of txs fees where `addr` spend coins [int] (1 point)
- `b_in_first`: block height of the first block where `addr` received coins [int] (0.5 points)
- `b_out_first`: block height of the first block where `addr` spend coins [int] (0.5 points)
- `n_neighbours_in`: number of unique addresses that received coins from `addr` (include `addr`, if present) [int] (1 point)
- `n_neighbours_out`: number of unique addresses that send coins to `addr` (include `addr`, if present) [int] (1 point)

Write them as integers into a specified JSON file.

## Run the script

You need to specify as arguments a BTC address (`-a`) and an JSON output path 
(`-o`) when running the script. 

    python3 exercise_01.py -a <YOUR_ADDRESS> -o <YOUR_PATH>

Example:

    python3 exercise_01.py -a "17SkEw2md5avVNyYgj6RiXuQKNwkXaxFyQ" -o "./output.json"

The script should work for any Bitcoin address, but we will test it with one of
the following addresses [stories behind](https://medium.com/blockchain/famous-bitcoin-transactions-the-stories-behind-them-b45f36acfeb):


	17SkEw2md5avVNyYgj6RiXuQKNwkXaxFyQ
	12sENwECeRSmTeDwyLNqwh47JistZqFmW8


The script is helping you in the process with comments and you can find more
details about the [Blockstream API](https://github.com/Blockstream/esplora/blob/master/API.md)
