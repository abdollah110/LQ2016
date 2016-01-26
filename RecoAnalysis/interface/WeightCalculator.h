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

float XSection(std::string OutName) {
    
    
    
//    https://docs.google.com/spreadsheets/d/1rWM3AlFKO8IJVaeoQkWZYWwSvicQ1QCXYSzH74QyZqE/edit?alt=json#gid=398123591
    
    if (OutName.compare("WJets") == 0) return 61526;
    else if (OutName.compare("DYJetsToLL") == 0) return 6025.2;
    else if (OutName.compare("TTJets") == 0) return 831.76 ;
    
    else if (OutName.compare("WW") == 0) return 309.7;
    else if (OutName.compare("WZ") == 0) return 30400;
    else if (OutName.compare("ZZ") == 0) return 5400;
    
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

    else {
     cout<<"Not Listed in XSection menu !!!! Watch cout \n";
    return 0;
    }
}


float weightCalc(TH1F *Histo,std::string outputName) {
    
//    cout<< "outputName is "<<outputName << "  and histoname is " <<Histo->GetName()<<  " Histo->GetBinContent(1)="<<Histo->GetBinContent(1)<< " XSection(wjet)=" <<XSection("WJets")<<"\n";
    
//    float luminosity=1264-55;
        float luminosity=1560;
    
    size_t isSingleMu = outputName.find("SingleMu");
    size_t isSingleEle = outputName.find("SingleEle");
    size_t isWjet = outputName.find("WJets");
    size_t isZJet = outputName.find("DYJetsToLL");
    size_t isTTbar = outputName.find("TTJets");
    size_t isWW = outputName.find("WW");
    size_t isWZ = outputName.find("WZ");
    size_t isZZ = outputName.find("ZZ");
    size_t isSignalLQ = outputName.find("skimed_lq");
    
    if (isSingleMu != string::npos || isSingleEle!= string::npos)   return 1;
    else if ( isWjet != string::npos ) return (luminosity * XSection("WJets")*1.0) / Histo->GetBinContent(2) ;
    else if ( isZJet != string::npos )   return luminosity * XSection("DYJetsToLL")*1.0 / Histo->GetBinContent(2) ;
    else if ( isTTbar != string::npos )   return luminosity * XSection("TTJets")*1.0 / Histo->GetBinContent(2) ;
    else if ( isWW != string::npos )   return luminosity * XSection("WW")*1.0 / Histo->GetBinContent(2) ;
    else if ( isWZ != string::npos )   return luminosity * XSection("WZ")*1.0 / Histo->GetBinContent(2) ;
    else if ( isZZ != string::npos )   return luminosity * XSection("ZZ")*1.0 / Histo->GetBinContent(2) ;
    
    
    
    else if (isSignalLQ != string::npos) {
        stringstream ss(outputName);
        
        string token;
        string M;
        while (getline(ss,token, '/'))
        {
            cout<< token <<endl;
            M=token;
        }
        
        cout<<"last one is "<< M<<"\n";
        
        
        
        return luminosity * XSection(M)*1.0 / Histo->GetBinContent(2) ;
    }
    
    else
    { cout<<    "Gen Weight is Zeroooo !!!"<<"\n";
        return 0;
    }
    
}














