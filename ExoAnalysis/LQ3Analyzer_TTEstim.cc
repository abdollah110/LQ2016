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
    
    
    //    TFile * PUData= new TFile("interface/MyDataPileupHistogram_246908-260426.root");
    //    TFile * PUData= new TFile("interface/MyDataPileupHistogram_246908-260426.root");
    //        TFile * PUData= new TFile("pileup-hists/Data_Pileup_2015D_Nov17.root");
    //    TFile * PUData= TFile::Open("pileup-hists/Data_Pileup_2015D_1p56fb.root");
    //        TFile * PUData= TFile::Open("pileup-hists/Data_Pileup_1p915fb.root");
    TFile * PUData= TFile::Open("pileup-hists/Data_Pileup_2015D_Nov17.root");
    TH1F * HistoPUData= (TH1F *) PUData->Get("pileup");
    HistoPUData->Scale(1.0/HistoPUData->Integral());
    
    TFile * PUMC= TFile::Open("pileup-hists/MC_Spring15_PU25_Startup.root");
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
        
        
        std::string ROOTLoc= "/Users/abdollah1/GIT_abdollah110/LQ2016/ROOT/V1_TTEstim/";
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
        
        
        
        
        
        float MuMass= 0.10565837;
        float eleMass= 0.000511;
        
        float LumiWeight = 1;
        
        
        
        
        
        Int_t nentries_wtn = (Int_t) Run_Tree->GetEntries();
        cout<<"nentries_wtn===="<<nentries_wtn<<"\n";
        for (Int_t i = 0; i < nentries_wtn; i++) {
            Run_Tree->GetEntry(i);
            if (i % 10000 == 0) fprintf(stdout, "\r  Processed events: %8d of %8d ", i, nentries_wtn);
            fflush(stdout);
            
            
            
            
            //###############################################################################################
            //  Weight Calculation
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
            float TotalWeight = LumiWeight * GetGenWeight * PUWeight;
            //###############################################################################################
            //  Histogram Filling
            //###############################################################################################
            plotFill("WeightLumi",LumiWeight,10000,0,100);
//            plotFill("WeightGen",GetGenWeight,1000000,0,1000000);
            plotFill("WeightPU",PUWeight,50,0,5);
            plotFill("WeightTotal",TotalWeight,200,0,2);
            plotFill("nVtx_NoPUCorr",nVtx,60,0,60);
            plotFill("nVtx_PUCorr",nVtx,60,0,60,PUWeight);
            for (int qq=0; qq < 50;qq++){
                if ((HLTEleMuX >> qq & 1) == 1)
                    plotFill("HLT",qq,50,0,50,TotalWeight);
            }

            
            
            //###############################################################################################
            //  Doing MuEle Analysis
            //###############################################################################################
            
            
            //Loop over MuEle events
            for  (int imu=0 ; imu < nMu; imu++){
                for  (int iele=0 ; iele < nEle; iele++){
                    
                    
                    float IsoMu=muPFChIso->at(imu)/muPt->at(imu);
                    if ( (muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu) )  > 0.0)
                        IsoMu= ( muPFChIso->at(imu)/muPt->at(imu) + muPFNeuIso->at(imu) + muPFPhoIso->at(imu) - 0.5* muPFPUIso->at(imu))/muPt->at(imu);
                    
                    bool MuPtCut = muPt->at(imu) > 40 && fabs(muEta->at(imu)) < 2.1 ;
                    bool MuIdIso=(muIsMediumID->at(imu) > 0 && IsoMu < 0.10 && fabs(muD0->at(imu)) < 0.045 && fabs(muDz->at(imu)) < 0.2);
                    
                    
                    
                    TLorentzVector Mu4Momentum,  ele4Momentum, Z4Momentum, Jet4Momentum,ExtraMu4Momentum, Extraele4Momentum;;
                    Mu4Momentum.SetPtEtaPhiM(muPt->at(imu),muEta->at(imu),muPhi->at(imu),MuMass);
                    ele4Momentum.SetPtEtaPhiM(elePt->at(iele),eleEta->at(iele),elePhi->at(iele),eleMass);
                    Z4Momentum=ele4Momentum+Mu4Momentum;
                    
                    
                    
                    
                    float IsoEle=elePFChIso->at(iele)/elePt->at(iele);
                    if ( (elePFNeuIso->at(iele) + elePFPhoIso->at(iele) - 0.5* elePFPUIso->at(iele))  > 0.0)
                        IsoEle= (elePFChIso->at(iele)/elePt->at(iele) + elePFNeuIso->at(iele) + elePFPhoIso->at(iele) - 0.5* elePFPUIso->at(iele))/elePt->at(iele);
                    
                    bool eleMVAId= false;
                    if (fabs (eleSCEta->at(iele)) < 0.8 && eleIDMVANonTrg->at(iele) > 0.967083) eleMVAId= true;
                    else if (fabs (eleSCEta->at(iele)) >  0.8 &&fabs (eleSCEta->at(iele)) <  1.5 && eleIDMVANonTrg->at(iele) > 0.929117) eleMVAId= true;
                    else if ( fabs (eleSCEta->at(iele)) >  1.5 && eleIDMVANonTrg->at(iele) > 0.726311 ) eleMVAId= true;
                    else eleMVAId= false;
                    
                    
                    
                    
                    
                    bool elePtCut = elePt->at(iele) > 40 && fabs(eleEta->at(iele)) < 2.1 ;
                    bool eleIdIso= (eleMVAId && eleMissHits->at(iele) < 2 && eleConvVeto->at(iele) && IsoEle < 0.10);
                    
                    
                    
                    float muCorr=getCorrFactorMuon74X(isData,  muPt->at(imu), muEta->at(imu) , HistoMuId,HistoMuIso,HistoMuTrg);
                    float eleCorr=getCorrFactorElectron74X(isData,  elePt->at(iele), eleEta->at(iele) , EleScaleFactor);
                    
                    TotalWeight= TotalWeight * muCorr * eleCorr;

                    plotFill("Weight_Mu",muCorr,200,0,2);
                    plotFill("Weight_Ele",eleCorr,200,0,2);
                    
                    //###########      Extra Mu Veto   ###########################################################
                    bool extraMuonExist= false;
                    //                  for  (int jmu=0 ; jmu < nMu; jmu++){
                    //                      //                        cout<<"step3\n";
                    //                      ExtraMu4Momentum.SetPtEtaPhiM(muPt->at(jmu),muEta->at(jmu),muPhi->at(jmu),MuMass);
                    //
                    //                      if (ExtraMu4Momentum.DeltaR(Mu4Momentum) < 0.5  || ExtraMu4Momentum.DeltaR(ele4Momentum) < 0.5 ) continue;
                    //                      if  ( muPt->at(jmu) < 15 ||  fabs(muEta->at(jmu)) > 2.4 ) continue ;
                    //
                    //                      float IsoMuExtra=muPFChIso->at(jmu)/muPt->at(jmu);
                    //                      if ( (muPFNeuIso->at(jmu) + muPFPhoIso->at(jmu) - 0.5* muPFPUIso->at(jmu) )  > 0.0)
                    //                      IsoMuExtra= ( muPFChIso->at(jmu)/muPt->at(jmu) + muPFNeuIso->at(jmu) + muPFPhoIso->at(jmu) - 0.5* muPFPUIso->at(jmu))/muPt->at(jmu);
                    //
                    //                      if (! (muIsLooseID->at(jmu) > 0 && IsoMuExtra < 0.30) ) continue;
                    //
                    //                      extraMuonExist=true;
                    //                  }
                    //###########      Extra Ele Veto   ###########################################################
                    
                    bool extraElectronExist= false;
                    //                  for  (int jele=0 ; jele < nEle; jele++){
                    //                      //                        cout<<"step4\n";
                    //                      Extraele4Momentum.SetPtEtaPhiM(elePt->at(jele),eleEta->at(jele),elePhi->at(jele),eleMass);
                    //
                    //                      if (Extraele4Momentum.DeltaR(Mu4Momentum) < 0.5  || Extraele4Momentum.DeltaR(ele4Momentum) < 0.5 ) continue;
                    //                      if ( elePt->at(jele) < 15 || fabs(eleEta->at(jele)) > 2.5) continue;
                    //
                    //                      float IsoEleExtra=elePFChIso->at(jele)/elePt->at(jele);
                    //                      if ( (elePFNeuIso->at(jele) + elePFPhoIso->at(jele) - 0.5* elePFPUIso->at(jele))  > 0.0)
                    //                      IsoEleExtra= (elePFChIso->at(jele)/elePt->at(jele) + elePFNeuIso->at(jele) + elePFPhoIso->at(jele) - 0.5* elePFPUIso->at(jele))/elePt->at(jele);
                    //
                    //                      bool eleMVAIdExtra= false;
                    //                      if (fabs (eleSCEta->at(jele)) < 0.8 && eleIDMVANonTrg->at(jele) >  0.913286 ) eleMVAIdExtra= true;
                    //                      else if (fabs (eleSCEta->at(jele)) >  0.8 &&fabs (eleSCEta->at(jele)) <  1.5 && eleIDMVANonTrg->at(jele) >  0.805013 ) eleMVAIdExtra= true;
                    //                      else if ( fabs (eleSCEta->at(jele)) >  1.5 && eleIDMVANonTrg->at(jele) >  0.358969  ) eleMVAIdExtra= true;
                    //                      else eleMVAIdExtra= false;
                    //
                    //
                    //                      if (!(eleMVAIdExtra && eleMissHits->at(jele) < 2 && eleConvVeto->at(jele) && IsoEleExtra < 0.30)) continue;
                    //                      extraElectronExist= true;
                    //
                    //                  }
                    
                    //################################################################################################
                    
                    
                    
                    bool  GeneralMuEleSelection= !extraMuonExist && MuPtCut && MuIdIso && Mu4Momentum.DeltaR(ele4Momentum) > 0.5 && !extraElectronExist && elePtCut &&  eleIdIso;
                    if ( GeneralMuEleSelection && muCorr==0)   cout <<"!!!!!!!!!!!! "<< muPt->at(imu)<< "   "<< muEta->at(imu)<<"\n";
                    
                    vector<float> EveJetPt;
                    vector<float> EveBJetPt;
                    EveJetPt.clear();
                    EveBJetPt.clear();
                    
                    for (int ijet= 0 ; ijet < nJet ; ijet++){
                        Jet4Momentum.SetPtEtaPhiE(jetPt->at(ijet),jetEta->at(ijet),jetPhi->at(ijet),jetEn->at(ijet));
                        if (jetPt->at(ijet) > 40 && fabs(jetEta->at(ijet)) < 2.5  && Jet4Momentum.DeltaR(ele4Momentum) > 0.5  && Jet4Momentum.DeltaR(Mu4Momentum) > 0.5 ){
                            EveJetPt.push_back(jetPt->at(ijet));
                            if (jetpfCombinedInclusiveSecondaryVertexV2BJetTags->at(ijet) >  0.89 ){
                                EveBJetPt.push_back(jetPt->at(ijet));
                            }
                        }
                        
                    }
                    
                    float ST_JetBjet=0;
                    bool JetBJet_Selection=EveJetPt.size() > 1& EveBJetPt.size()> 0 && (EveBJetPt[0]== EveJetPt[0] || EveBJetPt[0] ==EveJetPt[1]);
                    if (JetBJet_Selection){
                        ST_JetBjet=EveJetPt[0]+EveJetPt[1]+muPt->at(imu)+elePt->at(iele);
                        if ((EveJetPt[0]-EveJetPt[0]) * (EveBJetPt[0] - EveJetPt[1])) cout<<"MisMatch ij Jet BJet "<<"\n";
                    }
                    float ST_DiJet=0;
                    bool DiJet_Selection=EveJetPt.size() > 1;
                    if (DiJet_Selection)
                        ST_DiJet=EveJetPt[0]+EveJetPt[1]+muPt->at(imu)+elePt->at(iele);
                    
                    if (GeneralMuEleSelection){
                        for (int qq=0; qq < 50;qq++){
                            if ((HLTEleMuX >> qq & 1) == 1)
                                plotFill("HLT",qq,50,0,50,TotalWeight);
                        }
                    }
                    
                    
                    //###############################################################################################
                    //  Tau Lep Charge Categorization
                    //###############################################################################################
                    const int size_Q = 1;
                    //                    bool charge_No = 1;
                    bool charge_OS = muCharge->at(imu) * eleCharge->at(iele) < 0;
                    bool charge_SS = muCharge->at(imu) * eleCharge->at(iele) > 0;
                    bool charge_category[size_Q] = {charge_OS};
                    std::string q_Cat[size_Q] = {"_OS"};
                    
                    //###############################################################################################
                    //  Tau Isolation Categorization
                    //###############################################################################################
                    const int size_isoCat = 1;
                    bool TightIso = 1;
                    //                    bool RelaxIso = 1;
                    bool Iso_category[size_isoCat] = {TightIso};
                    std::string iso_Cat[size_isoCat] = {""};
                    //###############################################################################################
                    //  MT Categorization
                    //###############################################################################################
                    float tmass= TMass_F(muPt->at(imu), muPt->at(imu)*cos(muPhi->at(imu)),muPt->at(imu)*sin(muPhi->at(imu)) , pfMET, pfMETPhi);
                    const int size_mTCat = 2;
                    bool PassMT = tmass < 40;
                    bool NoMT = 1;
                    bool MT_category[size_mTCat] = {PassMT, NoMT};
                    std::string MT_Cat[size_mTCat] = {"", "_NoMT"};
                    //###############################################################################################
                    //  Trigger Categorization
                    //###############################################################################################
                    const int size_trgCat = 1;
                    bool PassTrigger = (HLTEleMuX >> 25 & 1) == 1; // Exist both in data and MC HLT_IsoMu27_v
                    //                  bool PassTrigger = ((HLTEleMuX >> 29 & 1) == 1 && !isData) || ((HLTEleMuX >> 30 & 1) == 1 && isData); //IsoMu17_eta2p1 MC && IsoMu18 Data
                    bool NoTrigger = 1;
                    bool Trigger_category[size_trgCat] = {PassTrigger};
                    std::string trg_Cat[size_trgCat] = {""};
                    //###############################################################################################
                    //  ST Categorization
                    //###############################################################################################
                    const int size_ST = 3;
                    bool ST_category[size_ST] = {1,JetBJet_Selection,DiJet_Selection};
                    std::string ST_Cat[size_ST] = {"_inclusive", "_JetBJet","_DiJet"};
                    //###############################################################################################
                    
                    
                    if (GeneralMuEleSelection){
                        for (int qcat = 0; qcat < size_Q; qcat++) {
                            if (charge_category[qcat]) {
                                for (int iso = 0; iso < size_isoCat; iso++) {
                                    if (Iso_category[iso]) {
                                        for (int imt = 0; imt < size_mTCat; imt++) {
                                            if (MT_category[imt]) {
                                                for (int ist = 0; ist < size_ST; ist++) {
                                                    if (ST_category[ist]) {
                                                        
                                                        
                                                        for (int trg = 0; trg < size_trgCat; trg++) {
                                                            
                                                            if (Trigger_category[trg]) {
                                                                
                                                                
                                                                std::string FullStringName = MT_Cat[imt] +q_Cat[qcat] + iso_Cat[iso] + trg_Cat[trg] +ST_Cat[ist];
                                                                
                                                                plotFill("MuEle_tmass"+FullStringName,tmass,200,0,2000,TotalWeight);
                                                                plotFill("MuEle_VisMass"+FullStringName,Z4Momentum.M(),200,0,1000,TotalWeight);
                                                                plotFill("MuEle_MuPt"+FullStringName,muPt->at(imu),200,0,200,TotalWeight);
                                                                plotFill("MuEle_MuPt_NoW8"+FullStringName,muPt->at(imu),300,0,300);
                                                                plotFill("MuEle_MuEta"+FullStringName,muEta->at(imu),100,-2.5,2.5,TotalWeight);
                                                                plotFill("MuEle_ElePt"+FullStringName,elePt->at(iele),200,0,200,TotalWeight);
                                                                plotFill("MuEle_EleEta"+FullStringName,eleEta->at(iele),100,-2.5,2.5,TotalWeight);
                                                                plotFill("MuEle_NumJet"+FullStringName,EveJetPt.size(),10,0,10,TotalWeight);
                                                                plotFill("MuEle_NumBJet"+FullStringName,EveBJetPt.size(),10,0,10,TotalWeight);
                                                                if (ST_JetBjet < 700) plotFill("MuEle_NumBJet_STLess700"+FullStringName,EveBJetPt.size(),10,0,10,TotalWeight);
                                                                if (EveJetPt.size() > 1) plotFill("MuEle_ST_DiJet"+FullStringName,ST_DiJet,100,0,1000,TotalWeight);
                                                                if (EveJetPt.size() > 1) plotFill("MuEle_ST_JetBJet"+FullStringName,ST_JetBjet,100,0,1000,TotalWeight);
                                                                
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
            }
            
            
            
            //###############################################################################################
            
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


