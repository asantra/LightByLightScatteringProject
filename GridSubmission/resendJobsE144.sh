#! /bin/bash

### how many jobs you want to submit, if -1, then submits jobs you set
fileExtns=${1:-"ER"}
### pairrate for the run, default is 1
### pairrate for the run, for low a0 it is 1e9
pairrate=${2:-"1"}
a0value=${3:-"0.4"} ## 0.4 for 1053 nm and 0.32 for 527 nm

#### runid for the output job name in the grid, increased by 1 for each job
runid=100
### submitting upto nJobs you wanted
itSt=${runid}
itEnd=200

### here only root processing run
failedFileLists="6025 "


for ((iter=itSt; iter<itEnd; iter++)); do
    ### a counter value
    b=1
    ### runId increased by one
    runid=$(( $runid + $b ))
    echo "runid: "$runid
    ### the place where the output and error file of the grid will live

    ### the place where the output and error file of the grid will live
    DESTINATION="/storage/agrp/arkas/GridOutputE144_a0_"$a0value"_xF1_Eachh5Weightedto1BX"
    OUTDIRLOC="/storage/agrp/arkas/E144Files/E144WorkArea_a0_"$a0value"_xF1_Eachh5Weightedto1BX"    #### from where you are submitting jobs
    PRESENTDIRECTORY=${PWD}
    
    flag=0
    if ls ${DESTINATION}/run_$runid/*${fileExtns} &> /dev/null
    then
        if grep -rnwq ${DESTINATION}/run_$runid/*${fileExtns} -e "error"
        then
            flag=1
        elif grep -rnwq ${DESTINATION}/run_$runid/*${fileExtns} -e "Error"
        then
            flag=1
        elif grep -rnwq ${DESTINATION}/run_$runid/*${fileExtns} -e "OSError"
        then
            flag=1
        elif grep -rnwq ${DESTINATION}/run_$runid/*${fileExtns} -e "Killed"
        then
            flag=1
        elif grep -rnwq ${DESTINATION}/run_$runid/*${fileExtns} -e "killed"
        then
            flag=1
        elif grep -rnwq ${DESTINATION}/run_$runid/*${fileExtns} -e "Aborting"
        then
            flag=1
        elif grep -rnwq ${DESTINATION}/run_$runid/*${fileExtns} -e "Caught Geant4 exception"
        then
            flag=1
        elif grep -rnwq ${DESTINATION}/run_$runid/*${fileExtns} -e "Interrupted"
        then
            flag=1
        elif grep -rnwq ${DESTINATION}/run_$runid/*${fileExtns} -e "Aborted"
        then
            flag=1
        else
            flag=0
        fi
    else
        flag=2
    fi
    
    #### if there is error, resubmit them
    if [[ $flag -eq 1 ]]
    then 
        echo "At least one error for ${DESTINATION}/run_$runid"
        if [[ -d "${DESTINATION}/run_$runid" ]]; then
            echo "Found a directory with output ${DESTINATION}/run_$runid! Deleting the previous one."
            rm -rf ${DESTINATION}/run_$runid
        fi
        
        #### create the run directory
        mkdir -p ${DESTINATION}"/run_"$runid
        mkdir -p ${OUTDIRLOC}
        #### from where you are submitting jobs
        PRESENTDIRECTORY=${PWD}
        
        #### submit jobs to the PBS system
        timeNow=$(date +%s)
        qsub -l ncpus=1,mem=6gb,io=0.1 -v parname1=${runid},parname2=${PRESENTDIRECTORY},parname3=${OUTDIRLOC},parname4=${a0value},parname5=${pairrate},parname6=${runid} -q N -N "run_"$runid -o "${DESTINATION}/run_"${runid} -e "${DESTINATION}/run_"${runid} gridScriptE144.sh
        ### sleep for 1 s, so that there is no problem in submitting jobs to the grid
        sleep 1s
    elif [[ $flag -eq 2 ]]
    then
        echo "This folder does not exist: ${DESTINATION}/run_$runid"
        echo "At least one problem for ${DESTINATION}/run_$runid"
        
        if [[ -d "${DESTINATION}/run_$runid" ]]; then
            echo "Found a directory with output ${DESTINATION}/run_$runid! Deleting the previous one."
            rm -rf ${DESTINATION}/run_$runid
        fi
        
        #### create the run directory
        mkdir -p ${DESTINATION}"/run_"$runid
        mkdir -p ${OUTDIRLOC}
        #### from where you are submitting jobs
        PRESENTDIRECTORY=${PWD}
        
        #### submit jobs to the PBS system
        timeNow=$(date +%s)
        qsub -l ncpus=1,mem=6gb,io=0.1 -v parname1=${runid},parname2=${PRESENTDIRECTORY},parname3=${OUTDIRLOC},parname4=${a0value},parname5=${pairrate},parname6=${runid} -q N -N "run_"$runid -o "${DESTINATION}/run_"${runid} -e "${DESTINATION}/run_"${runid} gridScriptE144.sh
        ### sleep for 1 s, so that there is no problem in submitting jobs to the grid
        sleep 1s
    else
        echo "No problem in this set: ${DESTINATION}/run_$runid"
    fi
done