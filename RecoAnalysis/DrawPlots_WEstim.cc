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




void draw_prefit_Sample(std::string inputF, std::string channel, std::string xTitle, std::string nameHisto, std::string CatName ) {
    
    //    gStyle->SetOptStat(0);
    
    
    cout<< "   name Histo is "<<nameHisto <<"\n";
    
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
    
    
    
    TH1F* VV = (TH1F*) input->Get((channel + "VV").c_str());
    if (VV){
        InitHist(VV, "", "", TColor::GetColor(200, 282, 232), 1001);
        cout << "VV= " << VV->Integral() << "\n";
        hs.Add(VV);
    }
    
    TH1F* SingleTop = (TH1F*) input->Get((channel + "SingleTop").c_str());
    InitHist(SingleTop, "", "", TColor::GetColor(150, 132, 232), 1001);
    cout << "SingleTop= " << SingleTop->Integral() << "\n";
    hs.Add(SingleTop);
    
    
    TH1F* TT = (TH1F*) input->Get((channel + "TT").c_str());
    InitHist(TT, "", "", TColor::GetColor(208, 376, 124), 1001);
    //    TT->Scale(0.85);
    hs.Add(TT);
    cout << "TT= " << TT->Integral() << "\n";
    
    TH1F* ZTT = (TH1F*) input->Get((channel + "ZTT").c_str());
    InitHist(ZTT, "", "", TColor::GetColor(108, 226, 354), 1001);
    cout << "ZTT= " << ZTT->Integral() << "\n";
    hs.Add(ZTT);
    
    TH1F* QCD = (TH1F*) input->Get((channel + "QCD").c_str());
    InitHist(QCD, "", "", TColor::GetColor(408, 106, 154), 1001);
    cout << "QCD= " << QCD->Integral() << "\n";
    hs.Add(QCD);
    
    TH1F* W = (TH1F*) input->Get((channel + "W").c_str());
    InitHist(W, "", "", TColor::GetColor(200, 2, 285), 1001);
    cout << "W= " << W->Integral() << "\n";
    hs.Add(W);
    
    
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
    zero->SetMaximum(2*data->GetMaximum());
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
    dataset = "CMS Preliminary,      2.2 fb^{-1} at 13 TeV";
    CMSPrelim(dataset, "", 0.17, 0.835);
    
    
    
    TLegend* leg = new TLegend(0.52, 0.58, 0.92, 0.89);
    SetLegendStyle(leg);
    leg->AddEntry(data, "observed", "LP");
    leg->AddEntry(W, "W", "F");
    leg->AddEntry(QCD, "QCD", "F");
    leg->AddEntry(ZTT, "Z#rightarrow#tau#tau", "F");
    leg->AddEntry(TT, "t#bar{t}", "F");
    leg->AddEntry(SingleTop, "SingleTop", "F");
    leg->AddEntry(VV, "VV", "F");
    
    
    leg->Draw();
    
    
    TPaveText* info  = new TPaveText(0.20, 0.78, 0.35, 0.89, "NDC");
    info->SetBorderSize(   0 );
    info->SetFillStyle(    0 );
    info->SetTextAlign(   12 );
    info->SetTextSize ( 0.03 );
    info->SetTextColor(    1 );
    info->SetTextFont (   62 );
    info->AddText(CatName.c_str());
    info->Draw();
    
    canv->Print(TString::Format((nameHisto + ".pdf").c_str()));
    
}

void DrawPlots_WEstim() {
    
    
    
    
    const int numPlots=1;
    const int numCat=2;
    
    const int numch =1;
    
    
    
    
    
    
    string Names [numPlots]= {"fileWEstim.root"};
    string Xaxis[numPlots]={ "ST  [GeV]"};
    
    
    string category[numCat] = {"beforeScale","afterScale"};
    string     legendN[numCat]= {"Before Scale Correction", "After Scale Correction"}
    string channelDirectory[numch] = {"MuTau"};
    
    
    for (int iname=0;iname < numPlots;iname++){
        for (int iCat=0;iCat < numCat;iCat++){
            for (int ich=0;ich < numch;ich++){
                cout<< "\n\n\n ------------------------------------------  Start New plot\n";
                string RootName="fileWEstim.root";
                string ChanCat=category[iCat]+"/";
                string LegName=legendN[iCat];
                string OutName="Plot_"+category[iCat]+Names[iname];
                
                draw_prefit_Sample(RootName, ChanCat,  Xaxis[iname], OutName,LegName);
                
            }
        }
        
    }
    
    
    
    
    
    
//    const int numPlots=6;
//    const int numCat=2;
//    
//    const int numch =1;
//    
//    
//    
//    
//    
//    
//    string Names [numPlots]= {"_tmass_HighMT_OS","_tmass_LowMT_SS_Total","_tmass_HighMT_SS_TauIsoLepAntiIso","_tmass_LowMT_SS_LepIso","_tmass_HighMT_OS_TauIsoLepAntiIso","_tmass_HighMT_SS"};
//    string Xaxis[numPlots]={ "M_{T}(lep,MET)  [GeV]","M_{T}(lep,MET)  [GeV]","M_{T}(lep,MET)  [GeV]","M_{T}(lep,MET)  [GeV]","M_{T}(lep,MET)  [GeV]"};
//    
//    //    string category[numCat] = {"_inclusive","_JetBJet","_DiNonBJet"};
//    string category[numCat] = {"_inclusive","_DiNonBJet"};
//    //    string channelDirectory[numch] = {"muTau", "eleTau"};
//    string channelDirectory[numch] = {"MuTau"};
//    
//    
//    for (int iname=0;iname < numPlots;iname++){
//        for (int iCat=0;iCat < numCat;iCat++){
//            for (int ich=0;ich < numch;ich++){
//                cout<< "\n\n\n ------------------------------------------  Start New plot\n";
//                string RootName="WEstimation_TotalRootForLimit_"+channelDirectory[ich]+Names[iname]+".root";
//                string ChanCat=channelDirectory[ich]+category[iCat]+"/";
//                string LegName=channelDirectory[ich]+category[iCat];
//                string OutName="Plot_"+channelDirectory[ich]++category[iCat]+Names[iname];
//                
//                draw_prefit_Sample(RootName, ChanCat,  Xaxis[iname], OutName,LegName);
//                
//            }
//        }
//        
//    }
    
    

    
    
};



