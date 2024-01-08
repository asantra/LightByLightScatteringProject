#! /bin/bash

xi=${1:-"3"}
gamma=${2:-"0p7"}
version=${3:-"1"}
inE=${4:-"125000.0"}

# echo "working on xi="${xi}" gamma="${gamma}
InputDir="/Users/arkasantra/arka/Tom_Work_Theory/"
echo " h5 file to root "
python3 ${InputDir}/Analyzer/h5Format2Root.py -x ${xi} -g ${gamma} -v ${version}

echo "root file to  histogram "
python3 ${InputDir}/Plotting/makeRootFiles.py -x ${xi} -g ${gamma} -v ${version} -n ${inE}

# echo "plot the root histogram"
# python3 makePlots.py -in1 raw_lightbylight_xi3_gamma${gamma}_histograms.root -in2 raw_lightbylight_xi10_gamma${gamma}_histograms.root -in3 raw_lightbylight_xi20_gamma${gamma}_histograms.root -in4 raw_lightbylight_xi30_gamma${gamma}_histograms.root -out gamma${gamma}


