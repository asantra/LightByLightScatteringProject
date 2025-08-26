#! /bin/bash

### how many jobs you want to submit, if -1, then submits jobs you set in the script
nJobs=${1:-"-1"}
### pairrate for the run, default is 1
### pairrate for the run, for low a0 it is 1e9
pairrate=${2:-"1000000000"}
# a0value=${3:-"0.4"} ## 0.4 for 1053 nm and 0.32 for 527 nm
# a0value=${3:-"0.35"} ## 0.4 for 1053 nm and 0.32/0.35 for 527 nm
a0value=${3:-"0.32"} ## 0.4 for 1053 nm and 0.32 for 527 nm
#### runid for the output job name in the grid, increased by 1 for each job
runid=1000
### submitting upto nJobs you wanted
itSt=${runid}
itEnd=1400

### here only root processing run
failedFileLists="3447 "

for ((iter=itSt; iter<itEnd; iter++)); do
    ### a counter value
    b=1
    ### runId increased by one
    runid=$(( $runid + $b ))
    

    ##### send files whose runids are in failedFileLists
    ##### turn the block off if need to run on all files
    # ! [[ $failedFileLists =~ (^|[[:space:]])$runid($|[[:space:]]) ]] &&  echo "$runid NOT in the list: continuing" && continue || echo "$runid in the list: running on "${runid}


    ### the place where the output and error file of the grid will live
    DESTINATION="/storage/agrp/arkas/GridOutputE144_a0_"$a0value"_xF1B_Eachh5Weightedto1BX_1mmEBeamLength"
    OUTDIRLOC="/storage/agrp/arkas/E144Files/E144WorkArea_a0_"$a0value"_xF1B_Eachh5Weightedto1BX_1mmEBeamLength"    #### from where you are submitting jobs
    
    ### if main directory/run_id exists, delete
    if [[ -d "${DESTINATION}/run_$runid" ]]; then
        echo "Found a directory with output ${DESTINATION}/run_$runid! Deleting the previous one."
        rm -rf ${DESTINATION}/run_$runid
    fi
    
    echo "Working on "$a0value" for runid: "$runid
    #### create the run directory
    mkdir -p ${DESTINATION}"/run_"$runid
    mkdir -p ${OUTDIRLOC}
    #### from where you are submitting jobs
    PRESENTDIRECTORY=${PWD}

    
    #### submit jobs to the PBS system
    timeNow=$(date +%s)
    
    qsub -l ncpus=1,mem=3gb,io=0.1 -v parname1=${runid},parname2=${PRESENTDIRECTORY},parname3=${OUTDIRLOC},parname4=${a0value},parname5=${pairrate},parname6=${runid} -q N -N "run_"$runid -o "${DESTINATION}/run_"${runid} -e "${DESTINATION}/run_"${runid} gridScriptE144.sh
    ### sleep for 1 s, so that there is no problem in submitting jobs to the grid
    sleep 1s
    ### if number of jobs required is reached then break the loop
    if [[ $runid -eq $nJobs ]]; then
        break
    fi
done
