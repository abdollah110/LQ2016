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
from Step13_TauFakeRatefromMC import Make_Tau_FakeRate
from Step13_TauFakeRatefromMC import _FIT_Jet_Function
##### Get Jet to Tau FR

gROOT.Reset()
import os




ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.ProcessLine('.x rootlogon.C')
SubRootDir = './'
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

category = ["_inclusive"]
#category = ["_DiJet","_JetBJet"]
#category = ["_NoBJet"]
#category = ["_JetBJet"]

#channelDirectory = [ "EleTau"]
channelDirectory = ["MuTau","EleTau"]

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
    print "the return is based on the", channel+HistoName + cat+ PostFix
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



            ################################################
            #  Filling QCD
            ################################################
            print "--------------------------------------------------->     Processing QCD"
            tDirectory.cd()
            


            Name="qcdForValdation"
            DataSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
            DataSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, TauScale[tscale],CoMEnergy)



            DataSampleQCDShapeHist=DataSampleQCDShape.Get("XXX")
            DataSampleQCDNormHist=DataSampleQCDNorm.Get("XXX")
            FR_FitMaram=Make_Tau_FakeRate()
            QCDEstimation=0
            for bin in xrange(50,400):
                value=DataSampleQCDNormHist.GetBinContent(bin)
#                if value < 0 : value=0

                FR= _FIT_Jet_Function(bin+.5,FR_FitMaram)
                print  "--->  value is ", value , "  & FR= ", FR
#                QCDEstimation += value * FR/(1-FR)
                QCDEstimation += value * FR
            QCDEstimation    *= OS_SS_Ratio
            print "\n##########\n QCDEstimation",    QCDEstimation

#            QCDEstimation= (DataSampleQCDNormHist.Integral()- (TT_qcd+ZTT_qcd+W_qcd+SingleT_qcd+VV_qcd)) * OS_SS_Ratio

            NameOut= "QCD"+str(TauScaleOut[tscale])
            DataSampleQCDShapeHist.Scale(QCDEstimation/DataSampleQCDShapeHist.Integral())  # The shape is from btag-Loose Need get back norm
            RebinedHist= DataSampleQCDShapeHist.Rebin(RB_)
            tDirectory.WriteObject(RebinedHist,NameOut)

            ################################################
            #  Filling Data
            ################################################
            print "--------------------------------------------------->     Processing Data"
            tDirectory.cd()

            Name='qcdForValdation'
            NameOut='qcd_obs'

            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
        
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy) #for data Shape and Norm should be the same
            ShapeHisto=ShapeFile.Get("XXX")
            
#            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(RB_)
            tDirectory.WriteObject(RebinedHist,NameOut)




    myOut.Close()





if __name__ == "__main__":
#    Binning = array.array("d",[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300,400,500])
    Binning = array.array("d",[0,5,10,15,20,25,30])
#    PlotName= ["_tmass","_VisMass","_LepPt","_LepEta","_TauPt","_TauEta","_NumJet","_NumBJet","_nVtx","_nVtx_NoPU","_MET","_M_taujet", "_LeadJetPt","_SubLeadJetPt","_ST_DiJet","_ST_MET"]
#    PlotName= ["_tmass","_VisMass","_LepPt","_LepEta","_TauPt","_TauEta","_NumJet","_NumBJet","_MET","_LeadJetPt","_SubLeadJetPt","_ST_DiJet","_ST_MET"]
    PlotName= ["_tmass","_LepPt","_LepEta","_TauPt","_TauEta","_MET"]
#    PlotName= ["_MET"]
#    QCDShape="_tmass_LowMT_Total"


#PlotNameQCDNorm= ["_tmass_SS","_VisMass_SS","_LepPt_SS","_LepEta_SS","_TauPt_SS","_TauEta_SS","_NumJet_SS","_NumBJet_SS","_nVtx_SS","_nVtx_NoPU_SS","_MET_SS","_M_taujet_SS", "_LeadJetPt_SS","_SubLeadJetPt_SS","_ST_DiJet_SS","_ST_MET_SS"]
#
#PlotNameQCDShape= ["_tmass_SS","_VisMass_SS","_LepPt_SS","_LepEta_SS","_TauPt_SS","_TauEta_SS","_NumJet_SS","_NumBJet_SS","_nVtx_SS","_nVtx_NoPU_SS","_MET_SS","_M_taujet_SS", "_LeadJetPt_SS","_SubLeadJetPt_SS","_ST_DiJet_SS","_ST_MET_SS"]


    for NormMC in PlotName:

        MakeTheHistogram("MuTau",NormMC+"_OS_TauIso","_CloseJetTauPt_OS_Total",NormMC+"_SS_TauIso","",0,Binning)
#        MakeTheHistogram("EleTau",NormMC+"_LowMT_OS_TauIsoLepAntiIso","_CloseJetTauPt_LowMT_OS_AntiIso",NormMC+"_LowMT_TauIsoLepAntiIso","",1,Binning)
#        MakeTheHistogram("EleTau",NormMC,"_CloseJetTauPt_TauAntiIsoLepIso",NormMC+"_SS_AntiIso","",1,Binning)
#        MakeTheHistogram("EleTau",NormMC,"_CloseJetTauPt_TauAntiIsoLepIso",NormMC+"_SS_AntiIso","",0,Binning)

###OS
#        MakeTheHistogram("MuTau",NormMC+"_OS","_CloseJetTauPt_OS_TauAntiIsoLepIso",NormMC+"_SS_AntiIso","",0,Binning)
#        MakeTheHistogram("EleTau",NormMC+"_OS","_CloseJetTauPt_OS_TauAntiIsoLepIso",NormMC+"_SS_AntiIso","",1,Binning)

