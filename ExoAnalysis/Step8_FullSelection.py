#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.
#http://root.cern.ch/viewvc/trunk/tutorials/pyroot/hsimple.py?revision=20881&view=markup
__author__ = "abdollahmohammadi"
__date__ = "$Feb 23, 2013 10:39:33 PM$"

import math
import ROOT
from ROOT import Double
from ROOT import TCanvas
from ROOT import TFile
from ROOT import TH1F
from ROOT import TH2F
from ROOT import TNtuple
from ROOT import TProfile
from ROOT import gBenchmark
from ROOT import gROOT
from ROOT import gRandom
from ROOT import gSystem
from ctypes import *
import ROOT as r
import array

##### Get Jet to Tau FR
from Step7_TauFakeRate import Make_Tau_FakeRate
from Step7_TauFakeRate import _FIT_Jet_Function
##### Get Jet to Tau FR

gROOT.Reset()
import os




ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.ProcessLine('.x rootlogon.C')
#SubRootDir = 'OutFiles_FullSelection_Buggy/'
#SubRootDir = 'OutFiles_FullSelection/'
#SubRootDir = 'OutFiles_FullSelection_MediumIso/'
#SubRootDir = 'OutFiles_FullSelection_TightIso/'
#SubRootDir = 'OutFiles_FullSelection/'
SubRootDir = 'OutFiles_FullSelection_NewDM/'



verbos_ = False
#OS_SS_Ratio=1.06
OS_SS_Ratio=1.00
RB_=10

TauScale = ["Down", "", "Up"]
SystematicHighPtTau = ["TauHighPtRWUp","TauHighPtRWDown"]
SystematicWShape = ["_WShapeUp","_WShapeDown"]
#TauScale = ["", "", ""]
#POSTFIX=["","Up","Down"]





#channelDirectory = ["MuTau", "eleTau"]
channelDirectory = ["MuTau", "EleTau"]
FinalName = ["_mt", "_et"]

####################################################
##   Functions
####################################################






############################################################################################################
def _FileReturn(Name, channel,cat,HistoName,PostFix,CoMEnergy):

    if not os.path.exists(SubRootDir):
        os.makedirs(SubRootDir)
    myfile = TFile(SubRootDir + Name +CoMEnergy+ '.root')
    print "##### --->>>>>>> File name is ", SubRootDir + Name +CoMEnergy+ '.root'  "   and histo is -->  ", channel+HistoName + cat+ PostFix
    Histo =  myfile.Get(channel+HistoName + cat+ PostFix)
    if not os.path.exists("Extra"):
        os.makedirs("Extra")
    NewFile=TFile("Extra/XXX.root","RECREATE")
    NewFile.WriteObject(Histo,"XXX")
    myfile.Close()
    return NewFile


####################################################
##   Start Making the Datacard Histograms
####################################################
def MakeTheHistogram(channel,NormMC,NormQCD,ShapeQCD,CoMEnergy,chl,Binning,Analysis):
    
    
    if Analysis=="lq":
        signal = ['LQ_']
        signalName = ['LQ_']
        mass = [200,250, 300, 350, 400, 450, 500, 550,  600, 650, 700, 750, 800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]
        TOTMASS = [200,250, 300, 350, 400, 450, 500, 550,  600, 650, 700, 750, 800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]
        lenghtSig = len(signal) * len(mass) +1
        category = ["_JetBJet"]
        charge="_OS"

    if Analysis=="RHW":
        signal = ['RHNu_']
        signalName = ['RHW_']
        mass = ['1000-500','1500-750','2000-1000','2500-1250','3000-1500']
        TOTMASS = ['1000','1500','2000','2500','3000']
        lenghtSig = len(signal) * len(mass) +1
        category = ["_DiJet"]
        charge=""

    
#    print "\n\n\n\n\n\n ****** ------------------------------>     Starting for ",NormMC, "in Channel= ",channel

    TauScaleOut = ["_CMS_scale_t_"+channel+CoMEnergy+"Down", "", "_CMS_scale_t_"+channel+CoMEnergy+"Up"]
    Signal_Unc_HighPtTau = ["_CMS_eff_t_HighPtTau_"+channel+CoMEnergy+"Up","_CMS_eff_t_HighPtTau_"+channel+CoMEnergy+"Down"]
    Signal_Unc_WShape = ["_CMS_W_Shape_"+channel+CoMEnergy+"Up","_CMS_W_Shape_"+channel+CoMEnergy+"Down"]

    myOut = TFile(Analysis+FinalName[chl]+".inputs-sm-13TeV.root" , 'RECREATE') # Name Of the output file


    icat=-1
    for NameCat in category:
        icat =icat +1
        print "starting NameCat and channel and HistoName ", NameCat, channel, NormMC

        tDirectory= myOut.mkdir(channelDirectory[chl] + str(NameCat))
        tDirectory.cd()
        for tscale in range(len(TauScale)):

           ################################################
           #   Filling Signal
#           ################################################
            for sig in range(len(signal)):
                for m in range(len(mass)):

                    print "--------------------------------------------------->     Processing  Signal ", signal[sig],mass[m]
                    tDirectory.cd()

                    Name= str(signal[sig])+str(mass[m])
                    NameOut= str(signalName[sig]) +str(TOTMASS[m])+str(TauScaleOut[tscale])

                            
                    NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
                    NormHisto=NormFile.Get("XXX")
            
                    RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                    tDirectory.WriteObject(RebinedHist,NameOut)
        
                    ###############  Systematics on Shape and Norm for  High Tau Pt ####
                    if  tscale==1 :
                        for systHighpt in range(len(SystematicHighPtTau)):
                            tDirectory.cd()
                            Histogram = NormMC.replace("_OS","")+SystematicHighPtTau[systHighpt]+charge
                            NameOut= str(signalName[sig]) +str(TOTMASS[m])+str(Signal_Unc_HighPtTau[systHighpt])
                            
                            NormFile= _FileReturn(Name, channel,NameCat, Histogram, TauScale[tscale],CoMEnergy)
                            NormHisto=NormFile.Get("XXX")
                            
                            RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                            tDirectory.WriteObject(RebinedHist,NameOut)
        
            ################################################
            #  Filling SingleTop
            ################################################
            print "--------------------------------------------------->     Processing SingleTop"
            tDirectory.cd()
        
            Name= "SingleTop"
            NameOut= "SingleTop"+str(TauScaleOut[tscale])
            
            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
            
            RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)
            
            ###############  Systematics on Shape and Norm for  High Tau Pt ####
            if  tscale==1 :
                for systHighpt in range(len(SystematicHighPtTau)):
                    tDirectory.cd()
                    Histogram = NormMC.replace("_OS","")+SystematicHighPtTau[systHighpt]+ charge
                    NameOut= "SingleTop"+str(Signal_Unc_HighPtTau[systHighpt])
                    
                    NormFile= _FileReturn(Name, channel,NameCat, Histogram, TauScale[tscale],CoMEnergy)
                    NormHisto=NormFile.Get("XXX")
                    
                    RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                    tDirectory.WriteObject(RebinedHist,NameOut)
            ################################################
            #  Filling VV
            ################################################
            print "--------------------------------------------------->     Processing VV"
            tDirectory.cd()
        
            Name= "VV"
            NameOut= "VV"+str(TauScaleOut[tscale])
            
            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
            
            RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)
            
            ###############  Systematics on Shape and Norm for  High Tau Pt ####
            if  tscale==1 :
                for systHighpt in range(len(SystematicHighPtTau)):
                    tDirectory.cd()
                    Histogram = NormMC.replace("_OS","")+SystematicHighPtTau[systHighpt]+ charge
                    NameOut= "VV"+str(Signal_Unc_HighPtTau[systHighpt])
                    
                    NormFile= _FileReturn(Name, channel,NameCat, Histogram, TauScale[tscale],CoMEnergy)
                    NormHisto=NormFile.Get("XXX")
                    
                    RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                    tDirectory.WriteObject(RebinedHist,NameOut)


            ################################################
            #  Filling TOP
            ################################################
            print "--------------------------------------------------->     Processing TOP"
            tDirectory.cd()

            Name= "TTJets"
            NameOut= "TT"+str(TauScaleOut[tscale])

            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
        
            RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)
            ###############  Systematics on Shape and Norm for  High Tau Pt ####
            if  tscale==1 :
                for systHighpt in range(len(SystematicHighPtTau)):
                    tDirectory.cd()
                    Histogram = NormMC.replace("_OS","")+SystematicHighPtTau[systHighpt]+ charge
                    NameOut= "TT"+str(Signal_Unc_HighPtTau[systHighpt])
                    
                    NormFile= _FileReturn(Name, channel,NameCat, Histogram, TauScale[tscale],CoMEnergy)
                    NormHisto=NormFile.Get("XXX")
                    
                    RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                    tDirectory.WriteObject(RebinedHist,NameOut)
            
            ################################################
            #  Filling ZTT
            ################################################
            print "--------------------------------------------------->     Processing ZTT"
            tDirectory.cd()

            Name= "DYJetsToLL"
            NameOut= "ZTT"+str(TauScaleOut[tscale])
            
            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
            
            RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)
            ###############  Systematics on Shape and Norm for  High Tau Pt ####
            if  tscale==1 :
                for systHighpt in range(len(SystematicHighPtTau)):
                    tDirectory.cd()
                    Histogram = NormMC.replace("_OS","")+SystematicHighPtTau[systHighpt]+ charge
                    NameOut= "ZTT"+str(Signal_Unc_HighPtTau[systHighpt])
                    
                    NormFile= _FileReturn(Name, channel,NameCat, Histogram, TauScale[tscale],CoMEnergy)
                    NormHisto=NormFile.Get("XXX")
                    
                    RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                    tDirectory.WriteObject(RebinedHist,NameOut)


            ################################################
            #  Filling W
            ################################################
            print "--------------------------------------------------->     Processing W"
            tDirectory.cd()

            Name="WJetsToLNu"
            NameOut= "W"+str(TauScaleOut[tscale])

            NormFileWNoCor= _FileReturn(Name, channel,NameCat, NormMC.replace("_OS","_NoCor") +"_OS", TauScale[tscale],CoMEnergy)
            NormHistoWNoCor=NormFileWNoCor.Get("XXX")
            WNoCorNormaliztaion=NormHistoWNoCor.Integral()
            
        
            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
            
            NormHisto.Scale(WNoCorNormaliztaion/NormHisto.Integral())
            RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)

            ###############  Systematics on Shape and Norm for  High Tau Pt ####
            if  tscale==1 :
                for systHighpt in range(len(SystematicHighPtTau)):
                    tDirectory.cd()
                    Histogram = NormMC.replace("_OS","")+SystematicHighPtTau[systHighpt]+ charge
                    NameOut= "W"+str(Signal_Unc_HighPtTau[systHighpt])
                        
                    NormFile= _FileReturn(Name, channel,NameCat, Histogram, TauScale[tscale],CoMEnergy)
                    NormHisto=NormFile.Get("XXX")
                    
                    RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                    tDirectory.WriteObject(RebinedHist,NameOut)
        
        
                for systW in range(len(SystematicWShape)):
                    tDirectory.cd()
                    Histogram = NormMC.replace("_OS","")+SystematicWShape[systW]+ charge
                    NameOut= "W"+str(Signal_Unc_WShape[systW])
                    
                    NormFile= _FileReturn(Name, channel,NameCat, Histogram, TauScale[tscale],CoMEnergy)
                    NormHisto=NormFile.Get("XXX")
                    
                    NormHisto.Scale(WNoCorNormaliztaion/NormHisto.Integral())
                    RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                    tDirectory.WriteObject(RebinedHist,NameOut)

        

            ################################################
            #  Filling QCD
            ################################################
            if tscale ==1:
                print "--------------------------------------------------->     Processing QCD"
                tDirectory.cd()
                
                Name= "SingleTop"
                SingleTSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
                SingleTSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, TauScale[tscale],CoMEnergy)
                
                Name= "VV"
                VVSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
                VVSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, TauScale[tscale],CoMEnergy)

                Name= "TTJets"
                TTSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
                TTSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, TauScale[tscale],CoMEnergy)

                Name= "DYJetsToLL"
                ZTTSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
                ZTTSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, TauScale[tscale],CoMEnergy)

                Name= "WJetsToLNu"
                WSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
                WSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, TauScale[tscale],CoMEnergy)
                            
                Name="Data"
                DataSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
                DataSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, TauScale[tscale],CoMEnergy)



                SingleTSampleQCDShapeHist=SingleTSampleQCDShape.Get("XXX")
                VVSampleQCDShapeHist=VVSampleQCDShape.Get("XXX")
                TTSampleQCDShapeHist=TTSampleQCDShape.Get("XXX")
                ZTTSampleQCDShapeHist=ZTTSampleQCDShape.Get("XXX")
                WSampleQCDShapeHist=WSampleQCDShape.Get("XXX")
                DataSampleQCDShapeHist=DataSampleQCDShape.Get("XXX")

                print "\n##########\nlooseQCDNORM before=",    DataSampleQCDShapeHist.Integral()
                
                if (SingleTSampleQCDShapeHist) : DataSampleQCDShapeHist.Add(SingleTSampleQCDShapeHist, -1)
                if (VVSampleQCDShapeHist): DataSampleQCDShapeHist.Add(VVSampleQCDShapeHist, -1)
                DataSampleQCDShapeHist.Add(TTSampleQCDShapeHist, -1)
                DataSampleQCDShapeHist.Add(ZTTSampleQCDShapeHist, -1)
                DataSampleQCDShapeHist.Add(WSampleQCDShapeHist, -1)


                SingleTSampleQCDNormHist=SingleTSampleQCDNorm.Get("XXX")
                VVSampleQCDNormHist=VVSampleQCDNorm.Get("XXX")
                TTSampleQCDNormHist=TTSampleQCDNorm.Get("XXX")
                ZTTSampleQCDNormHist=ZTTSampleQCDNorm.Get("XXX")
                WSampleQCDNormHist=WSampleQCDNorm.Get("XXX")
                DataSampleQCDNormHist=DataSampleQCDNorm.Get("XXX")
                

                if (SingleTSampleQCDNormHist) : DataSampleQCDNormHist.Add(SingleTSampleQCDNormHist, -1)
                if (VVSampleQCDNormHist): DataSampleQCDNormHist.Add(VVSampleQCDNormHist, -1)
                DataSampleQCDNormHist.Add(TTSampleQCDNormHist, -1)
                DataSampleQCDNormHist.Add(ZTTSampleQCDNormHist, -1)
                DataSampleQCDNormHist.Add(WSampleQCDNormHist, -1)
                
                print "\n##########\nlooseQCDNORM after=",    DataSampleQCDShapeHist.Integral()
                FR_FitMaram=Make_Tau_FakeRate()
                QCDEstimation=0
                for bin in xrange(50,400):
                    value=DataSampleQCDNormHist.GetBinContent(bin)
                    if value < 0 : value=0
                    FR= _FIT_Jet_Function(bin+1.5,FR_FitMaram)
                    QCDEstimation += value * FR/(1-FR)
                QCDEstimation    *= OS_SS_Ratio
                print "\n##########\n QCDEstimation",    QCDEstimation

    #            QCDEstimation= (DataSampleQCDNormHist.Integral()- (TT_qcd+ZTT_qcd+W_qcd+SingleT_qcd+VV_qcd)) * OS_SS_Ratio

                NameOut= "QCD"+str(TauScaleOut[tscale])
                DataSampleQCDShapeHist.Scale(QCDEstimation/DataSampleQCDShapeHist.Integral())  # The shape is from btag-Loose Need get back norm
                RebinedHist= DataSampleQCDShapeHist.Rebin(len(Binning)-1,"",Binning)
                tDirectory.WriteObject(RebinedHist,NameOut)

            ################################################
            #  Filling Data
            ################################################
            if tscale ==1:
                print "--------------------------------------------------->     Processing Data"
                tDirectory.cd()

                Name='Data'
                NameOut='data_obs'

                NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
                NormHisto=NormFile.Get("XXX")
            
                RebinedHist= NormHisto.Rebin(len(Binning)-1,"",Binning)
                tDirectory.WriteObject(RebinedHist,NameOut)




    myOut.Close()



#                    RebinedHist= ShapeHisto.Rebin(len(Binning)-1,"",Binning)

if __name__ == "__main__":
    Binning = array.array("d",[0,100,200,300,400,500,600,700,800,900,1000,1150,1300,1450,1600,1800,2000,2500,3000,4000,5000])
#    Binning = array.array("d",[0,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1075,1150,1225,1300,1375,1450,1525,1600,1700,1800,1900,2000,2250,2500,2750,3000,3500,4000,4500,5000])
#    Binning = array.array("d",[0,200,400,600,800,1000,1300,1600,2000,3000,5000])

    NormMC="_LQ_ST_MET"
    MakeTheHistogram("MuTau",NormMC+"_OS","_LQ_CloseJetTauPt_OS_TauAntiIsoLepIso",NormMC+"_AntiIso","",0,Binning,"lq")
    MakeTheHistogram("EleTau",NormMC+"_OS","_LQ_CloseJetTauPt_OS_TauAntiIsoLepIso",NormMC+"_AntiIso","",1,Binning,"lq")

    NormMC="_RW_ST_MET"
    MakeTheHistogram("MuTau",NormMC,"_RW_CloseJetTauPt_TauAntiIsoLepIso",NormMC+"_AntiIso","",0,Binning,"RHW")
    MakeTheHistogram("EleTau",NormMC,"_RW_CloseJetTauPt_TauAntiIsoLepIso",NormMC+"_AntiIso","",1,Binning,"RHW")
