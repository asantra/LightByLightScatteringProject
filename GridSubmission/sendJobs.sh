#! /bin/bash

### how many jobs you want to submit, if -1, then submits jobs you set in the script
nJobs=${1:-"-1"}
### pairrate for the run, default is 1
### pairrate for the run, for low a0 it is 1e9
### for E320, it can be as big as 1e6
pairrate=${2:-"1000000000"}
### for ELI-NP pairrate=1
# ## for E320
a0value1=${3:-"5.0"}
a0value2=${4:-"5.0"}
a0value3=${4:-"5.0"}
a0value4=${4:-"5.0"}

# ### for ELI-NP a0=20
# a0value1=${3:-"20.0"}
# a0value2=${4:-"20.0"}
# a0value3=${4:-"20.0"}
# a0value4=${4:-"20.0"}

#### runid for the output job name in the grid, increased by 1 for each job
runid=0
### submitting upto nJobs you wanted
itSt=${runid}
itEnd=500

### here only root processing run
failedFileLists="164 165 166 167 168 169 171 "

for ((iter=itSt; iter<itEnd; iter++)); do
    ### a counter value
    b=1
    ### runId increased by one
    runid=$(( $runid + $b ))
    

    ##### send files whose runids are in failedFileLists
    ##### turn the block off if need to run on all files
    # ! [[ $failedFileLists =~ (^|[[:space:]])$runid($|[[:space:]]) ]] &&  echo "$runid NOT in the list: continuing" && continue || echo "$runid in the list: running on "${runid}

    ### select four different a0values
    if [[ $runid -le 6500 ]]; then
        a0value=$a0value1
    elif [[ ( $runid -gt 6500 ) && ( $runid -le 7000 ) ]]; then
        a0value=$a0value2
    elif [[ ( $runid -gt 7000 ) && ( $runid -le 7500 ) ]]; then
        a0value=$a0value3
    else
        a0value=$a0value4
    fi

    ### the place where the output and error file of the grid will live
    
    # DESTINATION="/storage/agrp/arkas/GridOutputE320_a0_"$a0value"_positronpairrate_xF1M"
    # OUTDIRLOC="/storage/agrp/arkas/E320Files/E320WorkArea_a0_"$a0value"_positronpairrate_xF1M"


    DESTINATION="/storage/agrp/arkas/GridOutputE320_a0_"$a0value"_xF1B_Eachh5Weightedto1BX"
    OUTDIRLOC="/storage/agrp/arkas/E320Files/E320WorkArea_a0_"$a0value"_xF1B_Eachh5Weightedto1BX"    #### from where you are submitting jobs


    # ### ELINP files
    # DESTINATION="/storage/agrp/arkas/GridOutputELINP_LCFA_a0_"$a0value
    # OUTDIRLOC="/storage/agrp/arkas/ELINPFiles/ELINPWorkArea_Weight1_LCFA_a0_"$a0value    #### from where you are submitting jobs
    
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
    
    qsub -l ncpus=1,mem=6gb,io=0.1 -v parname1=${runid},parname2=${PRESENTDIRECTORY},parname3=${OUTDIRLOC},parname4=${a0value},parname5=${pairrate},parname6=${runid} -q N -N "run_"$runid -o "${DESTINATION}/run_"${runid} -e "${DESTINATION}/run_"${runid} gridScript.sh
    ### sleep for 1 s, so that there is no problem in submitting jobs to the grid
    sleep 1s
    ### if number of jobs required is reached then break the loop
    if [[ $runid -eq $nJobs ]]; then
        break
    fi
done
