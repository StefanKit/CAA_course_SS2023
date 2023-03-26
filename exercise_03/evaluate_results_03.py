from argparse import ArgumentParser

import pandas as pd
import glob
import os

def main(args):

    solution_json = args.solution
    results_dir = args.results
    output_file = args.output

	# introduce weights (points)
    weights = pd.Series(data = {'avg_received_txs':0.5, 'avg_sent_out_nbrs':0.5,
                                'avg_active_time' : 1, 'avg_active_time_no_outlier' : 0.5,
                                'total_received':0.5, 'entities_nbrs_exchange':1,
                                'entities_nbrs_wallet':1})
    type_int = ['avg_received_txs', 'avg_sent_out_nbrs', 'avg_active_time', 'avg_active_time_no_outlier', 'total_received']

	# read result, rename misspelling columns
    se_solution = pd.read_json(solution_json, orient = 'index', typ = "series")
    se_solution = se_solution.apply(lambda x: str(sorted(x)) if (type(x) == type(list())) else x)

    def extract_json(file):

        name_number = os.path.basename(file).split(".", 1)[0].split("_")[0:2]
        student_result = pd.read_json(file, orient = 'index', typ = "series")
        student_result = student_result.apply(lambda x: str(sorted(x)) if (type(x) == type(list())) else x)

        dict_student = {'name':name_number[0],
                        'martrikelnummer':name_number[1]}
        dict_student.update(student_result.to_dict())
        return(pd.DataFrame(data = dict_student, index = [0]))

	# get json files, extract them and concate them
    df_out = pd.concat(list(map(extract_json,glob.glob(results_dir, recursive = True))), ignore_index= True)
    for s in type_int:
        df_out.loc[:,s] = df_out.loc[:, s].astype(int)

    list_check = []
    for w in weights.iteritems():
        list_check.append(str(w[0]+"_CHECK"))
        df_out.loc[:,str(w[0]+"_CHECK")] = (df_out.loc[:,w[0]] == se_solution.loc[w[0]]) * w[1]

    df_out.loc[:,"sum"] = df_out.loc[:,list_check].sum(axis = 1)

    df_out.\
        sort_values("martrikelnummer")\
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
    parser.add_argument('-r', '--results',
                        help='Input file path (JSON)', type=str,
                        required=True)
    args = parser.parse_args()

    main(args)
