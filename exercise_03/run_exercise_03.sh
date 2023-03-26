submission_folder="../../submissions/exercise_03"
data_folder="../../data/exercise_03"
code_path=`pwd`

# activate python envir
. ../../venc-caa/bin/activate


cd $submission_folder

# unzip if necessary
zip_files=`find ./submitted/*/*.zip`
echo "# unzip"
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

py_files=`find "./submitted/" -name "*.py" | grep "exercise_03_"`
mkdir -p "./all_scripts"
mkdir -p "./results"
echo "# copy & execute"


####################################

for p in $py_files
do
	student=$(echo $p | awk -F "/" '{print $4}' | awk -F "_" '{print $3 "_" $4}' | awk -F "." '{print $1}')
	echo "-${student} \n"
	script="./all_scripts/exercise_03_${student}.py"
	outfile="./results/${student}_03.json"
	# copy python excersice file
	cp $p $script
	# execute 
	echo python $script -a ${data_folder}"/addrs_response.json" -e ${data_folder}"/entities_response.json" -n ${data_folder}"/neighbors_out.json" -o $outfile
	python $script -a ${data_folder}"/addrs_response.json" -e ${data_folder}"/entities_response.json" -n ${data_folder}"/neighbors_out.json" -o $outfile
done


# run solution to get verification reference
python ${code_path}/solution_03.py -a ${data_folder}"/addrs_response.json" -e ${data_folder}"/entities_response.json" -n ${data_folder}"/neighbors_out.json" -o "./out_solution.json"

python ${code_path}/evaluate_results_03.py -s "out_solution_03.json" -r "./results/*_03.json" -o "./evaluation.csv"

