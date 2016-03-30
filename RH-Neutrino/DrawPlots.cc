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
        canv->SetLogy();
    TFile* input = new TFile(inputF.c_str());
    const char* dataset;
    
    
    THStack hs("hs", "");
    
    //    TH1F* QCD = (TH1F*) input->Get((channel + "QCD").c_str());
    //    InitHist(QCD, "", "", TColor::GetColor(408, 106, 154), 1001);
    //    cout << "QCD= " << QCD->Integral() << "\n";
    //    hs.Add(QCD);
    
    TH1F* W = (TH1F*) input->Get((channel + "W").c_str());
    InitHist(W, "", "", TColor::GetColor(200, 2, 285), 1001);
    cout << "W= " << W->Integral() << "\n";
    hs.Add(W);
    
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
    hs.Add(TT);
    cout << "TT= " << TT->Integral() << "\n";
    
    TH1F* ZTT = (TH1F*) input->Get((channel + "ZTT").c_str());
    InitHist(ZTT, "", "", TColor::GetColor(108, 226, 354), 1001);
    cout << "ZTT= " << ZTT->Integral() << "\n";
    hs.Add(ZTT);
    
    
    
    TH1F* signal = (TH1F*) input->Get((channel + "RHW_1000").c_str());
    InitSignal(signal);
    cout << "signal= "<<signal->Integral()<<"\n";
//    hs.Add(signal);
    
    TH1F* signal2 = (TH1F*) input->Get((channel + "RHW_2000").c_str());
    InitSignal2(signal2);
    cout << "signal2= "<<signal2->Integral()<<"\n";
//    hs.Add(signal2);
    
    
    canv->cd();
    
    
    TH1F* data = (TH1F*) input->Get((channel + "data_obs").c_str());
    cout << "data= " << data->Integral() << "\n";
    InitData(data);
    TH1F* zero = (TH1F*) data->Clone("zero");
    zero->Scale(0);
    zero->SetTitle("");
    zero->GetXaxis()->SetTitle(xTitle.c_str());
    cout<<"max(hs.GetMaximum(),data->GetMaximum())"<<hs.GetMaximum()<<"   "<<data->GetMaximum()<<"\n";
    zero->SetMaximum(20*max(hs.GetMaximum(),data->GetMaximum()));
    zero->SetMinimum(.1);
    zero->Draw();
    
    hs.Draw("histsame");
    signal->Draw("histsame");
    signal2->Draw("histsame");
    data->Draw("PEsame");
    
    
    const char* dataset;
    dataset = "CMS Preliminary,     2.2 fb^{-1} at 13 TeV";
    CMSPrelim(dataset, "", 0.17, 0.835);
    
    
    
    TLegend* leg = new TLegend(0.52, 0.58, 0.92, 0.89);
    SetLegendStyle(leg);
    //    leg->AddEntry(signal, TString::Format("a1(50 GeV)#rightarrow#tau#tau [XS= 10 bp]", SIGNAL_SCALE), "L");
    leg->AddEntry(data, "observed", "LP");
    leg->AddEntry(ZTT, "Z#rightarrow#tau#tau", "F");
    leg->AddEntry(TT, "t#bar{t}", "F");
    leg->AddEntry(W, "W", "F");
    leg->AddEntry(VV, "VV", "F");
    leg->AddEntry(SingleTop, "SingleTop", "F");
    leg->AddEntry(signal, "RHW1000_RHNu500", "F");
    leg->AddEntry(signal2, "RHW2000_RHNu1000", "F");
    //    leg->AddEntry(QCD, "QCD", "F");
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

void DrawPlots() {
    
    
    
    
    const int numPlots=11;
    const int numCat=1;
    
    const int numch =2;
    
    
    
    
    string Names [numPlots]= {"_tmass","_VisMass","_LepPt","_TauPt","_FullMass","_FullMass_HighMET","_MET","_FullTransMass" ,"_FullTransMass_HighMET" , "_ST", "_ST_HighMET"};
    string Xaxis[numPlots]={ "M_{T}(lep,MET)  [GeV]","VissMass(lep,#tau)  [GeV]","Lepton Pt  [GeV]","#tau Pt  [GeV]","M_{l#taujj} (GeV)","M_{l#taujj}(MET > 50 ) (GeV)","MET  [GeV]","M_{T} (lljjMET) (GeV)","M_{T} (lljjMET) (MET > 50) (GeV)", "MHT (GeV)", " MHT (for MET > 50) (GeV)"};
    
    //    string category[numCat] = {"_inclusive","_JetBJet","_DiNonBJet"};
    string category[numCat] = {"_DiJet"};
    string channelDirectory[numch] = {"MuTau", "EleTau"};
    //        string channelDirectory[numch] = {"MuTau"};
    
    
    for (int iname=0;iname < numPlots;iname++){
        for (int iCat=0;iCat < numCat;iCat++){
            for (int ich=0;ich < numch;ich++){
                cout<< "\n\n\n ------------------------------------------  Start New plot\n";
                string RootName="TotalRootForLimit_"+channelDirectory[ich]+Names[iname]+".root";
                string ChanCat=channelDirectory[ich]+category[iCat]+"/";
                string LegName=channelDirectory[ich]+category[iCat];
                string OutName="Plot_"+channelDirectory[ich]++category[iCat]+Names[iname];
                
                draw_prefit_Sample(RootName, ChanCat,  Xaxis[iname], OutName,LegName);
                
            }
        }
        
    }
    
    
    
    
    
};



