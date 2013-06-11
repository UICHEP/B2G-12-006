///////////////////////////////////////////////////////////////////////////////////////////
//
// RooStats macro
// 2009/11 - Jan Steggemann
//
// Prepare a workspace (stored in a ROOT file) containing histogram-based models,
// data and other objects needed to run statistical classes in RooStats.
//
///////////////////////////////////////////////////////////////////////////////////////////


#include "TFile.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TROOT.h"

#include "RooIntegralMorph.h"
#include "RooMomentMorph.h"
#include "RooBinning.h"
#include "RooRealVar.h"
#include "RooDataHist.h"
#include "RooHistPdf.h"

#include <cmath>
#include <iostream>
#include <sstream>

using namespace RooFit;

TString id;

// IMPORTANT: RooFit does not clean up everything correctly and previous calculations can influence future
// results. Therefore, call this function with a different value for evaluateMass each time within one program
// run or change the global 'id' if you want to call it again with the same mass.
TH1* createInterpolatedHist(TH1* hlower, TH1* hupper, double evaluateMass, double lowerMass, double upperMass, const TString& newName, bool propagateErrors = false)
{
    // Interpolating histogram values

    cout << "interpolating values" << lowerMass << ", " << upperMass << "   to   " << evaluateMass << endl;
    double binning[hlower->GetNbinsX()+1];
    for (int i = 1; i <= hlower->GetNbinsX() + 1; ++i)
    {
        binning[i-1] = std::floor(hlower->GetBinLowEdge(i)+0.5); // should also work for overflow
    }

    RooBinning rooBinning(hlower->GetNbinsX(), binning);

    RooRealVar mttbar("mttbar", "mttbar", evaluateMass, "GeV");
    mttbar.setBinning(rooBinning);

    TString h_1_name = hlower->GetName();
    h_1_name += evaluateMass;
    TString pdf_1_name = hlower->GetName();
    pdf_1_name += "pdf1";
    pdf_1_name += evaluateMass;
    pdf_1_name += id;

    RooDataHist h_1(h_1_name, h_1_name, mttbar, Import(*hlower));
    RooHistPdf pdf_1(pdf_1_name, pdf_1_name, mttbar, h_1);

    TString h_2_name = hupper->GetName();
    h_2_name += evaluateMass;
    TString pdf_2_name = hupper->GetName();
    pdf_2_name += "pdf2";
    pdf_2_name += evaluateMass;
    pdf_2_name += id;
    RooDataHist h_2(h_2_name, h_2_name, mttbar, Import(*hupper));
    RooHistPdf pdf_2(pdf_2_name, pdf_2_name, mttbar, h_2);

    RooArgList massPdfs;
    massPdfs.add(pdf_1);
    massPdfs.add(pdf_2);

    RooRealVar mzprime("mzprime", "mzprime", evaluateMass, lowerMass, upperMass, "GeV");

    TVectorD massPoints;
    massPoints.ResizeTo(2);
    massPoints[0] = lowerMass;
    massPoints[1] = upperMass;

    RooMomentMorph morph("morph_value", "morph_value", mzprime, mttbar, massPdfs, massPoints);

    TH1F* interpolHist = new TH1F(newName, newName, hlower->GetNbinsX(), binning);

    // The RooFit binning convention differs from the ROOT binning convention
    for (Int_t i = 0; i < rooBinning.numBins(); ++i)
    {
        Double_t binCenter = rooBinning.binCenter(i);
        mttbar.setVal(binCenter);
        interpolHist->SetBinContent(i+1, morph.getVal());
    }

    // Interpolating histogram errors
    if (propagateErrors)
    {


        h_1_name = hlower->GetName();
        h_1_name += evaluateMass;
        pdf_1_name = hlower->GetName();
        pdf_1_name += "pdferror1";
        pdf_1_name += evaluateMass;
        pdf_1_name += id;

        TH1* elower = (TH1*) hlower->Clone();
        for (int i = 1; i <= elower->GetNbinsX(); ++i)
            elower->SetBinContent(i, elower->GetBinError(i));

        RooDataHist h_1_error(h_1_name, h_1_name, mttbar, Import(*elower));
        RooHistPdf pdf_1_error(pdf_1_name, pdf_1_name, mttbar, h_1_error);

        h_2_name = hupper->GetName();
        h_2_name += evaluateMass;
        pdf_2_name = hupper->GetName();
        pdf_2_name += "pdferror2";
        pdf_2_name += evaluateMass;
        pdf_2_name += id;

        TH1* eupper = (TH1*) hupper->Clone();
        for (int i = 1; i <= eupper->GetNbinsX(); ++i)
            eupper->SetBinContent(i, eupper->GetBinError(i));

        RooDataHist h_2_error(h_2_name, h_2_name, mttbar, Import(*eupper));
        RooHistPdf pdf_2_error(pdf_2_name, pdf_2_name, mttbar, h_2_error);

        RooArgList massErrorPdfs;
        massErrorPdfs.add(pdf_1_error);
        massErrorPdfs.add(pdf_2_error);

        RooMomentMorph morphError("morph_error", "morph_error", mzprime, mttbar, massErrorPdfs, massPoints);

        for (Int_t i = 0; i < rooBinning.numBins(); ++i)
        {
            Double_t binCenter = rooBinning.binCenter(i);
            mttbar.setVal(binCenter);
            interpolHist->SetBinError(i+1, morphError.getVal());
        }

    }

    interpolHist->SetDirectory(0);
    return interpolHist;
}

/*TH1* createVerticallyInterpolatedHist(TH1* hlower, TH1* hupper, double evaluateMass, double lowerMass, double upperMass, const TString& newName) {
    assert(hlower->GetNbinsX() == hupper->GetNbinsX());
    TH1 * result = new TH1D(newName, newName, hlower->GetNbinsX(), hlower->GetXaxis()->GetXmin(), hlower->GetXaxis()->GetXmax());
    result->SetDirectory(0);
    double lambda = (evaluateMass - lowerMass) / (upperMass - lowerMass);
    for(int ibin=1; ibin<=hlower->GetNbinsX(); ++ibin){
        double new_bincontent = hlower->GetBinContent(ibin) + lambda * (hupper->GetBinContent(ibin) - hlower->GetBinContent(ibin));
        result->SetBinContent(ibin, new_bincontent);
    }
    return result;
}*/

TH1* load(const string & filename, const string & hname)
{
    TFile f(filename.c_str(), "read");
    if(f.IsZombie())
    {
        cerr << "could not open file " << filename << endl;
        exit(1);
    }
    TH1* result = (TH1*)f.Get(hname.c_str());
    if(!result)
    {
        cout << "Did not find histo " << hname << " in file " << filename << endl;
        return 0;
    }
    result = (TH1*)result->Clone();
    result->SetDirectory(0);
    return result;
}

template<typename T>
void interpolate(TDirectory * dir_out, const map<int, TH1*> & zpmass_to_histo, const TString & pattern, const T & interpolator, bool interpolateErrors = false)
{
    int zp_lowest = zpmass_to_histo.begin()->first;
    int zp_highest = zpmass_to_histo.rbegin()->first;
    map<int, TH1*> zpmass_to_histo_interp;
    assert(pattern.First("X")!=kNPOS);
    for(int zpmass = zp_lowest; zpmass <= zp_highest; zpmass += 100)
    {
        stringstream zpmass_ss;
        zpmass_ss << zpmass;
        TString name = pattern;
        name.ReplaceAll("X", zpmass_ss.str().c_str());
        map<int, TH1*>::const_iterator it = zpmass_to_histo.upper_bound(zpmass);
        assert(it!=zpmass_to_histo.begin());
        --it;
        if(zpmass == it->first)
        {
            continue;
        }
        else
        {
            map<int, TH1*>::const_iterator it2 = it;
            ++it2;
            assert(it2!=zpmass_to_histo.end());
            TH1 * histo = interpolator(it->second, it2->second, zpmass, it->first, it2->first, name, interpolateErrors);
            //re-normalize: interpolate linearly:
            double delta_x = it2->first - it->first;
            double delta_y = it2->second->Integral() - it->second->Integral();
            double new_norm = (delta_y / delta_x) * (zpmass - it->first) + it->second->Integral();
            histo->Scale(new_norm / histo->Integral());
            histo->SetDirectory(dir_out);
        }
    }
}

void interpolate(const string & infilename, const string & channel)
{
    TFile f((channel + "_zpXw10p_interpolated.root").c_str(), "recreate");
    map<int, TH1*> zpmass_to_histo;
    zpmass_to_histo[500] = load(infilename, channel + "__zp500w10p");
    zpmass_to_histo[750] = load(infilename, channel + "__zp750w10p");
    zpmass_to_histo[1000] = load(infilename, channel + "__zp1000w10p");
    zpmass_to_histo[1250] = load(infilename, channel + "__zp1250w10p");
    zpmass_to_histo[1500] = load(infilename, channel + "__zp1500w10p");
    zpmass_to_histo[2000] = load(infilename, channel + "__zp2000w10p");
    zpmass_to_histo[3000] = load(infilename, channel + "__zp3000w10p");
    interpolate(&f, zpmass_to_histo, channel + "__zpXw10p", createInterpolatedHist, true);

    //jes and jer templates:
    vector<string> syst;
    syst.push_back("bmistag");
    syst.push_back("btageff");
    syst.push_back("jec");
    syst.push_back("jer");
    syst.push_back("muonid");
    syst.push_back("pdf");
    syst.push_back("pileup");
    for(size_t isyst=0; isyst<syst.size(); ++isyst)
    {
        for(int ipm=0; ipm<2; ipm++)
        {
            string dir = ipm==0?"plus":"minus";
            zpmass_to_histo[500] = load(infilename, channel + "__zp500w10p__" + syst[isyst] + "__" + dir);
            if(!zpmass_to_histo[500]) continue;
            zpmass_to_histo[750] = load(infilename, channel + "__zp750w10p__" + syst[isyst] + "__" + dir);
            zpmass_to_histo[1000] = load(infilename, channel + "__zp1000w10p__" + syst[isyst] + "__" + dir);
            zpmass_to_histo[1250] = load(infilename, channel + "__zp1250w10p__" + syst[isyst] + "__" + dir);
            zpmass_to_histo[1500] = load(infilename, channel + "__zp1500w10p__" + syst[isyst] + "__" + dir);
            zpmass_to_histo[2000] = load(infilename, channel + "__zp2000w10p__" + syst[isyst] + "__" + dir);
            zpmass_to_histo[3000] = load(infilename, channel + "__zp3000w10p__" + syst[isyst] + "__" + dir);
            interpolate(&f, zpmass_to_histo, channel + "__zpXw10p__" + syst[isyst] + "__" + dir, createInterpolatedHist);
        }
    }
    f.cd();
    f.Write();
    f.Close();
}

int main()
{
    id = "el_0btag";
    interpolate("boosted_semileptonic_lepton.root", "el_0btag_mttbar");
    id = "el_1btag";
    interpolate("boosted_semileptonic_lepton.root", "el_1btag_mttbar");
    id = "mu_0btag";
    interpolate("boosted_semileptonic_lepton.root", "mu_0btag_mttbar");
    id = "mu_1btag";
    interpolate("boosted_semileptonic_lepton.root", "mu_1btag_mttbar");
}

