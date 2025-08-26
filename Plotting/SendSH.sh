#! /bin/bash
targetDirectory="/storage/agrp/arkas/E320Files/Analyzer/"
sftp arkas@wipp-an1 << EOF
put histogramMaker.cpp $targetDirectory
put inputFunctions.h $targetDirectory
put makePlotsE320.py $targetDirectory
put makePlotsELI-NP.py $targetDirectory
put /Users/arkasantra/arka/include/Functions.py $targetDirectory
EOF