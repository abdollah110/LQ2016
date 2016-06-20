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
SubRootDir = 'OutFiles_PreSelection/'
#SubRootDir = 'OutFiles_NikiSelection1/'


verbos_ = False
#OS_SS_Ratio=1.06
OS_SS_Ratio=1.00
RB_=1

TauScale = [ ""]
#POSTFIX=["","Up","Down"]

signal = ['RHNu_']
signalName = ['RHW_']
mass = ['1000-500','1500-750','2000-1000','2500-1250','3000-1500']
Wmass = ['1000','1500','2000','2500','3000']

lenghtSig = len(signal) * len(mass) +1

category = ["_NoBJet"]
#category = ["_DiJet","_JetBJet"]
#category = ["_DiJet"]
#category = ["_JetBJet"]

#channelDirectory = [ "EleTau"]
channelDirectory = ["MuTau", "EleTau"]

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
def MakeTheHistogram(channel,NormMC,NormQCD,ShapeQCD,CoMEnergy,chl,Binning):
    print "\n\n\n\n\n\n ****** ------------------------------>     Starting for ",NormMC, "in Channel= ",channel

    TauScaleOut = [ ""]


    myOut = TFile("TotalRootForLimit_"+channel + NormMC+".root" , 'RECREATE') # Name Of the output file


    icat=-1
    for NameCat in category:
        icat =icat +1
        print "starting NameCat and channel and HistoName ", NameCat, channel, NormMC

        tDirectory= myOut.mkdir(channelDirectory[chl] + str(NameCat))
        tDirectory.cd()
        for tscale in range(len(TauScale)):

#           ################################################
#           #   Filling Signal
##           ################################################
#            for sig in range(len(signal)):
#                for m in range(len(mass)):#    for m in range(110, 145, 5):
#
#                    print "--------------------------------------------------->     Processing LQ Signal ", signal[sig],mass[m]
#                    tDirectory.cd()
#
#                    Name= str(signal[sig])+str(mass[m])
#                    NameOut= str(signalName[sig]) +str(Wmass[m])+str(TauScaleOut[tscale])
#
#                            
#                    NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
#                    NormHisto=NormFile.Get("XXX")
#            
#                    ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
#                    ShapeHisto=ShapeFile.Get("XXX")
#            
#                    ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
#                    RebinedHist= ShapeHisto.Rebin(RB_)
#                    tDirectory.WriteObject(RebinedHist,NameOut)

            ################################################
            #  Filling SingleTop
            ################################################
            print "--------------------------------------------------->     Processing SingleTop"
            tDirectory.cd()
        
            Name= "SingleTop"
            NameOut= "SingleTop"+str(TauScaleOut[tscale])
            
            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
            
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")
            
            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(RB_)
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
            
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")
            
            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(RB_)
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
        
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")

            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(RB_)
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
            
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")
            
            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(RB_)
            tDirectory.WriteObject(RebinedHist,NameOut)


            ################################################
            #  Filling W
            ################################################
            print "--------------------------------------------------->     Processing W"
            tDirectory.cd()

            Name="WJetsToLNu"
            NameOut= "W"+str(TauScaleOut[tscale])

            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
            
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")
            
            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(RB_)
            tDirectory.WriteObject(RebinedHist,NameOut)
            
            
            
            ################################################
            #  Filling Data
            ################################################
            print "--------------------------------------------------->     Processing Data"
            tDirectory.cd()
            
            Name='Data'
            NameOut='data_obs'
            
            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
            
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy) #for data Shape and Norm should be the same
            ShapeHisto=ShapeFile.Get("XXX")
            
            #            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(RB_)
            tDirectory.WriteObject(RebinedHist,NameOut)
            

            ################################################
            #  Filling QCD
            ################################################
            print "--------------------------------------------------->     Processing QCD"
            tDirectory.cd()
            
            Name= "SingleTop"
            SingleTSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
            SingleTSampleQCDShape= _FileReturn(Name, channel,"_NoBJet", ShapeQCD, TauScale[tscale],CoMEnergy)
            
            Name= "VV"
            VVSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
            VVSampleQCDShape= _FileReturn(Name, channel,"_NoBJet", ShapeQCD, TauScale[tscale],CoMEnergy)

            Name= "TTJets"
            TTSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
            TTSampleQCDShape= _FileReturn(Name, channel,"_NoBJet", ShapeQCD, TauScale[tscale],CoMEnergy)

            Name= "DYJetsToLL"
            ZTTSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
            ZTTSampleQCDShape= _FileReturn(Name, channel,"_NoBJet", ShapeQCD, TauScale[tscale],CoMEnergy)

            Name= "WJetsToLNu"
            WSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
            WSampleQCDShape= _FileReturn(Name, channel,"_NoBJet", ShapeQCD, TauScale[tscale],CoMEnergy)
                        
            Name="Data"
            DataSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
            DataSampleQCDShape= _FileReturn(Name, channel,"_NoBJet", ShapeQCD, TauScale[tscale],CoMEnergy)
            print  " norm  @@@@@@@", Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy
            print  " shape @@@@@@@", Name, channel,"_NoBJet", ShapeQCD, TauScale[tscale],CoMEnergy



            SingleTSampleQCDShapeHist=SingleTSampleQCDShape.Get("XXX")
            VVSampleQCDShapeHist=VVSampleQCDShape.Get("XXX")
            TTSampleQCDShapeHist=TTSampleQCDShape.Get("XXX")
            ZTTSampleQCDShapeHist=ZTTSampleQCDShape.Get("XXX")
            WSampleQCDShapeHist=WSampleQCDShape.Get("XXX")
            DataSampleQCDShapeHist=DataSampleQCDShape.Get("XXX")

            print "\n##########\n DataSampleQCDShapeHist before=",    DataSampleQCDShapeHist.Integral()
            
#            DataSampleQCDShapeHist.Add(SingleTSampleQCDShapeHist, -1)
#            DataSampleQCDShapeHist.Add(VVSampleQCDShapeHist, -1)
#            DataSampleQCDShapeHist.Add(TTSampleQCDShapeHist, -1)
#            DataSampleQCDShapeHist.Add(ZTTSampleQCDShapeHist, -1)
#            DataSampleQCDShapeHist.Add(WSampleQCDShapeHist, -1)

            print "\n##########\n DataSampleQCDShapeHist after=",    DataSampleQCDShapeHist.Integral()

            SingleTSampleQCDNormHist=SingleTSampleQCDNorm.Get("XXX")
            VVSampleQCDNormHist=VVSampleQCDNorm.Get("XXX")
            TTSampleQCDNormHist=TTSampleQCDNorm.Get("XXX")
            ZTTSampleQCDNormHist=ZTTSampleQCDNorm.Get("XXX")
            WSampleQCDNormHist=WSampleQCDNorm.Get("XXX")
            DataSampleQCDNormHist=DataSampleQCDNorm.Get("XXX")
            

#            if (SingleTSampleQCDNormHist) : DataSampleQCDNormHist.Add(SingleTSampleQCDNormHist, -1)
#            if (VVSampleQCDNormHist): DataSampleQCDNormHist.Add(VVSampleQCDNormHist, -1)
#            DataSampleQCDNormHist.Add(TTSampleQCDNormHist, -1)
#            DataSampleQCDNormHist.Add(ZTTSampleQCDNormHist, -1)
#            DataSampleQCDNormHist.Add(WSampleQCDNormHist, -1)


            FR_FitMaram=Make_Tau_FakeRate()
            QCDEstimation=0
            for bin in xrange(50,400):
                value=DataSampleQCDNormHist.GetBinContent(bin)
                print bin ," is value= ", value
        
                if value < 0 : value=0
                FR= _FIT_Jet_Function(bin+1.5,FR_FitMaram)
                QCDEstimation += value * FR/(1-FR)
            QCDEstimation    *= OS_SS_Ratio
            print "\n##########\n QCDEstimation",    QCDEstimation

#            QCDEstimation= (DataSampleQCDNormHist.Integral()- (TT_qcd+ZTT_qcd+W_qcd+SingleT_qcd+VV_qcd)) * OS_SS_Ratio

            NameOut= "QCD"+str(TauScaleOut[tscale])
            DataSampleQCDShapeHist.Scale(QCDEstimation/DataSampleQCDShapeHist.Integral())  # The shape is from btag-Loose Need get back norm
            RebinedHist= DataSampleQCDShapeHist.Rebin(RB_)
            tDirectory.WriteObject(RebinedHist,NameOut)





    myOut.Close()





if __name__ == "__main__":
    Binning = array.array("d",[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300,400,500])
#    PlotName= ["_tmass","_VisMass","_LepPt","_LepEta","_TauPt","_TauEta","_NumJet","_NumBJet","_nVtx","_nVtx_NoPU","_MET","_M_taujet", "_LeadJetPt","_SubLeadJetPt","_ST_DiJet","_ST_MET"]
#    PlotName= ["_tmass","_VisMass","_LepPt","_LepEta","_TauPt","_TauEta","_NumJet","_NumBJet","_MET","_LeadJetPt","_SubLeadJetPt","_ST_DiJet","_ST_MET"]
#    PlotName= ["_tmass","_VisMass","_LepPt","_LepEta","_TauPt","_TauEta","_NumJet","_NumBJet","_MET"]
    PlotName= ["_TauPt_LowMT_OS_TauIso"]

#PlotNameQCDNorm= ["_tmass_SS","_VisMass_SS","_LepPt_SS","_LepEta_SS","_TauPt_SS","_TauEta_SS","_NumJet_SS","_NumBJet_SS","_nVtx_SS","_nVtx_NoPU_SS","_MET_SS","_M_taujet_SS", "_LeadJetPt_SS","_SubLeadJetPt_SS","_ST_DiJet_SS","_ST_MET_SS"]
#
#PlotNameQCDShape= ["_tmass_SS","_VisMass_SS","_LepPt_SS","_LepEta_SS","_TauPt_SS","_TauEta_SS","_NumJet_SS","_NumBJet_SS","_nVtx_SS","_nVtx_NoPU_SS","_MET_SS","_M_taujet_SS", "_LeadJetPt_SS","_SubLeadJetPt_SS","_ST_DiJet_SS","_ST_MET_SS"]


    for NormMC in PlotName:

        MakeTheHistogram("MuTau",NormMC,"_CloseJetTauPt_LowMT_OS_TauIsoLepAntiIso","_NumJet_LowMT_OS","",0,Binning)
#        MakeTheHistogram("EleTau",NormMC,"_CloseJetTauPt_TauAntiIsoLepIso",NormMC+"_SS_AntiIso","",1,Binning)
#        MakeTheHistogram("EleTau",NormMC,"_CloseJetTauPt_TauAntiIsoLepIso",NormMC+"_SS_AntiIso","",1,Binning)

###OS
#        MakeTheHistogram("MuTau",NormMC+"_OS","_CloseJetTauPt_OS_TauAntiIsoLepIso",NormMC+"_SS_AntiIso","",0,Binning)
#        MakeTheHistogram("EleTau",NormMC+"_OS","_CloseJetTauPt_OS_TauAntiIsoLepIso",NormMC+"_SS_AntiIso","",1,Binning)

