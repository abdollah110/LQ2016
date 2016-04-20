#include <iostream>
#include<fstream>
#include<vector>

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
#include <string>

#include <TPaveText.h>
#include <THStack.h>
#include <algorithm>    // std::max
#include "interface/HttStyles.h"
#include "interface/HttStyles.cc"
#include <string>
#include <memory>


int PlotName[2][2] = {
    { 2, 3 },
    { 4, 5}
};


void draw_prefit_Sample(std::string inputF, std::string channel, string xTitle, std::string nameHisto, std::string CatName, int ReBIN_) {
    
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
    
    TH1F* QCD = (TH1F*) input->Get((channel + "QCD").c_str());
    QCD->Rebin(ReBIN_);
    InitHist(QCD, "", "", TColor::GetColor(408, 106, 154), 1001);
    cout << "QCD= " << QCD->Integral() << "\n";
    hs.Add(QCD);
    
    TH1F* W = (TH1F*) input->Get((channel + "W").c_str());
        W->Rebin(ReBIN_);
    InitHist(W, "", "", TColor::GetColor(200, 2, 285), 1001);
    cout << "W= " << W->Integral() << "\n";
    hs.Add(W);
    
    TH1F* VV = (TH1F*) input->Get((channel + "VV").c_str());
    if (VV){
            VV->Rebin(ReBIN_);
        InitHist(VV, "", "", TColor::GetColor(200, 282, 232), 1001);
        cout << "VV= " << VV->Integral() << "\n";
        hs.Add(VV);
    }
    
    TH1F* SingleTop = (TH1F*) input->Get((channel + "SingleTop").c_str());
    SingleTop->Rebin(ReBIN_);
    InitHist(SingleTop, "", "", TColor::GetColor(150, 132, 232), 1001);
    cout << "SingleTop= " << SingleTop->Integral() << "\n";
    hs.Add(SingleTop);
    
    
    TH1F* TT = (TH1F*) input->Get((channel + "TT").c_str());
    TT->Rebin(ReBIN_);
    InitHist(TT, "", "", TColor::GetColor(208, 376, 124), 1001);
    //    TT->Scale(0.85);
    hs.Add(TT);
    cout << "TT= " << TT->Integral() << "\n";
    
    TH1F* ZTT = (TH1F*) input->Get((channel + "ZTT").c_str());
    ZTT->Rebin(ReBIN_);
    InitHist(ZTT, "", "", TColor::GetColor(108, 226, 354), 1001);
    cout << "ZTT= " << ZTT->Integral() << "\n";
    hs.Add(ZTT);
    

    
//        TH1F* signal = (TH1F*) input->Get((channel + "LQ_700").c_str());
//        signal->Scale(10);
//        InitSignal(signal);
//        cout << "signal= "<<signal->Integral()<<"\n";
        //    signal->SetFillColor(kGreen);
        //    signal->SetLineColor(kGreen);
//        hs.Add(signal);
    
    
    canv->cd();
    
    
    TH1F* data = (TH1F*) input->Get((channel + "data_obs").c_str());
    data->Rebin(ReBIN_);
    cout << "data= " << data->Integral() << "\n";
        InitData(data);
    TH1F* zero = (TH1F*) data->Clone("zero");
    zero->Scale(0);
    zero->SetTitle("");
    zero->GetXaxis()->SetTitle(xTitle.c_str());
    cout<<"max(hs.GetMaximum(),data->GetMaximum())"<<hs.GetMaximum()<<"   "<<data->GetMaximum()<<"\n";
    zero->SetMaximum(2*max(hs.GetMaximum(),data->GetMaximum()));
    zero->Draw();
    
    hs.Draw("histsame");
//    signal->Draw("histsame");
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
    dataset = "CMS Preliminary,     2.2 fb^{-1} at 13 TeV";
    CMSPrelim(dataset, "", 0.17, 0.835);
    
    
    
    TLegend* leg = new TLegend(0.52, 0.58, 0.92, 0.89);
    SetLegendStyle(leg);
    //    leg->AddEntry(signal, TString::Format("a1(50 GeV)#rightarrow#tau#tau [XS= 10 bp]", SIGNAL_SCALE), "L");
    
    
    
    leg->AddEntry(data, "observed", "LP");
    leg->AddEntry(W, "W", "F");
    leg->AddEntry(QCD, "QCD", "F");
    leg->AddEntry(ZTT, "DY#rightarrowll", "F");
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

void DrawPlots_PreSelection() {
    
    
    
    
    const int numPlots=16;
//    const int mul=3;
    const int numCat=2;
    
    const int numch =2;
    
//    string MM= "yes";
//    
//char * myarray[2][3] = {
//        { "hello", "jack", "dawson" },
//        { "hello", "hello", "hello" }
//    };
//    
//    
//char *    PlotName [numPlots][mul]={
//        {"_tmass_OS","M_{T}[GeV]",10},
//        {"_VisMass_OS","VisMass[GeV]",10}};
//

    
    
    string Names [numPlots]= {"_tmass","_VisMass","_LepPt","_LepEta","_TauPt","_TauEta","_NumJet","_NumBJet","_nVtx","_nVtx_NoPU","_MET","_M_taujet", "_LeadJetPt","_SubLeadJetPt","_ST_DiJet","_ST_MET"};
    string Xaxis[numPlots]={ "M_{T}(lep,MET)  [GeV]","VisMass(lep,#tau)  [GeV]", "lep PT [GeV]", "lep #eta [GeV]","#tau PT [GeV]", "#tau #eta [GeV]", "Jet multiplicity", "BJet multiplicity", "Num Vertex","Num Vertex [no PU correction]", "MET  [GeV]",  " M_{#tauj}   [GeV]","Leading Jet PT  [GeV]","subLeading Jet PT  [GeV]","ST_{l#taujj}  [GeV] ","ST_{l#taujjMET}  [GeV] "};
    
    int ReBIN [numPlots]={10,10,10,10,10,10,1,1,1,1,10,10,10,10,10,10};
//    string category[numCat] = {"_inclusive"};
        string category[numCat] = {"_DiJet","_JetBJet"};
    string channelDirectory[numch] = {"MuTau", "EleTau"};
//        string channelDirectory[numch] = {"MuTau"};
    
    
    for (int iname=0;iname < numPlots;iname++){
        for (int iCat=0;iCat < numCat;iCat++){
            for (int ich=0;ich < numch;ich++){
                cout<< "\n\n\n ------------------------------------------  Start New plot\n";
                string RootName="TotalRootForLimit_"+channelDirectory[ich]+Names[iname]+"_OS"+".root";
                string ChanCat=channelDirectory[ich]+category[iCat]+"/";
                string LegName=channelDirectory[ich]+category[iCat];
                string OutName="Plot_"+channelDirectory[ich]+category[iCat]+Names[iname]+"_OS";
                cout<< "OutName="<<RootName<<"   "<<ChanCat<<"\n";
                
                draw_prefit_Sample(RootName, ChanCat,  Xaxis [iname], OutName,LegName,ReBIN[iname]);
                
            }
        }
        
    }
    
 


    
};



