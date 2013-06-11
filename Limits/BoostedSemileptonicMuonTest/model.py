
### Filter definitions ###

def narrow_resonances(hname):
    # Accept anything that there is neither of the signals
    if 'rsg' not in hname and 'zp' not in hname :
        return True
    # Reject RS gluons as signal
    elif 'rsg' in hname:
        return False
    # Process signal name
    pname = hname.split('__')[1]
    # reject wide reonances
    if 'w10p' in pname:
        return False
    # Accept only a few mass points (no interpolation)
    mass = pname.split('w')[0].split('zp')[1]
    mass_whitelist = ['500', '750','1000','1250','1500','2000','3000','4000']
    return mass in mass_whitelist


def wide_resonances(hname):
    # Accept anything that there is neither of the signals
    if 'rsg' not in hname and 'zp' not in hname :
        return True
    # Reject RS gluons as signal
    elif 'rsg' in hname:
        return False
    # Process signal name
    pname = hname.split('__')[1]
    # reject wide reonances
    if 'w1p' in pname:
        return False
    # Accept only a few mass points (no interpolation)
    mass = pname.split('w')[0].split('zp')[1]
    mass_whitelist = ['500', '750','1000','1250','1500','2000','3000','4000']
    return mass in mass_whitelist


def build_boosted_semileptonic_model(files, filter, signal, mcstat):
    """ Semileptonic high mass model"""
    model = build_model_from_rootfile(files, filter, include_mc_uncertainties = mcstat)
    model.fill_histogram_zerobins()
    model.set_signal_processes(signal)
    for p in model.processes:
        model.add_lognormal_uncertainty('lumi', math.log(1.06), p)
    
    model.add_lognormal_uncertainty('zj_rate', math.log(2.0), 'zlight')
    model.add_lognormal_uncertainty('wj_rate', math.log(2.0), 'wlight')
    model.add_lognormal_uncertainty('ttbar_rate', math.log(1.5), 'ttbar')
    model.add_lognormal_uncertainty('st_rate', math.log(1.5), 'singletop')
    model.add_lognormal_uncertainty('diboson_rate', math.log(1.5), 'diboson')    

    for obs in ('mu_0btag_mttbar', 'mu_1btag_mttbar'):
        for proc in model.processes:
            model.add_lognormal_uncertainty('mu_eff', math.log(1.05), proc, obs)
    
    return model


import exceptions


def build_model(type, jet1 = None, chi2 = None, mcstat = True):

    model = None

    if type == 'narrow_resonances':

        if jet1:
            model = build_boosted_semileptonic_model(
                ['boosted_semileptonic_muon_jet1_%d_rebinned.root' % jet1],
                narrow_resonances,
                'zp*',
                mcstat
            )
        elif chi2:
            model = build_boosted_semileptonic_model(
                ['boosted_semileptonic_muon_chi2_%s_rebinned.root' % chi2],
                narrow_resonances,
                'zp*',
                mcstat
            )
    
    elif type == 'wide_resonances':

        if jet1:
            model = build_boosted_semileptonic_model(
                ['boosted_semileptonic_muon_jet1_%d_rebinned.root' % jet1],
                wide_resonances,
                'zp*',
                mcstat
            )
        elif chi2:
            model = build_boosted_semileptonic_model(
                ['boosted_semileptonic_muon_chi2_%s_rebinned.root' % chi2],
                wide_resonances,
                'zp*',
                mcstat
            )        

    else:

        raise exceptions.ValueError('Type %s is undefined' % type)

    for p in model.distribution.get_parameters():
        d = model.distribution.get_distribution(p)
        if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
            model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])

    return model
