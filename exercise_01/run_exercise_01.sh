submission_folder="../../submissions/exercise_01"
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

py_files=`find "./submitted/" -name "*.py" | grep "exercise_01_"`
mkdir -p "./all_scripts"
mkdir -p "./results"
echo "# copy & execute"

parameter_a=1PAjxMU6PXvZ2nhXuC6a22BKoUNiSU5UBu
for p in $py_files
do
	student=$(echo $p | awk -F "/" '{print $4}' | awk -F "_" '{print $3 "_" $4}' | awk -F "." '{print $1}')
	echo "-${student} \n"
	script="./all_scripts/exercise_01_${student}.py"
	outfile="./results/${student}_01.json"
	# copy python excersice file
	cp $p $script
	# execute 
	echo python $script -a $parameter_a -o $outfile
	python $script -a $parameter_a -o $outfile
done


# run solution to get verification reference
python ${code_path}/solution_01.py -a $parameter_a -o "out_solution_01_${parameter_a}.json"
python ${code_path}/alternative_01.py -a $parameter_a -o "out_alternative_01_${parameter_a}.json"

python ${code_path}/evaluate_results_01.py -r "./results/*.json" -s "out_solution_01_${parameter_a}.json" -a "out_alternative_01_${parameter_a}.json" -o "./evaluation_${parameter_a}.csv"

