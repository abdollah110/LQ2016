#include <iostream>

#include <TH1F.h>
#include <TFile.h>
#include <TROOT.h>
#include <TString.h>
#include <TSystem.h>
#include <Rtypes.h>

#include <TMath.h>
#include <TAxis.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TAttLine.h>
#include <TPaveText.h>
#include <THStack.h>
#include <algorithm>    // std::max
#include "interface/HttStyles.h"
#include "interface/HttStyles.cc"




void draw_prefit_Sample(std::string inputF, std::string channel, std::string xTitle, std::string nameHisto) {
    
    //    gStyle->SetOptStat(0);
    
    
    SetStyle();
    //    InitSubPad
    TCanvas *canv = MakeCanvas("canv", "histograms", 600, 600);
    float SIGNAL_SCALE = 10;
    bool scaled = true;
    bool log = true;
//    canv->SetLogy();
    TFile* input = new TFile(inputF.c_str());
    const char* dataset;
    

    THStack hs("hs", "");
    
    TH1F* QCD = (TH1F*) input->Get((channel + "QCD").c_str());
    InitHist(QCD, "", "", TColor::GetColor(408, 106, 154), 1001);
    cout << "QCD= " << QCD->Integral() << "\n";
    hs.Add(QCD);
    
    TH1F* W = (TH1F*) input->Get((channel + "W").c_str());
    InitHist(W, "", "", TColor::GetColor(200, 2, 285), 1001);
    cout << "W= " << W->Integral() << "\n";
    
    //    TH1F* ZJ = (TH1F*) input->Get((channel + "ZJ").c_str());
    //    //    InitHist(ZJ, "", "", TColor::GetColor(100, 182, 232), 1001);
    //    cout << "ZJ= " << ZJ->Integral() << "\n";
    //    W->Add(ZJ);
    //
    //    TH1F* ZL = (TH1F*) input->Get((channel + "ZL").c_str());
    //    //    InitHist(ZL, "", "", TColor::GetColor(100, 182, 232), 1001);
    //    W->Add(ZL);
    //    cout << "ZL= " << ZL->Integral() << "\n";
    //
    //
    //    TH1F* VV = (TH1F*) input->Get((channel + "VV").c_str());
    //    //    InitHist(VV, "", "", TColor::GetColor(100, 182, 232), 1001);
    //    W->Add(VV);
    
    hs.Add(W);
    ////    TH1F* ZLL = (TH1F*) input->Get((channel +"ZLL");
    //    InitHist(ttbar, "", "", TColor::GetColor(155, 152, 204), 1001);
    
    TH1F* TT = (TH1F*) input->Get((channel + "TT").c_str());
    InitHist(TT, "", "", TColor::GetColor(208, 376, 124), 1001);
    hs.Add(TT);
    cout << "TT= " << TT->Integral() << "\n";
    
    TH1F* ZTT = (TH1F*) input->Get((channel + "ZTT").c_str());
    InitHist(ZTT, "", "", TColor::GetColor(108, 226, 354), 1001);
    cout << "ZTT= " << ZTT->Integral() << "\n";
    
    //    TH1F* ZTTLow = (TH1F*) input->Get((channel + "ZTT_lowMass").c_str());
    //    InitHist(ZTTLow, "", "", TColor::GetColor(248, 206, 104), 1001);
    //    cout << "ZTT_lowMass= "<<ZTTLow->Integral()<<"\n";
    //
    //    ZTT->Add(ZTTLow);
    
    hs.Add(ZTT);
    cout << "ZTT= " << ZTT->Integral() << "\n";
    

    
    //    TH1F* signal = (TH1F*) input->Get((channel + "bba150").c_str());
    //    signal->Scale(10);
    //    InitSignal(signal);
    //    cout << "signal= "<<signal->Integral()<<"\n";
    //    //    signal->SetFillColor(kGreen);
    //    //    signal->SetLineColor(kGreen);
    //    hs.Add(signal);
    
    
    canv->cd();
    
    
    TH1F* data = (TH1F*) input->Get((channel + "data_obs").c_str());
    cout << "data= " << data->Integral() << "\n";
        InitData(data);
    TH1F* zero = (TH1F*) data->Clone("zero");
    zero->Scale(0);
    zero->SetTitle("");
    zero->GetXaxis()->SetTitle(xTitle.c_str());
    cout<<"max(hs.GetMaximum(),data->GetMaximum())"<<hs.GetMaximum()<<"   "<<data->GetMaximum()<<"\n";
    zero->SetMaximum(1.5*max(hs.GetMaximum(),data->GetMaximum()));
    zero->Draw();
    
    hs.Draw("histsame");
    //    data->SetBinContent(1,0);
    //    data->SetBinContent(2,0);
    //    data->SetBinContent(3,0);
    //    data->SetBinContent(4,0);
    //    data->SetBinContent(5,0);
    //    data->SetBinContent(6,0);
    //    data->SetBinContent(7,0);
    //    data->SetBinContent(8,0);
    data->Draw("PEsame");
    
    
    const char* dataset;
    dataset = "CMS Preliminary,     1.56 fb^{-1} at 13 TeV";
    CMSPrelim(dataset, "", 0.17, 0.835);
    
    
    
    TLegend* leg = new TLegend(0.52, 0.58, 0.92, 0.89);
    SetLegendStyle(leg);
    //    leg->AddEntry(signal, TString::Format("a1(50 GeV)#rightarrow#tau#tau [XS= 10 bp]", SIGNAL_SCALE), "L");
    
    
    
    leg->AddEntry(data, "observed", "LP");
    leg->AddEntry(ZTT, "Z#rightarrow#tau#tau", "F");
    leg->AddEntry(TT, "t#bar{t}", "F");
    leg->AddEntry(W, "electroweak", "F");
    leg->AddEntry(QCD, "QCD", "F");
    leg->Draw();
    

    canv->Print(TString::Format((nameHisto + ".pdf").c_str()));

}

void draw_prefit_Leppt() {
    
    draw_prefit_Sample("TotalRootForLimit_MuTau_tmass_NoMT_OS.root", "muTau_inclusive/",  "M_{T}  [GeV]", "PLOT_muTau_inclusive_tmass_NoMT");
    draw_prefit_Sample("TotalRootForLimit_EleTau_tmass_NoMT_OS.root", "eleTau_inclusive/", "M_{T} [GeV]", "PLOT_eleTau_inclusive_tmass_NoMT");
    
    draw_prefit_Sample("TotalRootForLimit_MuTau_VisMass_OS.root", "muTau_inclusive/",  "VisibleMass #mu#tau[GeV]", "PLOT_muTau_inclusive_VisbleMass");
    draw_prefit_Sample("TotalRootForLimit_EleTau_VisMass_OS.root", "eleTau_inclusive/",  "VisibleMass e#tau[GeV]", "PLOT_eleTau_inclusive_VisbleMass");

    draw_prefit_Sample("TotalRootForLimit_MuTau_ST_JetBJet_NoMT_OS.root", "muTau_inclusive/",  "ST #mu#tau[GeV]", "PLOT_muTau_inclusive_ST");
    draw_prefit_Sample("TotalRootForLimit_EleTau_ST_JetBJet_NoMT_OS.root", "eleTau_inclusive/", "ST e#tau[GeV]", "PLOT_eleTau_inclusive_ST");


    draw_prefit_Sample("TotalRootForLimit_MuTau_ST_JetBJet_NoMT_OS.root", "muTau_JetBJet/",  "ST #mu#tau[GeV]", "PLOT_muTau_JetBJet_ST");
    draw_prefit_Sample("TotalRootForLimit_EleTau_ST_JetBJet_NoMT_OS.root", "eleTau_JetBJet/", "ST e#tau[GeV]", "PLOT_eleTau_JetBJet_ST");
    
    draw_prefit_Sample("TotalRootForLimit_MuTau_NumJet_NoMT_OS.root", "muTau_inclusive/",  "Jet Multiplicity #mu#tau[GeV]", "PLOT_muTau_inclusive_JetNum");
    draw_prefit_Sample("TotalRootForLimit_EleTau_NumJet_NoMT_OS.root", "eleTau_inclusive/", "Jet Multiplicity e#tau[GeV]", "PLOT_eleTau_inclusive_JetNum");

    
    draw_prefit_Sample("TotalRootForLimit_MuTau_NumBJet_NoMT_OS.root", "muTau_inclusive/",  "BJet Multiplicity #mu#tau[GeV]", "PLOT_muTau_inclusive_BJetNum");
    draw_prefit_Sample("TotalRootForLimit_EleTau_NumBJet_NoMT_OS.root", "eleTau_inclusive/", "BJet Multiplicity e#tau[GeV]", "PLOT_eleTau_inclusive_BJetNum");
    
    draw_prefit_Sample("TotalRootForLimit_MuTau_NumJet_NoMT_OS.root", "muTau_JetBJet/",  "Jet Multiplicity #mu#tau[GeV]", "PLOT_muTau_JetBJet_JetNum");
    draw_prefit_Sample("TotalRootForLimit_EleTau_NumJet_NoMT_OS.root", "eleTau_JetBJet/", "Jet Multiplicity e#tau[GeV]", "PLOT_eleTau_JetBJet_JetNum");
    
    
    draw_prefit_Sample("TotalRootForLimit_MuTau_NumBJet_NoMT_OS.root", "muTau_JetBJet/",  "BJet Multiplicity #mu#tau[GeV]", "PLOT_muTau_JetBJet_BJetNum");
    draw_prefit_Sample("TotalRootForLimit_EleTau_NumBJet_NoMT_OS.root", "eleTau_JetBJet/", "BJet Multiplicity e#tau[GeV]", "PLOT_eleTau_JetBJet_BJetNum");
    


    
};



