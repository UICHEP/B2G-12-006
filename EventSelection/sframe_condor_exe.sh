#! /bin/bash
# Source version of CMSSW associated to SFRAME
cd /uscms_data/d1/baites/CMSSW/CMSSW_5_3_3/src
eval `scramv1 runtime -sh`
cd /uscms_data/d1/baites/SFrame/SFrame-03-05-16 
source fullsetup.sh
# Run the sframe job
cd /uscms/home/baites/nobackup/UserCode/UICAnalyses/ZprimeAnalysis2012 
sframe_main $1
