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


import math


def computeBin(histogram, rerror):
    lowindex = 0   
    value = 0.0
    error = 0.0
    for i in range(1,histogram.GetNbinsX()+1):
        value = value + histogram.GetBinContent(i)
        error = math.sqrt(error**2+histogram.GetBinError(i)**2)
        ratio = 1.0
        if value != 0: ratio = error/value
        if ratio < rerror:
            lowindex = i
            break
    
    highindex = []
    start = histogram.GetNbinsX()+1
    for j in range(histogram.GetNbinsX()):
        value = 0.0
        error = 0.0
        for i in range(start, 0, -1):
            value = value + histogram.GetBinContent(i)
            error = math.sqrt(error**2+histogram.GetBinError(i)**2)
            ratio = 1.0
            if value != 0: ratio = error/value
            if ratio < rerror:
                highindex.append(i)
                start = i-1
                break
        if start == lowindex:
            break
            
    highindex = sorted(highindex)
    binning = [histogram.GetBinLowEdge(0), histogram.GetBinLowEdge(lowindex)+histogram.GetBinWidth(lowindex)]
    for i in highindex[1:]:
        binning.append(histogram.GetBinLowEdge(i))
    binning.append(histogram.GetBinLowEdge(histogram.GetNbinsX())+histogram.GetBinWidth(histogram.GetNbinsX()))
    print binning
    return binning   

import array

def binFile(rerror, filename, xtitle, backgrounds): 

    file = TFile(filename)
    keys = file.GetListOfKeys()

    h_bkg = {}
    h_data = {}

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
            elif info.process == 'data':
                if info.channel in h_data:
                    h_data[info.channel] = merge(h_data[info.channel], file.Get(key).Clone())
                else:
                    h_data[info.channel] = file.Get(key).Clone()

    canvas = TCanvas()
    canvas.SetLogy()

    keys = file.GetListOfKeys()

    output = TFile(filename.split('.')[0]+'_rebinned.root', 'RECREATE')

    # print all the histograms for all the channels
    for key in h_bkg:

        binning = array.array('d', computeBin(h_bkg[key], rerror))
        h_bkg[key] = h_bkg[key].Rebin(len(binning)-1, h_bkg[key].GetName(), binning)
        h_data[key] = h_data[key].Rebin(len(binning)-1, h_data[key].GetName(), binning)
       
        h_bkg[key].SetLineColor(ROOT.kRed+1)
        h_bkg[key].SetFillColor(ROOT.kRed+1)
        h_data[key].SetLineColor(ROOT.kBlack)  
        h_data[key].SetMarkerStyle(20)

        pad = canvas.cd(1)
        pad.SetLeftMargin(0.15)
        pad.SetBottomMargin(0.15)
        
        maxs = [h_data[key].GetMaximum(), h_bkg[key].GetMaximum()]

        h_data[key].GetYaxis().SetRangeUser(h_bkg[key].GetMinimum()*0.5,max(maxs)*1.8)

        h_data[key].GetYaxis().SetLabelSize(0.05)
        h_data[key].GetYaxis().SetTitleSize(0.05)
        h_data[key].GetYaxis().SetTitle('event yield')
        h_data[key].GetXaxis().SetLabelSize(0.05)
        h_data[key].GetXaxis().SetTitleSize(0.05)
        h_data[key].GetXaxis().SetTitle(xtitle)

        h_data[key].Draw('e')
        h_bkg[key].Draw('samehist')
        h_data[key].Draw('samee')

        legend = TLegend(.67, .78, .89, .88)
        legend.SetMargin(0.12);
        legend.SetTextSize(0.03);
        legend.SetFillColor(10);
        legend.SetBorderSize(0);
        legend.AddEntry(h_bkg[key], "Background", "f")
        legend.AddEntry(h_data[key], "CMS Data 2012", "lp")
        legend.Draw()

        labelcms = TLegend(.15, .91, 1, .96)
        labelcms.SetTextSize(0.04)
        labelcms.SetMargin(0.12);
        labelcms.SetFillColor(10);
        labelcms.SetBorderSize(0);
        labelcms.SetHeader('CMS Preliminary #sqrt{s} = 8 TeV')
        labelcms.Draw()

        labellumi = TLegend(.70, .91, 1, .96)
        labellumi.SetTextSize(0.04)
        labellumi.SetMargin(0.12);
        labellumi.SetFillColor(10);
        labellumi.SetBorderSize(0);
        labellumi.SetHeader('L = 11.2 fb^{-1}')
        labellumi.Draw()

        labellumi2 = TLegend(.67, .70, .89, .75)
        labellumi2.SetTextSize(0.03)
        labellumi2.SetMargin(0.12);
        labellumi2.SetFillColor(10);
        labellumi2.SetBorderSize(0);
        labellumi2.SetHeader(key)
        labellumi2.Draw()

        canvas.SaveAs('h_'+filename.split('.')[0]+'_'+key+'.pdf')

        for hkey in keys:
            hkey = hkey.GetName()
            info = hinfo(hkey)
            if info.channel == key:
                histogram = file.Get(hkey).Clone()
                # Hack to fix the data lowercase names
                if 'data' in histogram.GetName():
                    histogram.SetName(histogram.GetName().replace('data','DATA'))
                histogram = histogram.Rebin(len(binning)-1, histogram.GetName(), binning)
                output.cd()
                histogram.Write()


binFile(0.3, 'boosted_semileptonic_muon_jet1_150.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])
binFile(0.3, 'boosted_semileptonic_muon_jet1_200.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])
binFile(0.3, 'boosted_semileptonic_muon_jet1_250.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])
binFile(0.3, 'boosted_semileptonic_muon_chi2_2.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])
binFile(0.3, 'boosted_semileptonic_muon_chi2_5.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])
binFile(0.3, 'boosted_semileptonic_muon_chi2_8.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])
binFile(0.3, 'boosted_semileptonic_muon_chi2_10.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])
binFile(0.3, 'boosted_semileptonic_muon_chi2_15.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])
binFile(0.3, 'boosted_semileptonic_muon_chi2_20.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])
binFile(0.3, 'boosted_semileptonic_muon_chi2_50.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])
binFile(0.3, 'boosted_semileptonic_muon_chi2_100.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])
binFile(0.3, 'boosted_semileptonic_muon_chi2_Inf.root', 'M_{t#bar{t}} [GeV/c^{2}]', ['ttbar', 'wlight', 'zlight', 'singletop', 'diboson'])

