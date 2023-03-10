from argparse import ArgumentParser

import pandas as pd
import glob
import os

def main(args):

    solution_json = args.solution
    alternative_json = args.alternative
    result_dir = args.results
    output_file = args.output

	# introduce weights (points)
    weights = pd.Series(data = {'n_txs_in':0.4, 'n_txs_out':0.4, 'satoshi_in':0.4, 'satoshi_out':0.4, 'balance':0.2,
       't_block_in_first':0.8, 't_block_out_last':0.8, 'n_addr_reused':0.8, 'fees':0.8})

	# read result, rename misspelling columns
    df_solution = pd.read_json(solution_json, orient = 'index', typ = "series").to_frame().T \
        .rename(columns={'t_block_in_frist': 't_block_in_first'}) \
        .rename(columns={'t_block_last_out': 't_block_out_last'})

    # read alternative solution
    if(alternative_json is None):
        df_alternative = df_solution.copy
    else:
        df_alternative = pd.read_json(alternative_json, orient = 'index', typ = "series").to_frame().T \
        .rename(columns={'t_block_in_frist': 't_block_in_first'}) \
        .rename(columns={'t_block_last_out': 't_block_out_last'})

    def extract_json(file):
        name_number = os.path.basename(file).split(".", 1)[0].split("_")[0:2]
        return pd.read_json(file, orient='index', typ="series").to_frame().T\
        .assign(name=name_number[0], martrikelnummer=name_number[1])\
        .rename(columns={'t_block_in_frist':'t_block_in_first'}) \
        .rename(columns={'t_block_last_out': 't_block_out_last'})

	# get json files, extract them and concate them
    df_results = pd.concat(list(map(extract_json,glob.glob(result_dir, recursive = True))), ignore_index= True)

	# check the student solution !!+ alternative solution!
    for c in df_solution.columns.to_list():
        df_results.loc[:, str(c)+"_CHECK"] = ((df_results.loc[:,c] == df_solution.loc[0,c]) |
                                              (df_results.loc[:,c] == df_alternative.loc[0,c])) * weights[c]
    #### correct this!
    col = df_solution.columns.to_list()
    col_check = [c+"_CHECK" for c in col]
    col = col + col_check
    col.sort()

    df_results.loc[:,"sum"] = df_results.loc[:,col_check].sum(axis = 1)

    df_results.loc[:,["martrikelnummer","name","sum"] + col].sort_values("martrikelnummer")\
        .reset_index(drop = True)\
        .to_csv(output_file)

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',
                        help='Output file path (CSV)', type=str,
                        required=True)
    parser.add_argument('-s', '--solution',
                        help='Input file path (JSON)', type=str,
                        required=True)
    parser.add_argument('-a', '--alternative',
                        help='Input file path (JSON)', type=str,
                        required=False)
    parser.add_argument('-r', '--results',
                        help='Input dir path (*.JSON)', type=str,
                        required=True)
    args = parser.parse_args()

    main(args)
