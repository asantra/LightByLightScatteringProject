#! /bin/bash

### how many jobs you want to submit, if -1, then submits jobs you set
fileExtns=${1:-"h5"}
pairrate=${2:-"1"}
a0value1=${3:-"10.0"}
a0value2=${4:-"10.0"}
#### runid for the output job name in the grid, increased by 1 for each job
runid=6000
### submitting upto nJobs you wanted
itSt=${runid}
itEnd=11923

for ((iter=itSt; iter<itEnd; iter++)); do
    ### a counter value
    b=1
    ### runId increased by one
    runid=$(( $runid + $b ))
    echo "runid: "$runid
    ### the place where the output and error file of the grid will live
    ### select two different a0values
    if [[ $runid -lt 5001 ]]; then
        a0value=$a0value1
    else
        a0value=$a0value2
    fi

    ### the place where the output and error file of the grid will live
    OUTDIRLOC="/storage/agrp/arkas/PtarmiganWorkAreaHorizontal_a0_"$a0value"_xFOne"
    
    flag=0
    if ls ${OUTDIRLOC}/run_$runid/*${fileExtns} &> /dev/null
    then
        flag=1
    else
        flag=2
    fi
    
    #### if there is error, resubmit them
    if [[ $flag -eq 1 ]]
    then 
        echo "This file exists: ${OUTDIRLOC}/run_$runid/*${fileExtns}"
    elif [[ $flag -eq 2 ]]
    then
        echo "This file does not exist: ${OUTDIRLOC}/run_$runid/*${fileExtns}"
        echo -n "$runid " >> missedh5FileRunNumber.txt         
    else
        echo "No problem in this set: ${DESTINATION}/run_$runid"
    fi
done