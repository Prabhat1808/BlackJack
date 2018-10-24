#/bin/bash
. vpl_environment.sh
unzip *.zip > /dev/null 
orig_dir=$(pwd)
first_par=${VPL_SUBFILE0%.*}
#cd $first_par
echo "-------Check for compile.sh, run.sh and writeup.sh -------"
ls compile.sh run.sh writeup.txt
echo "----------Checking writeup.txt---------------"
if python $orig_dir/writeup_checker.py ./writeup.txt; then
    echo "Proceeding for further checks"
else 
    echo "Not proceeding for further checks"
    exit 0
fi
echo "--------------Running compile.sh -----------------: "
chmod +x compile.sh
if timeout 30s ./compile.sh; then
    printf "\n"
    echo "-------------Runnning against input 0.5 with timeout of 20 secs---------------"
    chmod +x run.sh
    execution=$(timeout 20s ./run.sh 0.5 2>&1) # equivalent to 0.1 mins time limit in input files
    exit_status=$?
    if [ $exit_status -eq 124 ] #timeout occured
    then
        echo "----Timed out in 20 secs!!\nCould not check output format------"
        
    elif [ $exit_status -eq 0 ] #No runtime error occured (Correct or wrong answer)
    then
        echo "----Executed run.sh----"
        printf "$execution\n\n"
        echo "----Running format checker-----"
        python3 FormatCheck.py $orig_dir/Policy.txt
        
    else #some error occured for this test case
        echo "------!!!Run time error !!------"
        printf "Runtime Error: $execution\n\n"
    fi
else
    echo "compilation failed/timed out"
fi
