#include "../interface/LQ3Analyzer.h"
#include "../interface/WeightCalculator.h"
#include "../interface/Corrector.h"
#include <string>
#include <ostream>


int main(int argc, char** argv) {
    using namespace std;
    
    std::string out = *(argv + 1);
    
    cout << "\n\n\n OUTPUT NAME IS:    " << out << endl;     //PRINTING THE OUTPUT name
    TFile *fout = TFile::Open(out.c_str(), "RECREATE");
    
    myMap1 = new std::map<std::string, TH1F*>();
    myMap2 = new map<string, TH2F*>();
    
    std::vector<string> input;
    for (int f = 2; f < argc; f++) {
        input.push_back(*(argv + f));
        cout << "\n INPUT NAME IS:   " << input[f - 2] << "\n";
    }
    
    
    TFile * PUData= TFile::Open("../interface/pileup-hists/Data_Pileup_2015D_Nov17.root");
    TH1F * HistoPUData= (TH1F *) PUData->Get("pileup");
    HistoPUData->Scale(1.0/HistoPUData->Integral());
    
    TFile * PUMC= TFile::Open("../interface/pileup-hists/MC_Spring15_PU25_Startup.root");
    TH1F * HistoPUMC= (TH1F *) PUMC->Get("pileup");
    HistoPUMC->Scale(1.0/HistoPUMC->Integral());
    
    TFile * MuCorrId= TFile::Open("../interface/pileup-hists/MuonID_Z_RunCD_Reco74X_Dec1.root");
    TH2F * HistoMuId= (TH2F *) MuCorrId->Get("NUM_MediumID_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio");
    
    TFile * MuCorrIso= TFile::Open("../interface/pileup-hists/MuonIso_Z_RunCD_Reco74X_Dec1.root");
    TH2F * HistoMuIso= (TH2F *) MuCorrIso->Get("NUM_TightRelIso_DEN_MediumID_PAR_pt_spliteta_bin1/pt_abseta_ratio");
    
    TFile * MuCorrTrg= TFile::Open("../interface/pileup-hists/SingleMuonTrigger_Z_RunCD_Reco74X_Dec1.root");
    TH2F * HistoMuTrg= (TH2F *) MuCorrTrg->Get("runD_Mu45_eta2p1_PtEtaBins/pt_abseta_ratio");
    
    
    TFile * ElectronIdIso= TFile::Open("../interface/pileup-hists/Electron_IdIso0p10_eff.root");
    
    TGraphAsymmErrors *	eleMCEnd =  (TGraphAsymmErrors *) ElectronIdIso->Get("ZMassEtaGt1p48_MC");
    TGraphAsymmErrors *	eleMCBar = (TGraphAsymmErrors *) ElectronIdIso->Get("ZMassEtaLt1p48_MC");
    TGraphAsymmErrors *	eleDataEnd =  (TGraphAsymmErrors *) ElectronIdIso->Get("ZMassEtaGt1p48_Data");
    TGraphAsymmErrors *	eleDataBar = (TGraphAsymmErrors *) ElectronIdIso->Get("ZMassEtaLt1p48_Data");
    
    vector<TGraphAsymmErrors *> EleScaleFactor;
    EleScaleFactor.push_back(eleMCEnd);
    EleScaleFactor.push_back(eleMCBar);
    EleScaleFactor.push_back(eleDataEnd);
    EleScaleFactor.push_back(eleDataBar);
    
    
    for (int k = 0; k < input.size(); k++) {
        
        //std::string input = *(argv + 2);
        TFile *f_Double = TFile::Open(input[k].c_str());
        cout << "\n  Now is running on ------->   " << std::string(f_Double->GetName()) << "\n";
        
        std::string InputROOT= std::string(f_Double->GetName());
        TFile * myFile = TFile::Open(f_Double->GetName());
        TH1F * HistoTot = (TH1F*) myFile->Get("hcount");
        
        //        TTree *Run_Tree = (TTree*) f_Double->Get("ggNtuplizer/EventTree");
        TTree *Run_Tree = (TTree*) f_Double->Get("EventTree");
        
        cout.setf(ios::fixed, ios::floatfield);
        cout.precision(6);
        
        
        std::string ROOTLoc= "/Users/abdollah1/GIT_abdollah110/LQ2016/ROOT/V5_FinalSlimmIso03/";
        vector<float> DY_Events = DY_HTBin(ROOTLoc);
        vector<float> W_Events = W_HTBin(ROOTLoc);
        
        /////////////////////////   General Info
        Run_Tree->SetBranchAddress("isData", &isData);
        Run_Tree->SetBranchAddress("run", &run);
        Run_Tree->SetBranchAddress("lumis", &lumis);
        Run_Tree->SetBranchAddress("event", &event);
        Run_Tree->SetBranchAddress("genWeight",&genWeight);
        Run_Tree->SetBranchAddress("HLTEleMuX", &HLTEleMuX);
        Run_Tree->SetBranchAddress("puTrue", &puTrue);
        Run_Tree->SetBranchAddress("nVtx",&nVtx);
        
        /////////////////////////   MC Info
        Run_Tree->SetBranchAddress("mcPID", &mcPID);
        Run_Tree->SetBranchAddress("mcStatus", &mcStatus);
        Run_Tree->SetBranchAddress("mcPt", &mcPt );
        Run_Tree->SetBranchAddress("mcEta", &mcEta );
        Run_Tree->SetBranchAddress("mcPhi", &mcPhi );
        Run_Tree->SetBranchAddress("mcE", &mcE );
        Run_Tree->SetBranchAddress("mcMass", &mcMass );
        
        /////////////////////////   Tau Info
        Run_Tree->SetBranchAddress("nTau", &nTau);
        Run_Tree->SetBranchAddress("tauPt"  ,&tauPt);
        Run_Tree->SetBranchAddress("tauEta"  ,&tauEta);
        Run_Tree->SetBranchAddress("tauPhi"  ,&tauPhi);
        Run_Tree->SetBranchAddress("tauMass"  ,&tauMass);
        Run_Tree->SetBranchAddress("tauCharge"  ,&tauCharge);
        Run_Tree->SetBranchAddress("pfTausDiscriminationByDecayModeFinding", &pfTausDiscriminationByDecayModeFinding);
        Run_Tree->SetBranchAddress("tauByTightMuonRejection3", &tauByTightMuonRejection3);
        Run_Tree->SetBranchAddress("tauByLooseMuonRejection3", &tauByLooseMuonRejection3);
        Run_Tree->SetBranchAddress("tauByMVA5MediumElectronRejection"  ,&tauByMVA5MediumElectronRejection);
        Run_Tree->SetBranchAddress("tauByLooseCombinedIsolationDeltaBetaCorr3Hits",&tauByLooseCombinedIsolationDeltaBetaCorr3Hits);
        Run_Tree->SetBranchAddress("tauByMediumCombinedIsolationDeltaBetaCorr3Hits",&tauByMediumCombinedIsolationDeltaBetaCorr3Hits);
        Run_Tree->SetBranchAddress("tauByMVA5LooseElectronRejection", &tauByMVA5LooseElectronRejection);
        Run_Tree->SetBranchAddress("tauDxy",&tauDxy);
        Run_Tree->SetBranchAddress("tauDecayMode",&tauDecayMode);
        Run_Tree->SetBranchAddress("tauNumSignalPFChargedHadrCands",&tauNumSignalPFChargedHadrCands);
        Run_Tree->SetBranchAddress("tauCombinedIsolationDeltaBetaCorrRaw3Hits",&tauCombinedIsolationDeltaBetaCorrRaw3Hits);

        
        /////////////////////////   Mu Info
        Run_Tree->SetBranchAddress("nMu", &nMu);
        Run_Tree->SetBranchAddress("muPt"  ,&muPt);
        Run_Tree->SetBranchAddress("muEta"  ,&muEta);
        Run_Tree->SetBranchAddress("muPhi"  ,&muPhi);
        Run_Tree->SetBranchAddress("muIsoTrk", &muIsoTrk);
        Run_Tree->SetBranchAddress("muCharge",&muCharge);
        Run_Tree->SetBranchAddress("muIsMediumID",&muIsMediumID);
        Run_Tree->SetBranchAddress("muIsLooseID",&muIsLooseID);
        Run_Tree->SetBranchAddress("muPFChIso", &muPFChIso);
        Run_Tree->SetBranchAddress("muPFPhoIso", &muPFPhoIso);
        Run_Tree->SetBranchAddress("muPFNeuIso", &muPFNeuIso);
        Run_Tree->SetBranchAddress("muPFPUIso", &muPFPUIso);
        Run_Tree->SetBranchAddress("muD0",&muD0);
        Run_Tree->SetBranchAddress("muDz",&muDz);
        
        /////////////////////////   Ele Info
        Run_Tree->SetBranchAddress("nEle", &nEle);
        Run_Tree->SetBranchAddress("elePt"  ,&elePt);
        Run_Tree->SetBranchAddress("eleEta"  ,&eleEta);
        Run_Tree->SetBranchAddress("elePhi"  ,&elePhi);
        Run_Tree->SetBranchAddress("elePFChIso", &elePFChIso);
        Run_Tree->SetBranchAddress("eleIDMVANonTrg", &eleIDMVANonTrg);
        Run_Tree->SetBranchAddress("eleCharge",&eleCharge);
        Run_Tree->SetBranchAddress("eleSCEta",&eleSCEta);
        Run_Tree->SetBranchAddress("elePFChIso", &elePFChIso);
        Run_Tree->SetBranchAddress("elePFPhoIso", &elePFPhoIso);
        Run_Tree->SetBranchAddress("elePFNeuIso", &elePFNeuIso);
        Run_Tree->SetBranchAddress("elePFPUIso", &elePFPUIso);
        Run_Tree->SetBranchAddress("eleD0",&eleD0);
        Run_Tree->SetBranchAddress("eleDz",&eleDz);
        Run_Tree->SetBranchAddress("eleMissHits", &eleMissHits);
        Run_Tree->SetBranchAddress("eleConvVeto", &eleConvVeto);
        
        /////////////////////////   Jet Info
        Run_Tree->SetBranchAddress("nJet",&nJet);
        Run_Tree->SetBranchAddress("jetPt",&jetPt);
        Run_Tree->SetBranchAddress("jetEta",&jetEta);
        Run_Tree->SetBranchAddress("jetPhi",&jetPhi);
        Run_Tree->SetBranchAddress("jetEn",&jetEn);
        Run_Tree->SetBranchAddress("jetpfCombinedInclusiveSecondaryVertexV2BJetTags",&jetpfCombinedInclusiveSecondaryVertexV2BJetTags);
        Run_Tree->SetBranchAddress("jetPFLooseId",&jetPFLooseId);
        Run_Tree->SetBranchAddress("jetPUidFullDiscriminant",&jetPUidFullDiscriminant);
        /////////////////////////   MET Info
        Run_Tree->SetBranchAddress("pfMET",&pfMET);
        Run_Tree->SetBranchAddress("pfMETPhi",&pfMETPhi);
        Run_Tree->SetBranchAddress("genHT",&genHT);
        
        
        //###############################################################################################
        //  Weight Calculation
        //###############################################################################################
        float WSCALEFACTORE=1.3;
        float MuMass= 0.10565837;
        float eleMass= 0.000511;
        float LeptonPtCut_=50;
        float TauPtCut_=50;
        float JetPtCut=30;
        float BJetPtCut=30;
        float LooseCSV= 0.605;                    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation74X
        float LeptonIsoCut=0.10;
        
        
        
        Int_t nentries_wtn = (Int_t) Run_Tree->GetEntries();
        cout<<"nentries_wtn===="<<nentries_wtn<<"\n";
        for (Int_t i = 0; i < nentries_wtn; i++) {
            //        for (Int_t i = 0; i < 50000; i++) {
            Run_Tree->GetEntry(i);
            if (i % 10000 == 0) fprintf(stdout, "\r  Processed events: %8d of %8d ", i, nentries_wtn);
            fflush(stdout);
            
            
            
            
            //###############################################################################################
            //  Weight Calculation
            //###############################################################################################
            
            //############ Top Reweighting
            float GenTopPt=0;
            float GenAntiTopPt=0;
            float TopPtReweighting = 1;
            for (int igen=0;igen < nMC; igen++){
                if (mcPID->at(igen) == 6 && mcStatus->at(igen) ==62) GenTopPt=mcPt->at(igen) ;
                if (mcPID->at(igen) == -6 && mcStatus->at(igen) ==62) GenAntiTopPt=mcPt->at(igen);
            }
            size_t isTTJets = InputROOT.find("TTJets");
            if (isTTJets!= string::npos) TopPtReweighting = compTopPtWeight(GenTopPt, GenAntiTopPt);
            //###############################################################################################
            float LumiWeight = 1;
            float GetGenWeight=1;
            float PUWeight = 1;
            
            if (!isData){
                
                if (HistoTot) LumiWeight = weightCalc(HistoTot, InputROOT, genHT, W_Events, DY_Events);
                GetGenWeight=genWeight;
                
                int puNUmmc=int(puTrue->at(0)*10);
                int puNUmdata=int(puTrue->at(0)*10);
                float PUMC_=HistoPUMC->GetBinContent(puNUmmc+1);
                float PUData_=HistoPUData->GetBinContent(puNUmdata+1);
                PUWeight= PUData_/PUMC_;
            }
            float TotalWeight = LumiWeight * GetGenWeight * PUWeight * TopPtReweighting;
            //###############################################################################################
            //  Histogram Filling
            //###############################################################################################
            plotFill("WeightLumi",LumiWeight,10000,0,100);
            //            plotFill("WeightGen",GetGenWeight,1000000,0,1000000);
            plotFill("WeightPU",PUWeight,100,0,10);
            //            plotFill("WeightTotal",TotalWeight,50,0,5);
            plotFill("nVtx_NoPUCorr",nVtx,60,0,60);
            plotFill("nVtx_PUCorr",nVtx,60,0,60,PUWeight);
            for (int qq=0; qq < 50;qq++){
                if ((HLTEleMuX >> qq & 1) == 1)
                    plotFill("HLT",qq,50,0,50);
            }
            //###############################################################################################
            size_t isSingleMu = InputROOT.find("SingleMu");
            size_t isSingleEle = InputROOT.find("SingleEle");
//            size_t isTTJets = InputROOT.find("TTJets");
            size_t isWJets = InputROOT.find("WJets");
//            //###############################################################################################
//            //  Doing MuTau Analysis
//            //###############################################################################################
//            bool DoMuTauAnalysis=0;
//            
//            if (DoMuTauAnalysis &&   isSingleEle== string::npos) {
//                
//                //Loop over MuTau events
//                for  (int imu=0 ; imu < nMu; imu++){
//                    for  (int itau=0 ; itau < nTau; itau++){
//                        
//                        
//                        float IsoMu=muPFChIso->at(imu)/muPt->at(imu);
//                        if ( (muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu) )  > 0.0)
//                            IsoMu= ( muPFChIso->at(imu)/muPt->at(imu) + muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu))/muPt->at(imu);
//                        
//                        bool MuPtCut = muPt->at(imu) > LeptonPtCut_ && fabs(muEta->at(imu)) < 2.1 ;
//                        bool MuIdIso=(muIsMediumID->at(imu) > 0  && fabs(muD0->at(imu)) < 0.045 && fabs(muDz->at(imu)) < 0.2);
//                        bool TauPtCut = tauPt->at(itau) > TauPtCut_  && fabs(tauEta->at(itau)) < 2.3 ;
//                        bool TauIdIso =  tauByTightMuonRejection3->at(itau) > 0 && tauByMVA5LooseElectronRejection->at(itau) > 0 && fabs(tauDxy->at(itau)) < 0.05;
////                        bool TauIdIso =  tauByTightMuonRejection3->at(itau) > 0 && tauByMVA5LooseElectronRejection->at(itau) > 0 && fabs(tauDxy->at(itau)) < 0.05 && (tauDecayMode->at(itau) < 3 || tauDecayMode->at(itau) > 8);
//                        
//                        
//                        float muCorr=getCorrFactorMuon74X(isData,  muPt->at(imu), muEta->at(imu) , HistoMuId,HistoMuIso,HistoMuTrg);
//                        float TotalWeight = LumiWeight * GetGenWeight * PUWeight * muCorr;
//                        float NewTotalWeight=TotalWeight;
//                        
//                        
//                        TLorentzVector Mu4Momentum, Tau4Momentum, Z4Momentum, Jet4Momentum,ExtraMu4Momentum, ExtraEle4Momentum,KJet4Momentum;
//                        Mu4Momentum.SetPtEtaPhiM(muPt->at(imu),muEta->at(imu),muPhi->at(imu),MuMass);
//                        Tau4Momentum.SetPtEtaPhiM(tauPt->at(itau),tauEta->at(itau),tauPhi->at(itau),tauMass->at(itau));
//                        Z4Momentum=Mu4Momentum+Tau4Momentum;
//                        
//                        
//                        
//                        //###########      Finding the close jet near tau   ###########################################################
//                        float CLoseJetTauPt=tauPt->at(itau);
//                        float CLoseJetTauEta=tauEta->at(itau);
//                        float CLoseJetMuPt=muPt->at(imu);
//                        float CLoseJetMuEta=muEta->at(imu);
//                        
//                        if (TauPtCut&& TauIdIso && MuPtCut && MuIdIso ){
//                            double Refer_R_jettau = 5;
//                            double Refer_R_jetmu = 5;
//                            
//                            for (int kjet= 0 ; kjet < nJet ; kjet++){
//                                KJet4Momentum.SetPtEtaPhiE(jetPt->at(kjet),jetEta->at(kjet),jetPhi->at(kjet),jetEn->at(kjet));
//                                
//                                if (KJet4Momentum.DeltaR(Tau4Momentum) < Refer_R_jettau) {
//                                    Refer_R_jettau = KJet4Momentum.DeltaR(Tau4Momentum);
//                                    if (Refer_R_jettau < 0.5 && jetPt->at(kjet)  >= tauPt->at(itau)) {
//                                        CLoseJetTauPt = jetPt->at(kjet);
//                                        CLoseJetTauEta = jetEta->at(kjet);
//                                        
//                                    }
//                                    
//                                    
//                                }
//                                
//                                if (KJet4Momentum.DeltaR(Mu4Momentum) < Refer_R_jetmu) {
//                                    Refer_R_jetmu = KJet4Momentum.DeltaR(Mu4Momentum);
//                                    if (Refer_R_jetmu < 0.5 && jetPt->at(kjet)  >= muPt->at(imu)) {
//                                        CLoseJetMuPt = jetPt->at(kjet);
//                                        CLoseJetMuEta = jetEta->at(kjet);
//                                        
//                                    }
//                                    
//                                }
//                                
//                                
//                            }
//                        }
//                        
//                        
//                        //###########      Extra Mu Veto   ###########################################################
//                        bool extraMuonExist= false;
//                        for  (int jmu=0 ; jmu < nMu; jmu++){
//                            ExtraMu4Momentum.SetPtEtaPhiM(muPt->at(jmu),muEta->at(jmu),muPhi->at(jmu),MuMass);
//                            
//                            if (ExtraMu4Momentum.DeltaR(Mu4Momentum) < 0.5  || ExtraMu4Momentum.DeltaR(Tau4Momentum) < 0.5 ) continue;
//                            if  ( muPt->at(jmu) < 15 ||  fabs(muEta->at(jmu)) > 2.4 ) continue ;
//                            
//                            float IsoMuExtra=muPFChIso->at(jmu)/muPt->at(jmu);
//                            if ( (muPFNeuIso->at(jmu) + muPFPhoIso->at(jmu) - 0.5* muPFPUIso->at(jmu) )  > 0.0)
//                                IsoMuExtra= ( muPFChIso->at(jmu)/muPt->at(jmu) + muPFNeuIso->at(jmu) + muPFPhoIso->at(jmu) - 0.5* muPFPUIso->at(jmu))/muPt->at(jmu);
//                            
//                            if (! (muIsLooseID->at(jmu) > 0 && IsoMuExtra < 0.30) ) continue;
//                            
//                            extraMuonExist=true;
//                        }
//                        //###########      Extra Ele Veto   ###########################################################
//                        
//                        bool extraElectronExist= false;
//                        for  (int jele=0 ; jele < nEle; jele++){
//                            ExtraEle4Momentum.SetPtEtaPhiM(elePt->at(jele),eleEta->at(jele),elePhi->at(jele),eleMass);
//                            
//                            if (ExtraEle4Momentum.DeltaR(Mu4Momentum) < 0.5  || ExtraEle4Momentum.DeltaR(Tau4Momentum) < 0.5 ) continue;
//                            if ( elePt->at(jele) < 15 || fabs(eleEta->at(jele)) > 2.5) continue;
//                            
//                            float IsoEleExtra=elePFChIso->at(jele)/elePt->at(jele);
//                            if ( (elePFNeuIso->at(jele) + elePFPhoIso->at(jele) - 0.5* elePFPUIso->at(jele))  > 0.0)
//                                IsoEleExtra= (elePFChIso->at(jele)/elePt->at(jele) + elePFNeuIso->at(jele) + elePFPhoIso->at(jele) - 0.5* elePFPUIso->at(jele))/elePt->at(jele);
//                            
//                            bool eleMVAIdExtra= false;
//                            if (fabs (eleSCEta->at(jele)) < 0.8 && eleIDMVANonTrg->at(jele) >  0.913286 ) eleMVAIdExtra= true;
//                            else if (fabs (eleSCEta->at(jele)) >  0.8 &&fabs (eleSCEta->at(jele)) <  1.5 && eleIDMVANonTrg->at(jele) >  0.805013 ) eleMVAIdExtra= true;
//                            else if ( fabs (eleSCEta->at(jele)) >  1.5 && eleIDMVANonTrg->at(jele) >  0.358969  ) eleMVAIdExtra= true;
//                            else eleMVAIdExtra= false;
//                            
//                            
//                            if (!(eleMVAIdExtra && eleMissHits->at(jele) < 2 && eleConvVeto->at(jele) && IsoEleExtra < 0.30)) continue;
//                            extraElectronExist= true;
//                            
//                        }
//                        
//                        //###########      General   ###########################################################
//                        
//                        bool  GeneralMuTauSelection=  !extraMuonExist && !extraElectronExist && MuPtCut && TauPtCut && MuIdIso && TauIdIso && Mu4Momentum.DeltaR(Tau4Momentum) > 0.5;
//                        
//                        
//                        //###########      Jet definition   ###########################################################
//                        vector<TLorentzVector> JetVector;
//                        vector<TLorentzVector> BJetBVector;
//                        vector<TLorentzVector> BJet20Vector;
//                        JetVector.clear();
//                        BJetBVector.clear();
//                        BJet20Vector.clear();
//                        
//                        for (int ijet= 0 ; ijet < nJet ; ijet++){
//                            Jet4Momentum.SetPtEtaPhiE(jetPt->at(ijet),jetEta->at(ijet),jetPhi->at(ijet),jetEn->at(ijet));
//                            //cout << jetPFLooseId->at(ijet)  << "   pu    "<< jetPUidFullDiscriminant->at(ijet)<<"\n";
//                            
//                            if (jetPFLooseId->at(ijet) > 0.5 && jetPt->at(ijet) > JetPtCut && fabs(jetEta->at(ijet)) < 2.4 && Jet4Momentum.DeltaR(Tau4Momentum) > 0.5 && Jet4Momentum.DeltaR(Mu4Momentum) > 0.5 ){
//                                JetVector.push_back(Jet4Momentum);
//                                if (jetpfCombinedInclusiveSecondaryVertexV2BJetTags->at(ijet) >  LooseCSV  ){
//                                    BJetBVector.push_back(Jet4Momentum);
//                                }
//                            }
//                            if (jetPFLooseId->at(ijet) > 0.5 && jetPt->at(ijet) > BJetPtCut && fabs(jetEta->at(ijet)) < 2.4 && Jet4Momentum.DeltaR(Tau4Momentum) > 0.5 && Jet4Momentum.DeltaR(Mu4Momentum) > 0.5 && jetpfCombinedInclusiveSecondaryVertexV2BJetTags->at(ijet) >  LooseCSV ){
//                                BJet20Vector.push_back(Jet4Momentum);
//                            }
//                            
//                        }
//                        
//                        
//                        float M_muj0,M_muj1,M_tauj0,M_tauj1, M_MuJet,M_TauJet,ST_DiJet,ST_MET =0;
//                        
//                        bool DiJet_Selection=JetVector.size() > 1;
//                        bool DiNonBJet_Selection=JetVector.size() > 1 && BJet20Vector.size() < 1 ;
//                        bool JetBJet_Selection=JetVector.size() > 1& BJetBVector.size()> 0 && (BJetBVector[0].Pt()== JetVector[0].Pt() || BJetBVector[0].Pt() ==JetVector[1].Pt());
//                        
//                        if (DiJet_Selection){
//                            ST_DiJet=JetVector[0].Pt()+JetVector[1].Pt()+muPt->at(imu)+tauPt->at(itau);
//                            ST_MET=JetVector[0].Pt()+JetVector[1].Pt()+muPt->at(imu)+tauPt->at(itau)+pfMET;
//
//                            
//                            M_muj0= (Mu4Momentum+JetVector[0]).M();
//                            M_muj1= (Mu4Momentum+JetVector[1]).M();
//                            M_tauj0= (Tau4Momentum+JetVector[0]).M();
//                            M_tauj1= (Tau4Momentum+JetVector[1]).M();
//                            
//                            M_MuJet=M_muj0;
//                            M_TauJet=M_tauj1;
//                            if ( fabs(M_muj0-M_tauj1) > fabs(M_muj1-M_tauj0)){
//                                M_MuJet=M_muj1;
//                                M_TauJet=M_tauj0;
//                                
//                            }
//                        }
//                        
//                        
//                        
//                        
//                        //###############################################################################################
//                        //  Tau Lep Charge Categorization
//                        //###############################################################################################
//                        const int size_Q = 3;
//                                            bool charge_No = 1;
//                        bool charge_OS = muCharge->at(imu) * tauCharge->at(itau) < 0;
//                        bool charge_SS = muCharge->at(imu) * tauCharge->at(itau) > 0;
//                        bool charge_category[size_Q] = {charge_No,charge_OS, charge_SS};
//                        std::string q_Cat[size_Q] = {"","_OS", "_SS"};
//                        
//                        //###############################################################################################
//                        //  Isolation Categorization
//                        //###############################################################################################
//                        //###############################################################################################
//                        //  Isolation Categorization
//                        //###############################################################################################
//                        const int size_isoCat = 9;
//                        bool Isolation = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) > 0.5 && IsoMu < LeptonIsoCut;
//                        bool AntiIsolation = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) < 0.5 && IsoMu >= LeptonIsoCut;
//                        bool TauIsoLepAntiIso = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) > 0.5 && IsoMu >= LeptonIsoCut;
//                        bool TauAntiIsoLepIso = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) < 0.5 && IsoMu < LeptonIsoCut;
//                        bool TauIso = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) > LeptonIsoCut ;
//                        bool TauAntiIso = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) < LeptonIsoCut ;
//                        bool LepIso = IsoMu < LeptonIsoCut;
//                        bool LepAntiIso = IsoMu >= LeptonIsoCut;
//                        bool Total = 1;
//                        
//                        
//                        bool Iso_category[size_isoCat] = {Isolation, AntiIsolation,TauIsoLepAntiIso,TauAntiIsoLepIso,TauIso,TauAntiIso,LepIso,LepAntiIso,Total};
//
//                        
//                        std::string iso_Cat[size_isoCat] = {
//                            "", "_AntiIso","_TauIsoLepAntiIso","_TauAntiIsoLepIso","_TauIso","TauAntiIso","_LepIso","_LepAntiIso","_Total"};
//                        //###############################################################################################
//                        //  MT Categorization
//                        //###############################################################################################
//                        float tmass= TMass_F(muPt->at(imu), muPt->at(imu)*cos(muPhi->at(imu)),muPt->at(imu)*sin(muPhi->at(imu)) , pfMET, pfMETPhi);
//                        const int size_mTCat = 1;
//                        bool NoMT = 1;
//                        bool LoWMT = tmass < 30;
//                        bool HighMT = tmass > 70;
//                        //                        bool MT_category[size_mTCat] = {NoMT,LoWMT,HighMT};
//                        //                        std::string MT_Cat[size_mTCat] = {"", "_LowMT","_HighMT"};
//                        bool MT_category[size_mTCat] = {NoMT};
//                        std::string MT_Cat[size_mTCat] = {""};
//                        
//                        //###############################################################################################
//                        //  Trigger Categorization
//                        //###############################################################################################
//                        //                        else if (name.find("HLT_Mu45_eta2p1_v") != string::npos) bitEleMuX = 26;
//                        const int size_trgCat = 1;
//                        bool PassTrigger = (HLTEleMuX >> 26 & 1) == 1; // Exist both in data and MC HLT_IsoMu27_v
//                        //                        bool PassTrigger = (HLTEleMuX >> 25 & 1) == 1; // Exist both in data and MC HLT_IsoMu27_v
//                        //                  bool PassTrigger = ((HLTEleMuX >> 29 & 1) == 1 && !isData) || ((HLTEleMuX >> 30 & 1) == 1 && isData); //IsoMu17_eta2p1 MC && IsoMu18 Data
//                        bool NoTrigger = 1;
//                        //                    bool Trigger_category[size_trgCat] = {PassTrigger, NoTrigger};
//                        //                    std::string trg_Cat[size_trgCat] = {"", "_NoTrigger"};
//                        bool Trigger_category[size_trgCat] = {PassTrigger};
//                        std::string trg_Cat[size_trgCat] = {""};
//                        
//                        //###############################################################################################
//                        //  ST Categorization
//                        //###############################################################################################
//                        const int size_ST = 2;
//                        bool ST_category[size_ST] = {JetBJet_Selection,DiJet_Selection};
//                        std::string ST_Cat[size_ST] = {"_JetBJet","_DiJet"};
////                        float TTScaleFactor[size_ST]={0.88,0.94};
//                        float TTScaleFactor[size_ST]={1.00,1.00};
//                        
//                        
//                        //###############################################################################################
//                        
//                        
//                        if (GeneralMuTauSelection){
//                            plotFill("Weight_Mu",muCorr,200,0,2);
//                            plotFill("TotalWeight_Mu",TotalWeight,1000,0,10);
//                            plotFill("TotalNonLumiWeight_Mu",TotalWeight/LumiWeight,1000,0,10);                            
//                            
//                            for (int qcat = 0; qcat < size_Q; qcat++) {
//                                if (charge_category[qcat]) {
//                                    for (int iso = 0; iso < size_isoCat; iso++) {
//                                        if (Iso_category[iso]) {
//                                            for (int imt = 0; imt < size_mTCat; imt++) {
//                                                if (MT_category[imt]) {
//                                                    for (int ist = 0; ist < size_ST; ist++) {
//                                                        if (ST_category[ist]) {
//                                                            
//                                                            if (isTTJets!= string::npos) NewTotalWeight=TotalWeight * TTScaleFactor[ist];  // Add TT scale factor
//                                                            if (isWJets!= string::npos) NewTotalWeight=TotalWeight * WSCALEFACTORE;  // Add W scale factor
//                                                            
//                                                            for (int trg = 0; trg < size_trgCat; trg++) {
//                                                                
//                                                                if (Trigger_category[trg]) {
//                                                                    
//                                                                    
//                                                                    std::string FullStringName = MT_Cat[imt] +q_Cat[qcat] + iso_Cat[iso] + trg_Cat[trg] +ST_Cat[ist];
//
//                                                                    plotFill("MuTau_tauDecayMode"+FullStringName,tauDecayMode->at(itau),12,0,12,NewTotalWeight);
//                                                                    plotFill("MuTau_tauNumSignalPFChargedHadrCands"+FullStringName,tauNumSignalPFChargedHadrCands->at(itau),5,0,5,NewTotalWeight);
//                                                                    
//                                                                    plotFill("MuTau_tmass"+FullStringName,tmass,500,0,500,NewTotalWeight);
//                                                                    plotFill("MuTau_VisMass"+FullStringName,Z4Momentum.M(),500,0,500,NewTotalWeight);
//                                                                    plotFill("MuTau_LepPt"+FullStringName,muPt->at(imu),300,0,300,NewTotalWeight);
//                                                                    plotFill("MuTau_LepIso"+FullStringName,IsoMu,100,0,10,NewTotalWeight);
//                                                                    plotFill("MuTau_LepEta"+FullStringName,muEta->at(imu),100,-2.5,2.5,NewTotalWeight);
//                                                                    plotFill("MuTau_TauPt"+FullStringName,tauPt->at(itau),200,0,200,NewTotalWeight);
//                                                                    plotFill("MuTau_TauEta"+FullStringName,tauEta->at(itau),100,-2.5,2.5,NewTotalWeight);
//                                                                    plotFill("MuTau_CloseJetTauPt"+FullStringName,CLoseJetTauPt,500,0,500,NewTotalWeight);
//                                                                    plotFill("MuTau_NumJet"+FullStringName,JetVector.size(),10,0,10,NewTotalWeight);
//                                                                    plotFill("MuTau_NumBJet"+FullStringName,BJetBVector.size(),10,0,10,NewTotalWeight);
//                                                                    plotFill("MuTau_nVtx"+FullStringName,nVtx,50,0,50,NewTotalWeight);
//                                                                    plotFill("MuTau_nVtx_NoPU"+FullStringName,nVtx,50,0,50,NewTotalWeight / PUWeight);
//                                                                    plotFill("MuTau_MET"+FullStringName,pfMET,500,0,500,NewTotalWeight);
//                                                                    plotFill("MuTau_M_taujet"+FullStringName,M_TauJet,1000,0,1000,NewTotalWeight);
//                                                                    if (JetVector.size() > 1) plotFill("MuTau_LeadJetPt"+FullStringName,JetVector[0].Pt(),300,0,300,NewTotalWeight);
//                                                                    if (JetVector.size() > 1) plotFill("MuTau_SubLeadJetPt"+FullStringName,JetVector[1].Pt(),300,0,300,NewTotalWeight);
//                                                                    plotFill("MuTau_ST_DiJet"+FullStringName,ST_DiJet,100,0,1000,NewTotalWeight);
//                                                                    plotFill("MuTau_ST_MET"+FullStringName,ST_MET,100,0,1000,NewTotalWeight);
//                                                                    
//                                                                    
//                                                                }
//                                                            }
//                                                        }
//                                                    }
//                                                }
//                                            }
//                                        }
//                                    }
//                                }
//                            }
//                        }
//                    }
//                }
//            }
            
            //###############################################################################################
            //  Doing EleTau Analysis
            //###############################################################################################
            bool DoEleTauAnalysis=1;
            if (DoEleTauAnalysis  &&   isSingleMu== string::npos) {
                
                
                
                //loop over eleTau Channels
                
                for  (int iele=0 ; iele < nEle; iele++){
                    for  (int itau=0 ; itau < nTau; itau++){
                        
                        
                        float IsoEle=elePFChIso->at(iele)/elePt->at(iele);
                        if ( (elePFNeuIso->at(iele) + elePFPhoIso->at(iele) - 0.5* elePFPUIso->at(iele))  > 0.0)
                            IsoEle= (elePFChIso->at(iele)/elePt->at(iele) + elePFNeuIso->at(iele) + elePFPhoIso->at(iele) - 0.5* elePFPUIso->at(iele))/elePt->at(iele);
                        
                        bool eleMVAId= false;
                        if (fabs (eleSCEta->at(iele)) < 0.8 && eleIDMVANonTrg->at(iele) > 0.967083) eleMVAId= true;
                        else if (fabs (eleSCEta->at(iele)) >  0.8 &&fabs (eleSCEta->at(iele)) <  1.5 && eleIDMVANonTrg->at(iele) > 0.929117) eleMVAId= true;
                        else if ( fabs (eleSCEta->at(iele)) >  1.5 && eleIDMVANonTrg->at(iele) > 0.726311 ) eleMVAId= true;
                        else eleMVAId= false;
//                        bool eleMVAId= true;
                        
                        TLorentzVector Ele4Momentum, Tau4Momentum, Z4Momentum, Jet4Momentum,ExtraMu4Momentum, ExtraEle4Momentum,KJet4Momentum;
                        Ele4Momentum.SetPtEtaPhiM(elePt->at(iele),eleEta->at(iele),elePhi->at(iele),eleMass);
                        Tau4Momentum.SetPtEtaPhiM(tauPt->at(itau),tauEta->at(itau),tauPhi->at(itau),tauMass->at(itau));
                        Z4Momentum=Ele4Momentum+Tau4Momentum;
                        
                        
                        bool ElePtCut = elePt->at(iele) > LeptonPtCut_ && fabs(eleEta->at(iele)) < 2.1 ;
                        bool TauPtCut = tauPt->at(itau) > TauPtCut_  && fabs(tauEta->at(itau)) < 2.3 ;
                        bool EleIdIso= (eleMVAId && eleMissHits->at(iele) < 2 && eleConvVeto->at(iele));
                        bool TauIdIso =  tauByLooseMuonRejection3->at(itau) > 0 && tauByMVA5MediumElectronRejection->at(itau) > 0 && fabs(tauDxy->at(itau)) < 0.05;
//                        bool TauIdIso =  tauByLooseMuonRejection3->at(itau) > 0 &&  fabs(tauDxy->at(itau)) < 0.05; // Removing antiElectron Medium
//                        bool TauIdIso =  tauByLooseMuonRejection3->at(itau) > 0 && tauByMVA5MediumElectronRejection->at(itau) > 0 && fabs(tauDxy->at(itau)) < 0.05 && (tauDecayMode->at(itau) < 3 || tauDecayMode->at(itau) > 8);;
                        
                        
                        
                        float eleCorr=getCorrFactorElectron74X(isData,  elePt->at(iele), eleEta->at(iele) , EleScaleFactor);
                        float TotalWeight = LumiWeight * GetGenWeight * PUWeight * eleCorr;
                        float NewTotalWeight=TotalWeight;
                        
                        
                        //###########      Finding the close jet near tau   ###########################################################
                        float CLoseJetTauPt=tauPt->at(itau);
                        float CLoseJetTauEta=tauEta->at(itau);
                        float CLoseJetElePt=elePt->at(iele);
                        float CLoseJetEleEta=eleEta->at(iele);
                        
                        if (TauPtCut&& TauIdIso && ElePtCut && EleIdIso ){
                            double Refer_R_jettau = 5;
                            double Refer_R_jetele = 5;
                            
                            for (int kjet= 0 ; kjet < nJet ; kjet++){
                                KJet4Momentum.SetPtEtaPhiE(jetPt->at(kjet),jetEta->at(kjet),jetPhi->at(kjet),jetEn->at(kjet));
                                
                                if (KJet4Momentum.DeltaR(Tau4Momentum) < Refer_R_jettau) {
                                    Refer_R_jettau = KJet4Momentum.DeltaR(Tau4Momentum);
                                    if (Refer_R_jettau < 0.5 && jetPt->at(kjet)  >= tauPt->at(itau)) {
                                        CLoseJetTauPt = jetPt->at(kjet);
                                        CLoseJetTauEta = jetEta->at(kjet);
                                        
                                    }
                                    
                                    
                                }
                                
                                if (KJet4Momentum.DeltaR(Ele4Momentum) < Refer_R_jetele) {
                                    Refer_R_jetele = KJet4Momentum.DeltaR(Ele4Momentum);
                                    if (Refer_R_jetele < 0.5 && jetPt->at(kjet)  >= elePt->at(iele)) {
                                        CLoseJetElePt = jetPt->at(kjet);
                                        CLoseJetEleEta = jetEta->at(kjet);
                                        
                                    }
                                }
                            }
                        }
                        
                        
                        //###########      Extra Mu Veto   ###########################################################
                        bool extraMuonExist= false;
                        for  (int jmu=0 ; jmu < nMu; jmu++){
                            
                            ExtraMu4Momentum.SetPtEtaPhiM(muPt->at(jmu),muEta->at(jmu),muPhi->at(jmu),MuMass);
                            
                            if (ExtraMu4Momentum.DeltaR(Ele4Momentum) < 0.5  || ExtraMu4Momentum.DeltaR(Tau4Momentum) < 0.5 ) continue;
                            if  ( muPt->at(jmu) < 15 ||  fabs(muEta->at(jmu)) > 2.4 ) continue ;
                            
                            float IsoMuExtra=muPFChIso->at(jmu)/muPt->at(jmu);
                            if ( (muPFNeuIso->at(jmu) + muPFPhoIso->at(jmu) - 0.5* muPFPUIso->at(jmu) )  > 0.0)
                                IsoMuExtra= ( muPFChIso->at(jmu)/muPt->at(jmu) + muPFNeuIso->at(jmu) + muPFPhoIso->at(jmu) - 0.5* muPFPUIso->at(jmu))/muPt->at(jmu);
                            
                            if (! (muIsLooseID->at(jmu) > 0 && IsoMuExtra < 0.30) ) continue;
                            
                            extraMuonExist=true;
                        }
                        //###########      Extra Ele Veto   ###########################################################
                        
                        bool extraElectronExist= false;
                        for  (int jele=0 ; jele < nEle; jele++){
                            
                            ExtraEle4Momentum.SetPtEtaPhiM(elePt->at(jele),eleEta->at(jele),elePhi->at(jele),eleMass);
                            
                            if (ExtraEle4Momentum.DeltaR(Ele4Momentum) < 0.5  || ExtraEle4Momentum.DeltaR(Tau4Momentum) < 0.5 ) continue;
                            if ( elePt->at(jele) < 15 || fabs(eleEta->at(jele)) > 2.5) continue;
                            
                            float IsoEleExtra=elePFChIso->at(jele)/elePt->at(jele);
                            if ( (elePFNeuIso->at(jele) + elePFPhoIso->at(jele) - 0.5* elePFPUIso->at(jele))  > 0.0)
                                IsoEleExtra= (elePFChIso->at(jele)/elePt->at(jele) + elePFNeuIso->at(jele) + elePFPhoIso->at(jele) - 0.5* elePFPUIso->at(jele))/elePt->at(jele);
                            
                            bool eleMVAIdExtra= false;
                            if (fabs (eleSCEta->at(jele)) < 0.8 && eleIDMVANonTrg->at(jele) >  0.913286 ) eleMVAIdExtra= true;
                            else if (fabs (eleSCEta->at(jele)) >  0.8 &&fabs (eleSCEta->at(jele)) <  1.5 && eleIDMVANonTrg->at(jele) >  0.805013 ) eleMVAIdExtra= true;
                            else if ( fabs (eleSCEta->at(jele)) >  1.5 && eleIDMVANonTrg->at(jele) >  0.358969  ) eleMVAIdExtra= true;
                            else eleMVAIdExtra= false;
                            
                            
                            if (!(eleMVAIdExtra && eleMissHits->at(jele) < 2 && eleConvVeto->at(jele) && IsoEleExtra < 0.30)) continue;
                            extraElectronExist= true;
                            
                        }
                        
                        //###########      General  ###########################################################
                        
                        bool GeneralEleTauSelection=  !extraMuonExist && !extraElectronExist && ElePtCut && TauPtCut && EleIdIso && TauIdIso  && Ele4Momentum.DeltaR(Tau4Momentum) > 0.5;
                        
                        //###########      Jet definition   ###########################################################
                        vector<TLorentzVector> JetVector;
                        vector<TLorentzVector> BJetBVector;
                        vector<TLorentzVector> BJet20Vector;
                        JetVector.clear();
                        BJetBVector.clear();
                        BJet20Vector.clear();
                        
                        for (int ijet= 0 ; ijet < nJet ; ijet++){
                            Jet4Momentum.SetPtEtaPhiE(jetPt->at(ijet),jetEta->at(ijet),jetPhi->at(ijet),jetEn->at(ijet));
                            //cout << jetPFLooseId->at(ijet)  << "   pu    "<< jetPUidFullDiscriminant->at(ijet)<<"\n";
                            if (jetPFLooseId->at(ijet) > 0.5 && jetPt->at(ijet) > JetPtCut && fabs(jetEta->at(ijet)) < 2.4 && Jet4Momentum.DeltaR(Tau4Momentum) > 0.5 && Jet4Momentum.DeltaR(Ele4Momentum) > 0.5 ){
                                JetVector.push_back(Jet4Momentum);
                                if (jetpfCombinedInclusiveSecondaryVertexV2BJetTags->at(ijet) >  LooseCSV  ){
                                    BJetBVector.push_back(Jet4Momentum);
                                }
                            }
                            if (jetPFLooseId->at(ijet) > 0.5 && jetPt->at(ijet) > BJetPtCut && fabs(jetEta->at(ijet)) < 2.4 && Jet4Momentum.DeltaR(Tau4Momentum) > 0.5 && Jet4Momentum.DeltaR(Ele4Momentum) > 0.5 && jetpfCombinedInclusiveSecondaryVertexV2BJetTags->at(ijet) >  LooseCSV ){
                                BJet20Vector.push_back(Jet4Momentum);
                            }
                        }
                        
                        
                        float M_elej0,M_elej1,M_tauj0,M_tauj1, M_EleJet,M_TauJet,ST_DiJet,ST_MET=0;
                        
//                        bool DiJet_Selection=JetVector.size() > 1;
                        bool DiJet_Selection=JetVector.size() > -1;
                        bool DiNonBJet_Selection=JetVector.size() > 1 && BJet20Vector.size() < 1 ;
//                        bool JetBJet_Selection=JetVector.size() > 1& BJetBVector.size()> 0 && (BJetBVector[0].Pt()== JetVector[0].Pt() || BJetBVector[0].Pt() ==JetVector[1].Pt());
                        bool JetBJet_Selection=JetVector.size() > -1 ;
                        
                        
//                        if (DiJet_Selection){
//                            ST_DiJet=JetVector[0].Pt()+JetVector[1].Pt()+elePt->at(iele)+tauPt->at(itau);
//                            ST_MET=JetVector[0].Pt()+JetVector[1].Pt()+elePt->at(iele)+tauPt->at(itau)+pfMET;
//                            
//                            M_elej0= (Ele4Momentum+JetVector[0]).M();
//                            M_elej1= (Ele4Momentum+JetVector[1]).M();
//                            M_tauj0= (Tau4Momentum+JetVector[0]).M();
//                            M_tauj1= (Tau4Momentum+JetVector[1]).M();
//                            
//                            M_EleJet=M_elej0;
//                            M_TauJet=M_tauj1;
//                            if ( fabs(M_elej0-M_tauj1) > fabs(M_elej1-M_tauj0)){
//                                M_EleJet=M_elej1;
//                                M_TauJet=M_tauj0;
//                                
//                            }
//                        }
                        
                        
                        
                        
                        //###############################################################################################
                        //  Tau Lep Charge Categorization
                        //###############################################################################################
                        const int size_Q = 3;
                        bool charge_No = 1;
                        bool charge_OS = eleCharge->at(iele) * tauCharge->at(itau) < 0;
                        bool charge_SS = eleCharge->at(iele) * tauCharge->at(itau) > 0;
                        bool charge_category[size_Q] = {charge_No,charge_OS, charge_SS};
                        std::string q_Cat[size_Q] = {"","_OS", "_SS"};
                        
                        //###############################################################################################
                        // Isolation Categorization
                        //###############################################################################################
//                        const int size_isoCat = 9;
//                        bool Isolation = tauCombinedIsolationDeltaBetaCorrRaw3Hits->at(itau) < 3.5 && IsoEle < LeptonIsoCut;
//                        bool AntiIsolation = tauCombinedIsolationDeltaBetaCorrRaw3Hits->at(itau) > 3.5 && IsoEle >= LeptonIsoCut;
//                        bool TauIsoLepAntiIso = tauCombinedIsolationDeltaBetaCorrRaw3Hits->at(itau) < 3.5 && IsoEle >= LeptonIsoCut;
//                        bool TauAntiIsoLepIso = tauCombinedIsolationDeltaBetaCorrRaw3Hits->at(itau) > 3.5 && IsoEle < LeptonIsoCut;
//                        bool TauIso = tauCombinedIsolationDeltaBetaCorrRaw3Hits->at(itau)  < 3.5 ;
//                        bool TauAntiIso = tauCombinedIsolationDeltaBetaCorrRaw3Hits->at(itau) > 3.5 ;
//                        bool LepIso = IsoEle < LeptonIsoCut;
//                        bool LepAntiIso = IsoEle >= LeptonIsoCut;
//                        bool Total = 1;
                        
                        const int size_isoCat = 9;
                        bool Isolation = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) > 0.5 && IsoEle < LeptonIsoCut;
                        bool AntiIsolation = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) < 0.5 && IsoEle >= LeptonIsoCut;
                        bool TauIsoLepAntiIso = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) > 0.5 && IsoEle >= LeptonIsoCut;
                        bool TauAntiIsoLepIso = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) < 0.5 && IsoEle < LeptonIsoCut;
                        bool TauIso = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) > 0.5 ;
                        bool TauAntiIso = tauByLooseCombinedIsolationDeltaBetaCorr3Hits->at(itau) < 0.5 ;
                        bool LepIso = IsoEle < LeptonIsoCut;
                        bool LepAntiIso = IsoEle >= LeptonIsoCut;
                        bool Total = 1;
                        
                        
                        
                        bool Iso_category[size_isoCat] = {Isolation, AntiIsolation,TauIsoLepAntiIso,TauAntiIsoLepIso,TauIso,TauAntiIso,LepIso,LepAntiIso,Total};
                        
                        
                        std::string iso_Cat[size_isoCat] = {
                            "", "_AntiIso","_TauIsoLepAntiIso","_TauAntiIsoLepIso","_TauIso","TauAntiIso","_LepIso","_LepAntiIso","_Total"};
                        
                        
                        //###############################################################################################
                        //  MT Categorization
                        //###############################################################################################
                        float tmass= TMass_F(elePt->at(iele), elePt->at(iele)*cos(elePhi->at(iele)),elePt->at(iele)*sin(elePhi->at(iele)) ,  pfMET, pfMETPhi);
                        const int size_mTCat = 1;
                        bool NoMT = 1;
                        bool LoWMT = tmass < 30;
                        bool HighMT = tmass > 70;
                        bool MT_category[size_mTCat] = {NoMT};
                        std::string MT_Cat[size_mTCat] = {""};
                        //                        bool MT_category[size_mTCat] = {NoMT,LoWMT,HighMT};
                        //                        std::string MT_Cat[size_mTCat] = {"", "_LowMT","_HighMT"};
                        
                        //###############################################################################################
                        //  Trigger Categorization
                        //###############################################################################################
                        //https://twiki.cern.ch/twiki/bin/view/CMS/ElectronScaleFactorsRun2
                        const int size_trgCat = 1;
                        //                            bool PassTrigger = (HLTEleMuX >> 0 & 1) == 1 || (HLTEleMuX >> 11 & 1) == 1;
                        //                            bool PassTrigger = (HLTEleMuX >> 0 & 1) == 1 || (HLTEleMuX >> 1 & 1) == 1 || (HLTEleMuX >> 6 & 1) == 1|| (HLTEleMuX >> 11 & 1) == 1;
                        bool PassTrigger =   ((HLTEleMuX >> 2 & 1) == 1 && isData )|| (1 && !isData );
                        //                        bool PassTrigger =   ((HLTEleMuX >> 6 & 1) == 1 && isData )|| ((HLTEleMuX >> 11 & 1) == 1 && !isData );
                        
                        bool NoTrigger = 1;
                        //                    bool Trigger_category[size_trgCat] = {PassTrigger, NoTrigger};
                        //                    std::string trg_Cat[size_trgCat] = {"", "_NoTrigger"};
                        bool Trigger_category[size_trgCat] = {PassTrigger};
                        std::string trg_Cat[size_trgCat] = {""};
                        
                        //###############################################################################################
                        //  ST Categorization
                        //###############################################################################################
                        const int size_ST = 2;
//                        bool ST_category[size_ST] = {JetBJet_Selection,DiJet_Selection};
                        bool ST_category[size_ST] = {1,1};
                        std::string ST_Cat[size_ST] = {"_JetBJet","_DiJet"};
//                        float TTScaleFactor[size_ST]={0.88,0.94};
                        float TTScaleFactor[size_ST]={1.00,1.00};
                        
                        //###############################################################################################
                        
                        
                        
                        if (GeneralEleTauSelection){
                            
                            plotFill("Weight_Ele",eleCorr,200,0,2);
                            plotFill("TotalWeight_Ele",TotalWeight,1000,0,10);
                            plotFill("TotalNonLumiWeight_Ele",TotalWeight/LumiWeight,1000,0,10);
                            
                            
                            for (int qcat = 0; qcat < size_Q; qcat++) {
                                if (charge_category[qcat]) {
                                    for (int iso = 0; iso < size_isoCat; iso++) {
                                        if (Iso_category[iso]) {
                                            for (int imt = 0; imt < size_mTCat; imt++) {
                                                if (MT_category[imt]) {
                                                    for (int ist = 0; ist < size_ST; ist++) {
                                                        if (ST_category[ist]) {

                                                            if (isTTJets!= string::npos) NewTotalWeight=TotalWeight * TTScaleFactor[ist];  // Add TT scale factor
                                                            if (isWJets!= string::npos) NewTotalWeight=TotalWeight * WSCALEFACTORE;  // Add W scale factor
                                                            
                                                            for (int trg = 0; trg < size_trgCat; trg++) {
                                                                if (Trigger_category[trg]) {
                                                                    
                                                                    
                                                                    std::string FullStringName = MT_Cat[imt] +q_Cat[qcat] + iso_Cat[iso] +trg_Cat[trg]+ST_Cat[ist];
//                                                                    plotFill("EleTau_tauDecayMode"+FullStringName,tauDecayMode->at(itau),12,0,12,NewTotalWeight);
//                                                                    plotFill("EleTau_tauNumSignalPFChargedHadrCands"+FullStringName,tauNumSignalPFChargedHadrCands->at(itau),5,0,5,NewTotalWeight);
                                                                    plotFill("EleTau_tmass"+FullStringName,tmass,500,0,500,NewTotalWeight);
                                                                    plotFill("EleTau_VisMass"+FullStringName,Z4Momentum.M(),500,0,500,NewTotalWeight);
                                                                    plotFill("EleTau_LepPt"+FullStringName,elePt->at(iele),300,0,300,NewTotalWeight);
                                                                    plotFill("EleTau_LepEta"+FullStringName,eleEta->at(iele),100,-2.5,2.5,NewTotalWeight);
                                                                    plotFill("EleTau_LepIso"+FullStringName,IsoEle,100,0,10,NewTotalWeight);
                                                                    plotFill("EleTau_TauPt"+FullStringName,tauPt->at(itau),200,0,200,NewTotalWeight);
                                                                    plotFill("EleTau_TauEta"+FullStringName,tauEta->at(itau),100,-2.5,2.5,NewTotalWeight);
                                                                    plotFill("EleTau_CloseJetTauPt"+FullStringName,CLoseJetTauPt,500,0,500,NewTotalWeight);
                                                                    plotFill("EleTau_NumJet"+FullStringName,JetVector.size(),10,0,10,NewTotalWeight);
                                                                    plotFill("EleTau_NumBJet"+FullStringName,BJetBVector.size(),10,0,10,NewTotalWeight);
//                                                                    plotFill("EleTau_nVtx"+FullStringName,nVtx,50,0,50,NewTotalWeight);
//                                                                    plotFill("EleTau_nVtx_NoPU"+FullStringName,nVtx,50,0,50,NewTotalWeight / PUWeight);
                                                                    plotFill("EleTau_MET"+FullStringName,pfMET,500,0,500,NewTotalWeight);
//                                                                    plotFill("EleTau_M_taujet"+FullStringName,M_TauJet,1000,0,1000,NewTotalWeight);
//                                                                    if (JetVector.size() > 1)  plotFill("EleTau_LeadJetPt"+FullStringName,JetVector[0].Pt(),300,0,300,NewTotalWeight);
//                                                                    if (JetVector.size() > 1) plotFill("EleTau_SubLeadJetPt"+FullStringName,JetVector[1].Pt(),300,0,300,NewTotalWeight);
//                                                                    plotFill("EleTau_ST_DiJet"+FullStringName,ST_DiJet,100,0,1000,NewTotalWeight);
//                                                                    plotFill("EleTau_ST_MET"+FullStringName,ST_MET,100,0,1000,NewTotalWeight);
                                                                    
                                                                    
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                                
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                    
                    
                } //End of Tree
            }//End of file
            //##############  end of dielectron
            
        }
        
    }
    
    fout->cd();
    //    BG_Tree->Write();
    
    map<string, TH1F*>::const_iterator iMap1 = myMap1->begin();
    map<string, TH1F*>::const_iterator jMap1 = myMap1->end();
    
    for (; iMap1 != jMap1; ++iMap1)
        nplot1(iMap1->first)->Write();
    
    map<string, TH2F*>::const_iterator iMap2 = myMap2->begin();
    map<string, TH2F*>::const_iterator jMap2 = myMap2->end();
    
    for (; iMap2 != jMap2; ++iMap2)
        nplot2(iMap2->first)->Write();
    
    fout->Close();
    
    
}


/////??////////??////////??////////??////////??////////??////////??///

//    else if (name.find("HLT_IsoMu17_eta2p1_v") != string::npos) bitEleMuX = 29;
// else if (name.find("HLT_IsoMu18_v") != string::npos) bitEleMuX = 30;

// MC  ele   if      (name.find("HLT_Ele22_eta2p1_WPLoose_Gsf_v")                    != string::npos) bitEleMuX =  0; //bit0(lowest)
// MC  ele   if (name.find("HLT_Ele22_eta2p1_WPTight_Gsf_v")                    != string::npos) bitEleMuX =  1;
//  data ele    if (name.find("HLT_Ele22_eta2p1_WPLoose_Gsf_v") != string::npos) bitEleMuX = 0; //bit0(lowest) NO iT shouldbe 6
// else if (name.find("HLT_Ele23_WPLoose_Gsf_v") != string::npos) bitEleMuX = 6;


