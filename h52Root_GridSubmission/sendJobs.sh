#! /bin/bash

### how many jobs you want to submit, if -1, then submits jobs you set
nJobs=${1:-"-1"}
version=${2:-"1"}
#### runid for the output job name in the grid, increased by 1 for each job
runid=0

### submitting upto nJobs you wanted
itSt=0
itEnd=202

for ((iter=itSt; iter<itEnd; iter++)); do
    ### a counter value
    b=1
    ### runId increased by one
    runid=$(( $runid + $b ))
    echo "runid: "$runid
    ### the place where the output and error file of the grid will live
    ### ELI-NP
    # DESTINATION="/storage/agrp/arkas/GridOutputPtarmiganH5Format2Root_LMA_Actual"
    ### E320
    DESTINATION="/storage/agrp/arkas/GridOutputPtarmiganH5Format2Root_E320"
    ### create the main directory if it does not exists
    mkdir -p ${DESTINATION}
    
    ### if main directory/run_id exists, delete
    if [[ -d "${DESTINATION}/run_$runid" ]]; then
        echo "Found a directory with output ${DESTINATION}/run_$runid! Deleting the previous one."
        rm -rf ${DESTINATION}/run_$runid
    fi

    #### create the run directory
    mkdir -p ${DESTINATION}"/run_"$runid
    #### from where you are submitting jobs
    PRESENTDIRECTORY=${PWD}
    #### submit jobs to the PBS system
    qsub -l ncpus=1,mem=2gb,io=0.1 -v parname1=${runid},parname2=${PRESENTDIRECTORY},parname3=${version} -q N -N "run_"$runid -o "${DESTINATION}/run_"${runid} -e "${DESTINATION}/run_"${runid} gridScript.sh
    ### sleep for 1 s, so that there is no problem in submitting jobs to the grid
    sleep 1s
    ### if number of jobs required is reached then break the loop
    if [[ $runid -eq $nJobs ]]; then
        break
    fi
done
