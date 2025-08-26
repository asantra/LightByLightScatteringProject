#! /bin/bash
#PBS -m n
#PBS -l walltime=01:00:00

#### script that run the python script, the MadGraph generator
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
### for latest root
# lsetup "views LCG_104b_ATLAS_2 x86_64-centos7-gcc11-opt"
lsetup "views LCG_104c x86_64-el9-gcc13-opt"
# echo "Installing numpy and h5py"
# pip install numpy --user
# pip install h5py --user

# ### linking HDF5 library
export LD_LIBRARY_PATH=/srv01/agrp/arkas/HDF5/HDF5_Install/lib:${LD_LIBRARY_PATH}
echo "running the python script>>>>>>"
iteration=${parname1}
directory=${parname2}
version=${parname3}
nStart=${parname4}
increment=${parname5}

nFinish=$(( ${nStart} + ${increment}-1 ))

echo "running from ${nStart} to ${nFinish}"

#### go to the directory where the files live
cd ${directory}
echo "I am now in "${PWD}
echo "prepare output directory"
for njob in $(seq ${nStart} 1 ${nFinish}); do
    echo "iteration: "$njob
    time python Gridh5Format2Root.py -x 10.0 -g 10.0 -v ${version} -i ${njob}
done

