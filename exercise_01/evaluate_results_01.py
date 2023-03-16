import subprocess
import pandas as pd
import glob
import os
from argparse import ArgumentParser

def main(args):

    # get all directories from "../../submissions/exercise_01/submitted"
    l_dir = glob.glob("../../submissions/exercise_01/submitted/*")
    path_results = "../../submissions/exercise_01/results/"

    if args.address is not None:
        test_addr = args.address
    else:
        test_addr = "12sENwECeRSmTeDwyLNqwh47JistZqFmW8"

    # create a list for the resutls to concat later
    l_df = []

    # for each l_dir list entry, ...
    for dir in l_dir:
        # get the names and matriculation numbers
        name = os.path.basename(dir).split("_")[0]
        matr = os.path.basename(dir).split("_")[1]

        # get the contained python files
        py_files = glob.glob(dir + "/*.py")

        # if more than one python file is found, print a warning
        if len(py_files) > 1:
            print("Warning: More than one python file found in directory " + dir)
        else:
            # take the first python file
            py_file = py_files[0]
            out_file = path_results + "/out_" + name.replace(" ","") + "_" + matr + ".json"

            cmd = "python '" + \
                  os.path.abspath(py_file) + \
                  "' --address " + test_addr + \
                  " --output '" +os.path.abspath(out_file) +"'"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()

            # print error message, if any
            if err is not None:
                print("Error " + name + ": " + err)

            # read output file
            try:
                df = pd.read_json(out_file, orient = 'index', typ = "series").to_frame().T
            except:
                df = pd.DataFrame()
            # add name and matriculation number
            df['name'] = name
            df['matr'] = matr

            df.rename(columns={'n_neighbors_in':'n_neighbours_in'}, inplace=True)
            df.rename(columns={'n_neighbors_out':'n_neighbours_out'}, inplace=True)

            # add to list
            l_df.append(df)

    # run solution
    output_solution = path_results + "/solution.json"
    cmd = "python 'solution_01.py' " \
          "--address "+ test_addr + " " \
          "--output '" + os.path.abspath(output_solution) + "'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()



    # concat all data frames
    df = pd.concat(l_df, ignore_index=True)

    # compare student results with solution
    # print error message, if any
    if err is not None:
        print("Error " + name + ": " + err)

    # read output file
    df_solution = pd.read_json(output_solution, orient = 'index', typ = "series").to_frame().T
    df_solution['name'] = "SOLUTION"
    df_solution['matr'] = "SOLUTION"

    # introduce weights (points)
    weights = pd.Series(data={'satoshi_in': 0.4, 'satoshi_out': 0.4, 'balance': 0.2, 'fees': 1.,
                              'b_in_first': 0.5, 'b_out_first': 0.5, 'n_neighbours_in': 1., 'n_neighbours_out': 1.})

    # go through all columns of solution and compare with student results
    l_result_cols = []
    df["comment"] = ""
    for i, col in enumerate(df_solution.columns):
        if col not in ['name', 'matr']:
            # get the column of the solution
            col_solution = df_solution[col].iloc[0]
            # get the column of the student results
            col_student = df[col]
            # compare the two columns
            result_col_name = 'p_' + str(i) + "_" + col
            l_result_cols.append(result_col_name)
            correct = (col_solution == col_student)
            df[result_col_name] = (correct) * weights[col]
            df.loc[(~correct) ,"comment"] = df.loc[(~correct), "comment"] + \
                                    "Correct solution for '" + col + "' should be " + str(col_solution) + "\n"
    # row sum of the results
    df["points"] = df.loc[:, l_result_cols].sum(axis=1)
    df.loc[df["points"] == 5, "comment"] = "Well done!"

    # save results
    # reorder columns: name, matr, points, comment, all other columns
    cols_reorder = df.columns.tolist()
    [cols_reorder.remove(c) if (c in cols_reorder) else None for c in ['name', 'matr', 'points', 'comment']]
    cols_reorder = ['name', 'matr', 'points', 'comment'] + cols_reorder

    df.loc[:, cols_reorder].to_csv(path_results + "/results_"+test_addr+".csv", index=False)

    print("Test address: " + test_addr)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-a', '--address',
                        help='BTC address for computing statistics statistics',
                        type=str, required=True)
    args = parser.parse_args()
    main(args)

