#! /bin/bash
targetDirectory="/srv01/agrp/arkas/PtarmiganH52Root"
targetPyDir="/storage/agrp/arkas/E320WorkArea_a0_10.0"
sftp arkas@wipp-an1 << EOF
put Gridh5Format2Root.py $targetDirectory
put GridTextFormat2Root.py $targetDirectory
put runLocal.sh $targetDirectory
put gridScript.sh $targetDirectory
put sendJobs.sh $targetDirectory
put resendJobs.sh $targetDirectory
put gridScriptinSeries.sh $targetDirectory
put sendJobsinSeries.sh $targetDirectory
put resendJobsinSeries.sh $targetDirectory
put hadd.py $targetPyDir
put testchain.py $targetPyDir
put PreparePlotsFromH5.py $targetDirectory
EOF
