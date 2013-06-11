
compareJSON.py --or Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON.txt Cert_190782-190949_8TeV_06Aug2012ReReco_Collisions12_JSON.txt temp.json
compareJSON.py --or Cert_198022-198523_8TeV_24Aug2012ReReco_Collisions12_JSON.txt temp.json temp.json
compareJSON.py --or Cert_190456-203853_8TeV_PromptReco_Collisions12_JSON_v2.txt temp.json temp.json
compareJSON.py --or Cert_201191-201191_8TeV_11Dec2012ReReco-recover_Collisions12_JSON.txt temp.json temp.json
compareJSON.py --or Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt temp.json MyJSON_RunA13Jul_RunA06Aug_RunB13Jul_RunC24Aug_RunCPromptV2_RunC11Dec_RunDPromptV1.txt 
rm temp.json
