#! /bin/bash

mkdir /pnfs/cms/WAX/11/store/user/b2g12006/$1 

for file in `ls *.root`
do
    cmd="srmcp -2 file:///$PWD/$file srm://cmssrm.fnal.gov:8443/srm/managerv2?SFN=/11/store/user/b2g12006/$1/$file"
    echo $cmd
    $cmd
done

