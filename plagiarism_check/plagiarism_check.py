import os
import subprocess
from argparse import ArgumentParser
import pandas as pd
import csv
import glob

# python3 code/exercise_03/plagiarism_check.py
# -f submissions/exercise_03/all_scripts
# -o submissions/exercise_03/out_plagiarim.csv

def main(args):

    folder = args.folder
    outpath = args.output


    allscripts = []
    col1=[]
    col2=[]
    col3=[]

    allscripts = glob.glob(f"{folder}/*/*.py")
    for i in range(len(allscripts)-1):
        for j in range(i+1,len(allscripts)):
            student1 = allscripts[i].split(os.path.sep)[-1].split('_')[2]
            student2 = allscripts[j].split(os.path.sep)[-1].split('_')[2]
            command = "python3 pycode_similar.py '"+ allscripts[i]+"' '"+allscripts[j]+"'"
            try:
                o = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                print(command)
            out = o.decode()
            col1.append(student1)
            col2.append(student2)
            col3.append(float(out.splitlines()[2][:4]))
    res = pd.DataFrame.from_dict({'student1': col1,'student2':col2,'similarity':col3})
    res = res.sort_values(by=['similarity'],ascending=False)
    res.to_csv(outpath, index=False)



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--folder',
                        help='Path of folder containing python scripts submitted by students ',
                        type=str, required=True)
    parser.add_argument('-o', '--output',
                        help='Path of output csv file where to write the plagiarism results',
                        type=str, required=True)
    args = parser.parse_args()

    main(args)