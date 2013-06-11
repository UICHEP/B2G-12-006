#! /usr/bin/env python

import sys
sys.argv.append('-b')

import ROOT
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(000000000)
ROOT.gStyle.SetOptTitle(0)

from ROOT import TCanvas, TFile, TH1, THStack, TLegend

class hinfo:
  def __init__(self, name):
    fields = name.split('__')
    self.channel = fields[0]
    self.process = fields[1]
    self.systematic = None
    self.shift = None 
    if len(fields) > 2:
      self.systematic = fields[2]
      self.shift = fields[3]


def name(channel, process, systematic = None, shift = None):
  if not systematic:
    return '__'.join([channel, process])
  return '__'.join([channel, process, systematic, shift])


def merge(old,new):
  if not old:
    old = new.Clone()
  else:
    old.Add(new)
  return old


import array, math


def binFile(ratio, filename, xtitle, systematics, backgrounds): 

    file = TFile(filename)
    keys = file.GetListOfKeys()

    h_bkg = {}
    h_bkg_plus = {}
    h_bkg_minus = {}

    # load all the background and data histograms
    for key in keys:
        key = key.GetName()
        info = hinfo(key)
        if not info.systematic:
            if info.process in backgrounds:
                if info.channel in h_bkg:
                    h_bkg[info.channel] = merge(h_bkg[info.channel], file.Get(key).Clone())
                else:
                    h_bkg[info.channel] = file.Get(key).Clone()
        elif info.systematic in systematics and info.shift == 'plus':
            if info.process in backgrounds:
                systematic = info.channel + ":" + info.systematic
                if systematic in h_bkg_plus:
                    h_bkg_plus[systematic] = merge(h_bkg_plus[systematic], file.Get(key).Clone())
                else:
                    h_bkg_plus[systematic] = file.Get(key).Clone()
        elif info.systematic in systematics and info.shift == 'minus':
            if info.process in backgrounds:
                systematic = info.channel + ":" + info.systematic
                if systematic in h_bkg_minus:
                    h_bkg_minus[systematic] = merge(h_bkg_minus[systematic], file.Get(key).Clone())
                else:
                    h_bkg_minus[systematic] = file.Get(key).Clone()

    canvas = TCanvas()
    #if not ratio: canvas.SetLogy()

    keys = file.GetListOfKeys()

    # print all the histograms for all the channel
    for sys in h_bkg_plus:
    
            key = sys.split(':')[0]   

            pad = canvas.cd(1)
            pad.SetLeftMargin(0.15)
            pad.SetBottomMargin(0.15)

            nom = h_bkg[key].Clone()
            plus = h_bkg_plus[sys]
            minus = h_bkg_minus[sys]       

            if ratio:
                nom.Divide(h_bkg[key])
                plus.Divide(h_bkg[key])
                minus.Divide(h_bkg[key])

            maxnom = nom.GetBinContent(nom.GetMaximumBin())
            maxplus = plus.GetBinContent(plus.GetMaximumBin())
            maxminus = minus.GetBinContent(minus.GetMaximumBin()) 

            minnom = nom.GetBinContent(nom.GetMinimumBin())
            minplus = plus.GetBinContent(plus.GetMinimumBin())
            minminus = minus.GetBinContent(minus.GetMinimumBin())  

            maxs = [maxnom, maxplus, maxminus]
            mins = [minnom, minplus, minminus]

            nom.GetYaxis().SetRangeUser(0,max(maxs)*1.1)

            if ratio:
                ymin = 1-1.8*(1-min(mins))
                if ymin < 0: ymin = 0
                nom.GetYaxis().SetRangeUser(ymin,1+1.8*(max(maxs)-1))

            nom.GetYaxis().SetLabelSize(0.05)
            nom.GetYaxis().SetTitleSize(0.05)
            nom.GetYaxis().SetTitle('event yield')
            if ratio: nom.GetYaxis().SetTitle('ratio')
            nom.GetXaxis().SetLabelSize(0.05)
            nom.GetXaxis().SetTitleSize(0.05)
            nom.GetXaxis().SetTitle(xtitle)

            nom.SetLineStyle(1)
            nom.SetLineWidth(2)
            nom.SetFillColor(0)
            nom.SetLineColor(ROOT.kBlack)
            plus.SetLineStyle(1)
            plus.SetLineWidth(2)
            plus.SetFillColor(0)
            plus.SetLineColor(ROOT.kRed)
            minus.SetLineStyle(1)
            minus.SetLineWidth(2)
            minus.SetFillColor(0)
            minus.SetLineColor(ROOT.kBlue)

            nom.Draw('hist')
            plus.Draw('histsame')
            minus.Draw('histsame')
            nom.Draw('histsame')

            legend = TLegend(.67, .74, .89, .88)
            legend.SetMargin(0.12);
            legend.SetTextSize(0.03);
            legend.SetFillColor(10);
            legend.SetBorderSize(0);
            legend.AddEntry(plus, "%s plus" % sys.split(':')[1], "lp")
            legend.AddEntry(nom, "nominal", "lp")
            legend.AddEntry(minus, "%s minus" % sys.split(':')[1], "lp")
            legend.Draw()

            labelcms = TLegend(.15, .91, 1, .96)
            labelcms.SetTextSize(0.04)
            labelcms.SetMargin(0.12);
            labelcms.SetFillColor(10);
            labelcms.SetBorderSize(0);
            labelcms.SetHeader('CMS Preliminary #sqrt{s} = 8 TeV')
            labelcms.Draw()

            labellumi = TLegend(.73, .91, 1, .96)
            labellumi.SetTextSize(0.04)
            labellumi.SetMargin(0.12);
            labellumi.SetFillColor(10);
            labellumi.SetBorderSize(0);
            labellumi.SetHeader('L = 19.6 fb^{-1}')
            labellumi.Draw()

            labellumi2 = TLegend(.67, .66, .89, .75)
            labellumi2.SetTextSize(0.03)
            labellumi2.SetMargin(0.12);
            labellumi2.SetFillColor(10);
            labellumi2.SetBorderSize(0);
            labellumi2.SetHeader(key)
            labellumi2.Draw()

            if ratio:
                canvas.SaveAs('h_'+filename.split('.')[0]+'_'+sys.replace(':','_')+'_ratio.pdf')
            else:
                canvas.SaveAs('h_'+filename.split('.')[0]+'_'+sys.replace(':','_')+'.pdf')

binFile(False, 'boosted_semileptonic_lepton_rebinned.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['bmistag', 'btageff', 'jec', 'jer', 'pileup', 'pdf'], ['ttbar', 'wlight', 'wc', 'wb', 'zlight', 'singletop', 'diboson'])
binFile(True, 'boosted_semileptonic_lepton_rebinned.root', 'M_{t#bar{t}} [GeV/c^{2}]',['bmistag', 'btageff', 'jec', 'jer', 'pileup', 'pdf'],['ttbar', 'wlight', 'wc', 'wb', 'zlight', 'singletop', 'diboson'])

binFile(False, 'boosted_semileptonic_lepton_rebinned.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['scale_ttbar'], ['ttbar'])
binFile(True, 'boosted_semileptonic_lepton_rebinned.root', 'M_{t#bar{t}} [GeV/c^{2}]',['scale_ttbar'], ['ttbar'])

binFile(False, 'boosted_semileptonic_lepton_rebinned.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['scale_vjets'], ['wlight','zlight'])
binFile(True, 'boosted_semileptonic_lepton_rebinned.root', 'M_{t#bar{t}} [GeV/c^{2}]',['scale_vjets'], ['wlight','zlight'])

binFile(False, 'boosted_semileptonic_lepton_rebinned.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['matching_vjets'], ['wlight','zlight'])
binFile(True, 'boosted_semileptonic_lepton_rebinned.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['matching_vjets'], ['wlight','zlight'])


