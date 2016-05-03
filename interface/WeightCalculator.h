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
float TTScaleFactor=0.91;
//float WScaleFactor=1.22;
//float TTScaleFactor=0.856;


float XSection(std::string OutName) {
    
    
    
    //    https://docs.google.com/spreadsheets/d/1rWM3AlFKO8IJVaeoQkWZYWwSvicQ1QCXYSzH74QyZqE/edit?alt=json#gid=398123591
    
    
    //WJet       float XSection_W[numBG] = {30400, 5400, 1750, 519, 214};
    //     if (OutName.compare("WJetsToLNu") == 0) return 50690;
    if (OutName.compare("WJetsToLNu_Inc") == 0) return 50690; //61526.7;
    else if (OutName.compare("WJetsToLNu_HT-100To200") == 0) return 1345;
    else if (OutName.compare("WJetsToLNu_HT-200To400") == 0) return 359.7;
    else if (OutName.compare("WJetsToLNu_HT-400To600") == 0) return 48.91;
    else if (OutName.compare("WJetsToLNu_HT-600ToInf") == 0) return 18.77;
    
    //DYJets   float XSection_DY[numBG] = {2950, 561, 181, 51.1, 23};
    else if (OutName.compare("DYJetsToLL_Inc") == 0) return 4895;
    else if (OutName.compare("DYJetsToLL_M-50_HT-100to200") == 0) return 147.4;
    else if (OutName.compare("DYJetsToLL_M-50_HT-200to400") == 0) return 40.99;
    else if (OutName.compare("DYJetsToLL_M-50_HT-400to600") == 0) return 5.678;
    else if (OutName.compare("DYJetsToLL_M-50_HT-600toInf") == 0) return 2.198;
    
    //Di-boson
    else if (OutName.compare("WW") == 0) return 115.0;
    else if (OutName.compare("WZ") == 0) return 47.13;
    else if (OutName.compare("ZZ") == 0) return 16.523;
    
    //SingleTop
    else if (OutName.compare("ST_t-channel_antitop_4f_leptonDecays") == 0) return 80.95 * 0.108*3;
    else if (OutName.compare("ST_t-channel_top_4f_leptonDecays") == 0) return 136.02 * 0.108*3;
    else if (OutName.compare("ST_tW_antitop_5f_inclusiveDecays") == 0) return 35.6;
    else if (OutName.compare("ST_tW_top_5f_inclusiveDecays") == 0) return 35.6;
    
    
    //    else if (OutName.compare("TTJets_DiLept") == 0) return (89.05);
    //    else if (OutName.compare("TTJets_SingleLeptFromT") == 0) return (183.46);
    //    else if (OutName.compare("TTJets_SingleLeptFromTbar") == 0) return (183.46);
    
    //    else if (OutName.compare("TTJets_DiLept_Ext") == 0) return (89.05);
    //    else if (OutName.compare("TTJets_SingleLeptFromT_Ext") == 0) return (183.46);
    //    else if (OutName.compare("TTJets_SingleLeptFromTbar_Ext") == 0) return (183.46);
    
//    else if (OutName.compare("Inclusive_TTJets") == 0) return (831.76);
//    else if (OutName.compare("NewTT") == 0) return (831.76);
   
    else if (OutName.compare("Inclusive_TTJets") == 0) return (831.76 * TTScaleFactor);
//    else if (OutName.compare("NewTT") == 0) return (831.76 * 0.9);
    
    //    https://twiki.cern.ch/twiki/bin/view/CMS/Exo2015LQ1AndLQ2Analyses
    else if (OutName.compare("skimed_lq200.root") == 0) return 60.6;
    else if (OutName.compare("skimed_lq250.root") == 0) return 20.3;
    else if (OutName.compare("skimed_lq300.root") == 0) return     8.05E+00;
    else if (OutName.compare("skimed_lq350.root") == 0) return     3.58E+00;
    else if (OutName.compare("skimed_lq400.root") == 0) return     1.74E+00;
    else if (OutName.compare("skimed_lq450.root") == 0) return     9.05E-01;
    else if (OutName.compare("skimed_lq500.root") == 0) return     4.96E-01;
    else if (OutName.compare("skimed_lq550.root") == 0) return     2.84E-01;
    else if (OutName.compare("skimed_lq600.root") == 0) return     1.69E-01;
    else if (OutName.compare("skimed_lq650.root") == 0) return     1.03E-01;
    else if (OutName.compare("skimed_lq700.root") == 0) return     6.48E-02;
    else if (OutName.compare("skimed_lq750.root") == 0) return     4.16E-02;
    else if (OutName.compare("skimed_lq800.root") == 0) return     2.73E-02;
    else if (OutName.compare("skimed_lq850.root") == 0) return     1.82E-02;
    else if (OutName.compare("skimed_lq900.root") == 0) return     1.23E-02;
    else if (OutName.compare("skimed_lq950.root") == 0) return     8.45E-03;
    else if (OutName.compare("skimed_lq1000.root") == 0) return     5.86E-03;
    else if (OutName.compare("skimed_lq1050.root") == 0) return     4.11E-03;
    else if (OutName.compare("skimed_lq1100.root") == 0) return     2.91E-03;
    else if (OutName.compare("skimed_lq1150.root") == 0) return     2.08E-03;
    else if (OutName.compare("skimed_lq1200.root") == 0) return     1.50E-03;
    else if (OutName.compare("skimed_lq1250.root") == 0) return     1.09E-03;
    else if (OutName.compare("skimed_lq1300.root") == 0) return     7.95E-04;
    else if (OutName.compare("skimed_lq1350.root") == 0) return     5.85E-04;
    else if (OutName.compare("skimed_lq1400.root") == 0) return     4.33E-04;
    else if (OutName.compare("skimed_lq1450.root") == 0) return     3.21E-04;
    else if (OutName.compare("skimed_lq1500.root") == 0) return     2.40E-04;
    
    
    
    
    else if (OutName.compare("skimed_0_RHNu_1000-500") == 0) return      1.692E+00;
    else if (OutName.compare("skimed_0_RHNu_1500-750") == 0) return      2.90E-01;
    else if (OutName.compare("skimed_0_RHNu_2000-1000") == 0) return     6.563E-02;
    else if (OutName.compare("skimed_0_RHNu_2500-1250") == 0) return     1.92E-02;
    else if (OutName.compare("skimed_0_RHNu_3000-1500") == 0) return     6.030E-03;
    
    
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
    
    size_t isSignalLQ = outputName.find("skimed_lq");
    
    
    
    if (isSingleMu != string::npos || isSingleEle!= string::npos)   return 1;
    
    else if (isWjet != string::npos) {
        //        return luminosity*LOtoNLO_W / (W_events[0] / XSection("WJetsToLNu_Inc"));
        
        
        
        //    } else if (isDYJet != string::npos) {
        //
        //        return luminosity*LOtoNLO_DY / (DY_events[0] / XSection("DYJetsToLL"));
        //
        //    }
        //
        //
        //    else if (isWjet != string::npos) {
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
    
    
    
    
    else if (isSignalLQ != string::npos) {
        stringstream ss(outputName);
        
        string token;
        string M;
        while (getline(ss,token, '/'))
        {
            //                cout<< token <<endl;
            M=token;
        }
        
        //            cout<<"last one is "<< M<<"\n";
        
        
        
        return luminosity * XSection(M)*1.0 / Histo->GetBinContent(2) ;
    }
    
    else
        return luminosity * XSection(newOut)*1.0 / Histo->GetBinContent(2);
    //            return luminosity * XSection(newOut)*1.0 / Histo->Integral();  BUG found  25 Feb
    
    
}














