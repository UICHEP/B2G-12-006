#! /usr/bin/env python

scale = 0.93
#histgen = '/Chi2_BTag/M_ttbar_gen'
#histrec = '/Chi2_BTag/M_ttbar_rec'
#thetaname = 'el_1btag_mttbar__ttbar'

histgen = '/Chi2_NoBTag/M_ttbar_gen'
histrec = '/Chi2_NoBTag/M_ttbar_rec'
thetaname = 'el_0btag_mttbar__ttbar'

import sys
sys.argv.append('-b')

import ROOT
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(000000000)
ROOT.gStyle.SetOptTitle(0)

file0 = ROOT.TFile('ZprimePostSelectionCycle.MC.TTbar_scaleup.root')
file1 = ROOT.TFile('ZprimePostSelectionCycle.MC.TTbar_700to1000_scaleup.root')
file2 = ROOT.TFile('ZprimePostSelectionCycle.MC.TTbar_1000toInf_scaleup.root')
file3 = ROOT.TFile('ZprimePostSelectionCycle.MC.TTbar_0to700_scaleup.root')

h0 = file0.Get(histgen).Clone()
h1 = file1.Get(histgen).Clone()
h2 = file2.Get(histgen).Clone()
h3 = file3.Get(histgen).Clone()

scaleup = (h1.Integral(15,9999)+h2.Integral(15,9999))/h0.Integral(15,9999)
h3.Scale(scaleup)

h1.SetLineColor(ROOT.kRed)
h2.SetLineColor(ROOT.kRed)
h3.SetLineColor(ROOT.kRed)
h3.SetLineStyle(2)

canvas = ROOT.TCanvas()
canvas.SetLogy()

h3.Draw('hist');
h1.Draw('histsame');
h2.Draw('histsame');

file4 = ROOT.TFile('ZprimePostSelectionCycle.MC.TTbar_scaledown.root')
file5 = ROOT.TFile('ZprimePostSelectionCycle.MC.TTbar_700to1000_scaledown.root')
file6 = ROOT.TFile('ZprimePostSelectionCycle.MC.TTbar_1000toInf_scaledown.root')
file7 = ROOT.TFile('ZprimePostSelectionCycle.MC.TTbar_0to700_scaledown.root')

h4 = file4.Get(histgen).Clone()
h5 = file5.Get(histgen).Clone()
h6 = file6.Get(histgen).Clone()
h7 = file7.Get(histgen).Clone()

scaledown = (h5.Integral(15,9999)+h6.Integral(15,9999))/h4.Integral(15,9999)
h7.Scale(scaledown)

h5.SetLineColor(ROOT.kBlue)
h6.SetLineColor(ROOT.kBlue)
h7.SetLineColor(ROOT.kBlue)
h7.SetLineStyle(2)

h7.Draw('histsame')
h5.Draw('histsame')
h6.Draw('histsame')

file8 = ROOT.TFile('ZprimePostSelectionCycle.MC.TTbar_700to1000.root')
file9 = ROOT.TFile('ZprimePostSelectionCycle.MC.TTbar_1000toInf.root')
file10 = ROOT.TFile('ZprimePostSelectionCycle.MC.TTbar_0to700.root')

h8 = file8.Get(histgen)
h9 = file9.Get(histgen)
h10 = file10.Get(histgen)

h8.Draw('histsame')
h9.Draw('histsame')
h10.Draw('histsame')

print scaleup,scaledown
canvas.SaveAs('ttbar-scale-gen.png')

hup = file3.Get(histrec).Clone()
hup.SetName(thetaname+'__scale__plus')
hup.Scale(scaleup)
hup.Add(file1.Get(histrec).Clone())
hup.Add(file2.Get(histrec).Clone())
hup.Scale(scale)

hdown = file7.Get(histrec).Clone()
hdown.SetName(thetaname+'__scale__minus')
hdown.Scale(scaleup)
hdown.Add(file5.Get(histrec).Clone())
hdown.Add(file6.Get(histrec).Clone())
hdown.Scale(scale)

output = ROOT.TFile('theta-input.root', 'UPDATE')
hup.Write()
hdown.Write()
