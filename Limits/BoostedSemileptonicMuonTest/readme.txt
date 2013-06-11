0. Summaries

0.1 Command line using theta_driver

theta_driver preprocess --model 'model: type = narrow_resonances, jet1 = 150' --workdir narrow_resonances --analysis summary *.root
theta_driver preprocess --model 'model: type = narrow_resonances, jet1 = 250' --workdir narrow_resonances --analysis summary *.root

Note: same for wide resonances !

1. Computing the asymptotic limits

1.1 Command line using theta_driver

theta_driver preprocess --model 'model: type = narrow_resonances, jet1 = 150' --workdir narrow_resonances --analysis expected_asymptotic *.root
theta_driver preprocess --model 'model: type = narrow_resonances, jet1 = 200' --workdir narrow_resonances --analysis expected_asymptotic *.root
theta_driver preprocess --model 'model: type = narrow_resonances, jet1 = 250' --workdir narrow_resonances --analysis expected_asymptotic *.root

Note: same for wide resonances !

2. Computing the bayesian limits

2.1 Command line using theta_driver

theta_driver preprocess --model 'model: type = narrow_resonances, jet1 = 150' --workdir narrow_resonances_150 --analysis bayesian *.root
theta_driver preprocess --model 'model: type = narrow_resonances, jet1 = 250' --workdir narrow_resonances_250 --analysis bayesian *.root
theta_driver submit --workdir narrow_resonances_150
theta_driver submit --workdir narrow_resonances_250
crab -status -c narrow_resonances_150/crab
crab -status -c narrow_resonances_250/crab
crab -getoutput -c narrow_resonances_150/crab
crab -getoutput -c narrow_resonances_250/crab
theta_driver getoutput --workdir narrow_resonances_150
theta_driver getoutput --workdir narrow_resonances_250
theta_driver postprocess --workdir narrow_resonances_150
theta_driver postprocess --workdir narrow_resonances_250

2.2 Command line using theta_driver and nosys

Same as 2.1 only changing

theta_driver preprocess --model 'model_npsys: type = narrow_resonances, jet1 = 150' --workdir narrow_resonances_150 --analysis bayesian *.root
theta_driver preprocess --model 'model_nosys: type = narrow_resonances, jet1 = 250' --workdir narrow_resonances_250 --analysis bayesian *.root


theta_driver preprocess --model 'model_nosys: type = wide_resonances; chi2 = 2' --workdir wide_resonances_chi_2 --analysis bayesian *.root


