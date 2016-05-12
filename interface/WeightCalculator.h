#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <utility>
#include <map>
#include <string>
#include "TH1F.h"
#include "TH2F.h"
#include "TTree.h"
#include "TFile.h"
#include "TF1.h"
#include "TSystem.h"
#include "TMath.h" //M_PI is in TMath
#include "TRandom3.h"
#include <TLorentzVector.h>
using namespace std;


float WScaleFactor=1.20; // computed on Apr 20th
//float TTScaleFactor=0.91;
//float WScaleFactor=1.22;
//float TTScaleFactor=0.856;


float XSection(std::string OutName) {
    
    
    
    //    https://docs.google.com/spreadsheets/d/1rWM3AlFKO8IJVaeoQkWZYWwSvicQ1QCXYSzH74QyZqE/edit?alt=json#gid=398123591
    
    
    //WJet       float XSection_W[numBG] = {30400, 5400, 1750, 519, 214};
    //     if (OutName.find("WJetsToLNu") != string::npos) return 50690;
    if (OutName.find("WJetsToLNu_Inc") != string::npos) return 50690; //61526.7;
    else if (OutName.find("WJetsToLNu_HT-100To200") != string::npos) return 1345;
    else if (OutName.find("WJetsToLNu_HT-200To400") != string::npos) return 359.7;
    else if (OutName.find("WJetsToLNu_HT-400To600") != string::npos) return 48.91;
    else if (OutName.find("WJetsToLNu_HT-600ToInf") != string::npos) return 18.77;
    
    //DYJets   float XSection_DY[numBG] = {2950, 561, 181, 51.1, 23};
    else if (OutName.find("DYJetsToLL_Inc") != string::npos) return 4895;
    else if (OutName.find("DYJetsToLL_M-50_HT-100to200") != string::npos) return 147.4;
    else if (OutName.find("DYJetsToLL_M-50_HT-200to400") != string::npos) return 40.99;
    else if (OutName.find("DYJetsToLL_M-50_HT-400to600") != string::npos) return 5.678;
    else if (OutName.find("DYJetsToLL_M-50_HT-600toInf") != string::npos) return 2.198;
    
    //Di-boson
    else if (OutName.find("WW") != string::npos) return 115.0;
    else if (OutName.find("WZ") != string::npos) return 47.13;
    else if (OutName.find("ZZ") != string::npos) return 16.523;
    
    //SingleTop
    else if (OutName.find("ST_t-channel_antitop_4f_leptonDecays") != string::npos) return 80.95 * 0.108*3;
    else if (OutName.find("ST_t-channel_top_4f_leptonDecays") != string::npos) return 136.02 * 0.108*3;
    else if (OutName.find("ST_tW_antitop_5f_inclusiveDecays") != string::npos) return 35.6;
    else if (OutName.find("ST_tW_top_5f_inclusiveDecays") != string::npos) return 35.6;
    
    
    //    else if (OutName.find("TTJets_DiLept") != string::npos) return (89.05);
    //    else if (OutName.find("TTJets_SingleLeptFromT") != string::npos) return (183.46);
    //    else if (OutName.find("TTJets_SingleLeptFromTbar") != string::npos) return (183.46);
    
    //    else if (OutName.find("TTJets_DiLept_Ext") != string::npos) return (89.05);
    //    else if (OutName.find("TTJets_SingleLeptFromT_Ext") != string::npos) return (183.46);
    //    else if (OutName.find("TTJets_SingleLeptFromTbar_Ext") != string::npos) return (183.46);
    
//    else if (OutName.find("Inclusive_TTJets") != string::npos) return (831.76);
//    else if (OutName.find("NewTT") != string::npos) return (831.76);
   
    else if (OutName.find("Inclusive_TTJets") != string::npos) return (831.76);
//    else if (OutName.find("NewTT") != string::npos) return (831.76 * 0.9);
    
//    //    https://twiki.cern.ch/twiki/bin/view/CMS/Exo2015LQ1AndLQ2Analyses
//    else if (OutName.find("skimed_lq200.root") != string::npos) return 60.6;
//    else if (OutName.find("skimed_lq250.root") != string::npos) return 20.3;
//    else if (OutName.find("skimed_lq300.root") != string::npos) return     8.05E+00;
//    else if (OutName.find("skimed_lq350.root") != string::npos) return     3.58E+00;
//    else if (OutName.find("skimed_lq400.root") != string::npos) return     1.74E+00;
//    else if (OutName.find("skimed_lq450.root") != string::npos) return     9.05E-01;
//    else if (OutName.find("skimed_lq500.root") != string::npos) return     4.96E-01;
//    else if (OutName.find("skimed_lq550.root") != string::npos) return     2.84E-01;
//    else if (OutName.find("skimed_lq600.root") != string::npos) return     1.69E-01;
//    else if (OutName.find("skimed_lq650.root") != string::npos) return     1.03E-01;
//    else if (OutName.find("skimed_lq700.root") != string::npos) return     6.48E-02;
//    else if (OutName.find("skimed_lq750.root") != string::npos) return     4.16E-02;
//    else if (OutName.find("skimed_lq800.root") != string::npos) return     2.73E-02;
//    else if (OutName.find("skimed_lq850.root") != string::npos) return     1.82E-02;
//    else if (OutName.find("skimed_lq900.root") != string::npos) return     1.23E-02;
//    else if (OutName.find("skimed_lq950.root") != string::npos) return     8.45E-03;
//    else if (OutName.find("skimed_lq1000.root") != string::npos) return     5.86E-03;
//    else if (OutName.find("skimed_lq1050.root") != string::npos) return     4.11E-03;
//    else if (OutName.find("skimed_lq1100.root") != string::npos) return     2.91E-03;
//    else if (OutName.find("skimed_lq1150.root") != string::npos) return     2.08E-03;
//    else if (OutName.find("skimed_lq1200.root") != string::npos) return     1.50E-03;
//    else if (OutName.find("skimed_lq1250.root") != string::npos) return     1.09E-03;
//    else if (OutName.find("skimed_lq1300.root") != string::npos) return     7.95E-04;
//    else if (OutName.find("skimed_lq1350.root") != string::npos) return     5.85E-04;
//    else if (OutName.find("skimed_lq1400.root") != string::npos) return     4.33E-04;
//    else if (OutName.find("skimed_lq1450.root") != string::npos) return     3.21E-04;
//    else if (OutName.find("skimed_lq1500.root") != string::npos) return     2.40E-04;
//    
//    
//    
//    
//    else if (OutName.find("skimed_0_RHNu_1000-500") != string::npos) return      1.692E+00;
//    else if (OutName.find("skimed_0_RHNu_1500-750") != string::npos) return      2.90E-01;
//    else if (OutName.find("skimed_0_RHNu_2000-1000") != string::npos) return     6.563E-02;
//    else if (OutName.find("skimed_0_RHNu_2500-1250") != string::npos) return     1.92E-02;
//    else if (OutName.find("skimed_0_RHNu_3000-1500") != string::npos) return     6.030E-03;
    
    else if (OutName.find("skimed_lq") != string::npos) return     1.0;
        else if (OutName.find("skimed_0_RHNu_") != string::npos ) return      1.0;
    
    
    
    else {
        cout<<"Not Listed in XSection menu !!!! Watch cout \n";
        return 0;
    }
}




vector <float> W_HTBin(std::string FileLoc){
    
    const int WSize=5;
    std::string W_ROOTFiles[WSize]={"WJetsToLNu_Inc.root", "WJetsToLNu_HT-100To200.root","WJetsToLNu_HT-200To400.root","WJetsToLNu_HT-400To600.root", "WJetsToLNu_HT-600ToInf.root"};
    
    vector<float> W_events;
    W_events.clear();
    
    for (int i=0; i <WSize;i++){
        
        TFile * File_W = new TFile((FileLoc+W_ROOTFiles[i]).c_str());
        TH1F * Histo_W = (TH1F*) File_W->Get("hEvents");
        W_events.push_back(Histo_W->GetBinContent(2));
        cout<<"Number of proccessed evenets for "<<W_ROOTFiles[i]<<" = "<<Histo_W->GetBinContent(2)<<"\n";
    }
    
    return W_events ;
    
}

vector <float> DY_HTBin(std::string FileLoc){
    
    const int DYSize=5;
    std::string DY_ROOTFiles[DYSize]={"DYJetsToLL_M-50_Inc.root", "DYJetsToLL_M-50_HT-100to200.root","DYJetsToLL_M-50_HT-200to400.root","DYJetsToLL_M-50_HT-400to600.root", "DYJetsToLL_M-50_HT-600toInf.root"};
    
    vector<float> DY_events;
    DY_events.clear();
    
    for (int i=0; i < DYSize;i++){
        
        TFile * File_DY = new TFile((FileLoc+DY_ROOTFiles[i]).c_str());
        TH1F * Histo_DY= (TH1F*) File_DY->Get("hEvents");
        DY_events.push_back(Histo_DY->GetBinContent(2));
        cout<<"Number of proccessed evenets for "<<DY_ROOTFiles[i]<<" = "<<Histo_DY->GetBinContent(2)<<"\n";
    }
    
    return DY_events ;
    
}












float weightCalc(TH1F *Histo,std::string outputName , float genHT, vector<float> W_events, vector<float> DY_events) {
    
    //    cout<< "outputName is "<<outputName << "  and histoname is " <<Histo->GetName()<<  " Histo->GetBinContent(1)="<<Histo->GetBinContent(1)<< " XSection(wjet)=" <<XSection("WJets")<<"\n";
    
    
    stringstream ss(outputName);
    
    string token;
    string M;
    while (getline(ss,token, '/'))  M=token;
    
    std::string FirstPart = "";
    std::string LastPart = ".root";
    std::string newOut = M.substr(FirstPart.size());
    newOut = newOut.substr(0, newOut.size() - LastPart.size());
    //    cout<<"--->  Check Name is "<<newOut<<"\n";
    
    
    float LOtoNLO_DY = 1.230888662;
    float LOtoNLO_W = 1.213783784 * WScaleFactor;
    //    float luminosity=2154;
    float luminosity=    2262.946;
    
    size_t isSingleMu = outputName.find("SingleMu");
    size_t isSingleEle = outputName.find("SingleEle");
    
    size_t isWjet = outputName.find("WJets");
    size_t isDYJet = outputName.find("DYJets");
    
    
    if (isSingleMu != string::npos || isSingleEle!= string::npos)   return 1;
    
    else if (isWjet != string::npos) {

        if (genHT <= 100) return luminosity*LOtoNLO_W / (W_events[0] / XSection("WJetsToLNu_Inc"));
        else if (genHT > 100 && genHT <= 200) return luminosity*LOtoNLO_W / (W_events[1] / XSection("WJetsToLNu_HT-100To200") + W_events[0] / XSection("WJetsToLNu_Inc"));
        else if (genHT > 200 && genHT <=400) return luminosity*LOtoNLO_W / (W_events[2] / XSection("WJetsToLNu_HT-200To400") + W_events[0] / XSection("WJetsToLNu_Inc"));
        else if (genHT > 400 && genHT <=600) return luminosity*LOtoNLO_W / (W_events[3] / XSection("WJetsToLNu_HT-400To600") + W_events[0] / XSection("WJetsToLNu_Inc"));
        else if (genHT > 600) return luminosity*LOtoNLO_W / (W_events[4] / XSection("WJetsToLNu_HT-600ToInf") + W_events[0] / XSection("WJetsToLNu_Inc"));
        else   {cout<<"**********   wooow  ********* There is a problem here\n";return 0;}
        
        
    } else if (isDYJet != string::npos) {
        
        if (genHT <= 100) return luminosity*LOtoNLO_DY / (DY_events[0] / XSection("DYJetsToLL_Inc"));
        else if (genHT > 100 && genHT <= 200) return  luminosity*LOtoNLO_DY / (DY_events[1] / XSection("DYJetsToLL_M-50_HT-100to200") + DY_events[0] / XSection("DYJetsToLL_Inc"));
        else if (genHT > 200 && genHT <=400) return luminosity*LOtoNLO_DY / (DY_events[2] / XSection("DYJetsToLL_M-50_HT-200to400") + DY_events[0] / XSection("DYJetsToLL_Inc"));
        else if (genHT > 400 && genHT <=600) return luminosity*LOtoNLO_DY / (DY_events[3] / XSection("DYJetsToLL_M-50_HT-400to600") + DY_events[0] / XSection("DYJetsToLL_Inc"));
        else if (genHT > 600) return luminosity*LOtoNLO_DY / (DY_events[4] / XSection("DYJetsToLL_M-50_HT-600toInf") + DY_events[0] / XSection("DYJetsToLL_Inc"));
        else   {cout<<"**********   wooow  ********* There is a problem here\n";return 0;}
    }
    
    
    else
        return luminosity * XSection(newOut)*1.0 / Histo->GetBinContent(2);
    
    
}














