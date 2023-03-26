import subprocess
import pandas as pd
import glob
import os
from argparse import ArgumentParser
import json

def main(args):

    # get all directories from "../../submissions/exercise_02/submitted"
    l_dir = glob.glob("../../submissions/exercise_02/submitted/*")
    path_results = "../../submissions/exercise_02/results/"

    if args.output is not None:

        output_file = args.output

    if args.transactions is not None:

        test_transactions = args.transactions # "./input_txs.json"
        with open(test_transactions, 'r') as ft:
            test_input = json.load(ft)
        #test_transactions = "./input_txs.json"



    else:
        print("No transactions given. ")

    # create a list for the resutls to concat later
    dict_results = dict()


    # for each l_dir list entry, ...
    for dir in l_dir:
        # get the names and matriculation numbers
        name = os.path.basename(dir).split("_")[0]

        # get the path to the python file# get the contained python files
        py_files = glob.glob(dir + "/*.py")

        # if more than one python file is found, print a warning
        if len(py_files) > 1:
            print("Warning: More than one python file found in directory " + dir)
        else:
            # take the first python file
            py_file = py_files[0]
            matr = os.path.basename(py_file).split("_")[-1].split(".")[0]

            out_file = path_results + "/out_" + name.replace(" ", "") + "_" + matr + ".json"

            cmd = "python '" + \
                  os.path.abspath(py_file) + \
                  "' --transactions " + test_transactions + \
                  " --output '" + os.path.abspath(out_file) + "'"

            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()

            # print error message, if any
            if err is not None:
                print("Error " + name + ": " + err)

            try:

                with open(out_file, 'r') as ft:
                    student_result = json.load(ft)
                    dict_results[name+"_"+matr] = student_result
            except:

                print("Error " + name + ": " + out_file + " not found")
                dict_results[name+"_"+matr] =  []

    # run solution
    output_solution = path_results + "/solution.json"
    cmd = "python 'solution_02.py' " + \
          " --transactions " + test_transactions + \
          " --output '" + os.path.abspath(output_solution) + "'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

    l_results = []



    # for each json file in the results directory, ...
    for key, d_r in dict_results.items():
        print(key, d_r)
        with open(output_solution, 'r') as ft:
            l_solution = json.load(ft)
            solution_result = [set(l) for l in l_solution]

        for d_r_value in d_r:
            print(set(d_r_value))

            if set(d_r_value) in solution_result:
                [solution_result.remove(s) for s in solution_result if s == set(d_r_value)]

        print(f"{key}: {5-len(solution_result)}")
        if len(solution_result) == 0:
            comment = "Well done!"
        else:
            comment = f"{len(solution_result)} clusters have not been detected. \n\n" + \
                                     f"Missing clusters: {str(l_solution)} "+ \
                                     f"from input: {str(test_input)}"

        l_results.append(
            pd.DataFrame({"name": key.split("_")[0],
                          "matr": key.split("_")[1],
                          "points": 5-len(solution_result),
                          "comment": comment,
                          "solution": str(d_r)}, index = [0])
        )
    df_results = pd.concat(l_results, ignore_index=True)
    df_results.to_csv(output_file, index=False)

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',
                        help='Output file path (CSV)', type=str,
                        required=True)
    parser.add_argument('-t', '--transactions',
                        help='Input dir path (*.JSON)', type=str,
                        required=True)
    args = parser.parse_args()

    main(args)
