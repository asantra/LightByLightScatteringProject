#! /bin/bash
targetDirectory="/srv01/agrp/arkas/PtarmiganGridRuns"
sftp arkas@wipp-an1 << EOF
put E320_profile_MASTER.yml $targetDirectory
put E144_profile_MASTER.yml $targetDirectory
put ELINP_profile_MASTER.yml $targetDirectory
put luxe_MASTER.yml $targetDirectory
put luxe_tdr_MASTER.yml $targetDirectory
put gridScript.sh $targetDirectory
put gridScriptE144.sh $targetDirectory
put sendJobs.sh $targetDirectory
put resendJobs.sh $targetDirectory
put sendJobsE144.sh $targetDirectory
put resendJobsE144.sh $targetDirectory
put identifyLostJobs.sh $targetDirectory
put simpleAna.py $targetDirectory
put simpleh5Ana.py $targetDirectory
put simpleh5AnaE144.py $targetDirectory
put simplePlot.py $targetDirectory
put simpleTree.py $targetDirectory
put renameFiles.py $targetDirectory
put checkPositronWeightinh5.py $targetDirectory
EOF
