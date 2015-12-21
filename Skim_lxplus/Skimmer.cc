#define Skimmer_cxx
#include "Skimmer.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TLorentzVector.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <TMath.h>
using namespace std;

void Skimmer::Loop(TString outputName, int split)
{
    
    
    TH1F* hEvents = (TH1F*)gDirectory->Get("ggNtuplizer/hEvents");
    TH1F* hPU     = (TH1F*)gDirectory->Get("ggNtuplizer/hPU");
    TH1F* hPUTrue = (TH1F*)gDirectory->Get("ggNtuplizer/hPUTrue");
    
    TFile* file = TFile::Open(outputName, "RECREATE");
    TTree* MyNewTree = fChain->CloneTree(0);
    
    fChain->SetBranchStatus("*",0);
    fChain->SetBranchStatus("run",1);
    fChain->SetBranchStatus("event",1);
    fChain->SetBranchStatus("lumis",1);
    fChain->SetBranchStatus("isData",1);
    fChain->SetBranchStatus("HLT*",1);
    fChain->SetBranchStatus("gen*",1);
    fChain->SetBranchStatus("pdf",1);
    fChain->SetBranchStatus("pthat",1);
    fChain->SetBranchStatus("processID",1);
    fChain->SetBranchStatus("rho*",1);
    fChain->SetBranchStatus("pu*",1);
    fChain->SetBranchStatus("mc*",1);
    fChain->SetBranchStatus("pfMET*",1);
    fChain->SetBranchStatus("n*",1);
    fChain->SetBranchStatus("c*",1);
    fChain->SetBranchStatus("jet*",1);
    fChain->SetBranchStatus("AK8*",0);
    fChain->SetBranchStatus("ele*",1);
    fChain->SetBranchStatus("mu*",1);
    fChain->SetBranchStatus("nPho",0);
    fChain->SetBranchStatus("tau*",1);
    
    
    TH1F* hcount = new TH1F("hcount", "", 10, 1, 10);
    
    if (fChain == 0) return;
    
    Long64_t nentries = fChain->GetEntriesFast();
    Long64_t nbytes = 0, nb = 0;
    
    Long64_t nOverTen= nentries/10;
    Long64_t jentry = split*nOverTen;
    Long64_t finalEntry = (split+1)*nOverTen;
    if (split==9) finalEntry=nentries;
    
    for (jentry=split*nOverTen; jentry<finalEntry;jentry++) {
        
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0) break;
        nb = fChain->GetEntry(jentry);   nbytes += nb;
        
        
        if(jentry % 10000 == 0) cout << "Processed " << jentry << " events out of " <<nentries<< " from " << split*nOverTen << " to "<< finalEntry<<endl;
        hcount->Fill(1);
                hcount->Fill(2,genWeight);
        
        
        bool isMuTau=0;
        bool isEleTau=0;
        bool isMu=0;
        bool isEle=0;
        bool isTau=0;
        
        for (int iele = 0; iele < nEle; ++iele){
            bool IsoEle=elePFChIso->at(iele)/elePt->at(iele);
            if ( (elePFNeuIso->at(iele) + elePFPhoIso->at(iele) - 0.5* elePFPUIso->at(iele))  > 0.0)
                IsoEle= (elePFChIso->at(iele)/elePt->at(iele) + elePFNeuIso->at(iele) + elePFPhoIso->at(iele) - 0.5* elePFPUIso->at(iele))/elePt->at(iele);
            
            
            
            if (elePt->at(iele) > 19 && IsoEle < 0.5)
            {isEle=1;
                hcount->Fill(3);}
        }
        
        for (int imu = 0; imu < nMu; ++imu){
            
            bool IsoMu=muPFChIso->at(imu)/muPt->at(imu);
            if ( (muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu) )  > 0.0)
                IsoMu= ( muPFChIso->at(imu)/muPt->at(imu) + muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu))/muPt->at(imu);
            
            if (muPt->at(imu) > 19 &&  muIsLooseID->at(imu) > 0  && IsoMu < 0.50 )
            {isMu=1;
                hcount->Fill(4);
            }
            
            
        }
        
        
        
        
        for (int itau = 0; itau < nTau; ++itau){
            if (tauPt->at(itau) > 20  && tauCombinedIsolationDeltaBetaCorrRaw3Hits->at(itau) < 3.0 && tauByLooseMuonRejection3->at(itau) &&  tauByMVA5LooseElectronRejection->at(itau) )
                isTau=1;hcount->Fill(5);
        }
        
        if (isMu && isTau) {isMuTau=1; hcount->Fill(6);}
        if (isEle && isTau) {isEleTau=1;hcount->Fill(7);}
        
        if(!(isMuTau) || !(isEleTau)) continue;
        hcount->Fill(8);
        
        MyNewTree->Fill();
        
    }
    MyNewTree->AutoSave();
    //    MyNewTree->Write();
    hPU->Write();
    hPUTrue->Write();
    hEvents->Write();
    hcount->Write();
    file->Close();
}

int main(int argc, char* argv[]){
    TString path=argv[1];
    TString FinaName=argv[2];
    TString number= argv[3];
    int split = atoi(argv[3]);
    //    a=atoi(argv[1]);
    //    b=atoi(argv[2]);atoi or strtod.
    TString outputName = "";
    outputName +="skimed_"+number+"_"+FinaName;
    
    Skimmer t(path + "/" + FinaName);
    t.Loop(outputName,split);
    return 0;
}








