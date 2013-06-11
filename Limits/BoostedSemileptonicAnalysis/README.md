0. Theta input file

You need to provide at least two input file, one for electron (boosted_semileptonic_electron.root) and the other for muons (boosted_semileptonic_muons.root).


1. Creating a combined lepton file (boosted_semileptonic_lepton.root)

hadd boosted_semileptonic_lepton.root boosted_semileptonic_electron.root boosted_semileptonic_muons.root

2. Running mass point interpolation

2.1 Compiling interpolation macro

make morph_zpw1p
make morph_zpw10p
make morph_rsg

2.2 Executing the interpolation

nohup ./morph_zpw1p &> log &
nohup ./morph_zpw10p &> log &
nohup ./morph_rsg &> log &

2.3 Merging the interpolated signals into input theta files

hadd boosted_semileptonic_electron_interpolated.root boosted_semileptonic_electron.root el_* 
hadd boosted_semileptonic_muon_interpolated.root boosted_semileptonic_muon.root mu_*
hadd boosted_semileptonic_lepton_interpolated.root boosted_semileptonic_lepton.root el_* mu_*


3. Rebinning the input histograms

./histogram_rebinning.py

Note 1: the rebinning scrip generate basic control plot of data overlay with background expectation.
Note 2: the program should generate three new files

boosted_semileptonic_electron_rebinned.root
boosted_semileptonic_muon_rebinned.root
boosted_semileptonic_lepton_rebinned.root

4. Summaries

theta_driver preprocess --model 'model: type = narrow_resonances_lepton' --workdir summary_narrow_resonances_lepton --analysis summary *_rebinned.root
theta_driver preprocess --model 'model: type = wide_resonances_lepton' --workdir summary_wide_resonances_lepton --analysis summary *_rebinned.root
theta_driver preprocess --model 'model: type = rsg_resonances_lepton' --workdir summary_rsg_resonances_lepton --analysis summary *_rebinned.root

theta_driver tartheta --workdir summary_narrow_resonances_lepton
theta_driver tartheta --workdir summary_wide_resonances_lepton
theta_driver tartheta --workdir summary_rsg_resonances_lepton


5. MLE limtis 

theta_driver preprocess --model 'model: type = narrow_resonances_lepton' --workdir mle --analysis mle *_rebinned.root


6. Computing the bayesian limits

theta_driver preprocess --model 'model: type = narrow_resonances_muon' --workdir narrow_resonances_muon --analysis 'bayesian: mcmc_iterations = 160000' *_rebinned.root
theta_driver preprocess --model 'model: type = wide_resonances_muon' --workdir wide_resonances_muon --analysis 'bayesian: mcmc_iterations = 160000' *_rebinned.root
theta_driver preprocess --model 'model: type = rsg_resonances_muon' --workdir rsg_resonances_muon --analysis 'bayesian: mcmc_iterations = 160000' *_rebinned.root

theta_driver preprocess --model 'model: type = narrow_resonances_electron' --workdir narrow_resonances_electron --analysis 'bayesian: mcmc_iterations = 160000' *_rebinned.root
theta_driver preprocess --model 'model: type = wide_resonances_electron' --workdir wide_resonances_electron --analysis 'bayesian: mcmc_iterations = 160000' *_rebinned.root
theta_driver preprocess --model 'model: type = rsg_resonances_electron' --workdir rsg_resonances_electron --analysis 'bayesian: mcmc_iterations = 160000' *_rebinned.root

theta_driver preprocess --model 'model: type = narrow_resonances_lepton' --workdir narrow_resonances_lepton --analysis 'bayesian: mcmc_iterations = 160000' *_rebinned.root
theta_driver preprocess --model 'model: type = wide_resonances_lepton' --workdir wide_resonances_lepton --analysis 'bayesian: mcmc_iterations = 160000' *_rebinned.root
theta_driver preprocess --model 'model: type = rsg_resonances_lepton' --workdir rsg_resonances_lepton --analysis 'bayesian: mcmc_iterations = 160000' *_rebinned.root

theta_driver submit --workdir narrow_resonances_muon
theta_driver submit --workdir wide_resonances_muon
theta_driver submit --workdir rsg_resonances_muon

theta_driver submit --workdir narrow_resonances_electron
theta_driver submit --workdir wide_resonances_electron
theta_driver submit --workdir rsg_resonances_electron

theta_driver submit --workdir narrow_resonances_lepton
theta_driver submit --workdir wide_resonances_lepton
theta_driver submit --workdir rsg_resonances_lepton

