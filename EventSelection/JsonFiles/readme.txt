Nominal pileup
--------------

pileupCalc.py -i MyJSON_RunA13Jul_RunA06Aug_RunB13Jul_RunC24Aug_RunCPromptV2_RunC11Dec_RunDPromptV1.txt --inputLumiJSON pileup_JSON_DCSONLY_190389-208686_corr.txt --calcMode true --minBiasXsec 69400 --maxPileupBin 50 --numPileupBins 1000 PileUpHistoCycle.DATA.ElectronHad_208686.root

----

Run 194051 not found in Lumi/Pileup input file.  Check your files!
Run 202973, LumiSection 910 not found in Lumi/Pileup input file. Check your files!
Run 202973, LumiSection 911 not found in Lumi/Pileup input file. Check your files!
Run 202973, LumiSection 912 not found in Lumi/Pileup input file. Check your files!
Run 206066 not found in Lumi/Pileup input file.  Check your files!
Run 206207, LumiSection 689 not found in Lumi/Pileup input file. Check your files!
Run 206207, LumiSection 690 not found in Lumi/Pileup input file. Check your files!
Run 207372 not found in Lumi/Pileup input file.  Check your files!


Plus pileup
-----------

pileupCalc.py -i MyJSON_RunA13Jul_RunA06Aug_RunB13Jul_RunC24Aug_RunCPromptV2_RunC11Dec_RunDPromptV1.txt --inputLumiJSON pileup_JSON_DCSONLY_190389-208686_corr.txt --calcMode true --minBiasXsec 73500 --maxPileupBin 50 --numPileupBins 1000 PileUpHistoCycle.DATA.ElectronHad_208686_plus.root


Minus pileup
-----------

pileupCalc.py -i MyJSON_RunA13Jul_RunA06Aug_RunB13Jul_RunC24Aug_RunCPromptV2_RunC11Dec_RunDPromptV1.txt --inputLumiJSON pileup_JSON_DCSONLY_190389-208686_corr.txt --calcMode true --minBiasXsec 65300 --maxPileupBin 50 --numPileupBins 1000 PileUpHistoCycle.DATA.ElectronHad_208686_minus.root

