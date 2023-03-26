submission_folder="../../submissions/exercise_02"
data_folder="../../data/exercise_02"
code_path=`pwd`

# activate python envir
. ../../venc-caa/bin/activate

# go to submission folder
cd $submission_folder

# find all *.py files in all contained subfolders
py_files=`find "./submitted/" -name "*.py" | grep "exercise_02_"`
# for each python file
for p in $py_files
do
  # get the student name
  student=$(echo $p | awk -F "/" '{print $4}' | awk -F "_" '{print $3 "_" $4}' | awk -F "." '{print $1}')
  # create a folder for the student
  student =

  mkdir -p "./submitted/${student}"
  # copy the python file to the student folder
  cp $p "./submitted/${student}/exercise_02_${student}.py"
done


# filter the names of the students as the third part of the file name
students=`echo $py_files | awk -F "/" '{print $4}' | awk -F "_" '{print $3 "_" $4}' | awk -F "." '{print $1}'`



for z in $zip_files
do
	echo "-${student}"
	dir=$(echo $z | cut -d "/" -f 1-3)
	unzip -n $z -d $dir
	student=$(echo $dir | awk -F "/" '{print $3}' | awk -F "_" '{print $1}')	
	
done


## requirements
# find all requirement files and paste them
find ./submitted/*/requirements.txt -exec cat {} + > requirements.txt
# edit them manually
nano requirements.txt
cat requirements.txt | echo
# install requirements
pip install -r requirements.txt

# replace spaces in path
find "./submitted/" -type d -name "* *" -print0 -exec bash -c 'mv "$0" "${0// /_}"' {} \;

py_files=`find "./submitted/" -name "*.py" | grep "exercise_02_"`
mkdir -p "./all_scripts"
mkdir -p "./results"
echo "# copy & execute"


####################################

for p in $py_files
do
	student=$(echo $p | awk -F "/" '{print $4}' | awk -F "_" '{print $3 "_" $4}' | awk -F "." '{print $1}')
	echo "-${student} \n"
	script="./all_scripts/exercise_02_${student}.py"
	outfile_sample="./results/${student}_sample_02.json"
	outfile_rest="./results/${student}_rest_02.json"
	# copy python excersice file
	cp $p $script
	# execute 
	echo python $script -t ${data_folder}"/input_txs_sample.json" -o $outfile_sample
	python $script -t ${data_folder}"/input_txs_sample.json" -o $outfile_sample
	echo python $script -t ${data_folder}"/input_txs_rest.json" -c $outfile_sample -o $outfile_rest
	python $script -t ${data_folder}"/input_txs_rest.json" -c $outfile_sample -o $outfile_rest
done


# run solution to get verification reference
python ${code_path}/solution_02.py -t ${data_folder}"/input_txs_sample.json" -o "out_solution_sample_02.json"
python ${code_path}/solution_02.py -t ${data_folder}"/input_txs_rest.json" -c "out_solution_sample_02.json" -o "out_solution_rest_02.json"


python ${code_path}/evaluate_results_02.py -a "out_solution_sample_02.json" -b "./out_solution_rest_02.json" -x "./results/*_sample_02.json" -y "./results/*_rest_02.json" -o "./evaluation.csv"

