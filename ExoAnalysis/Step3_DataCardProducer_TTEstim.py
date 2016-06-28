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

gROOT.Reset()
import os




ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.ProcessLine('.x rootlogon.C')
#SubRootDir = 'OutFiles_TTEstim/'
SubRootDir = 'OutFiles_TTEstim_LQ/'
#SubRootDir = 'OutFiles_TTEstim_RHW/'


verbos_ = False
OS_SS_Ratio=1.06
RBN_=1


TauScale = [ ""]
#POSTFIX=["","Up","Down"]

signal = ['LQ_']
signalName = ['LQ_']
mass = [200,250, 300, 350, 400, 450, 500, 550,  600, 650, 700, 750, 800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]

lenghtSig = len(signal) * len(mass) +1

#category = ["_inclusive", "_nobtag", "_btag", "_btagLoose"]
#category = ["_inclusive"]
category = ["_inclusive","_JetBJet","_DiJet"]

channelDirectory = ["MuEle"]

####################################################
##   Functions
####################################################






############################################################################################################
def _FileReturn(Name, channel,cat,HistoName,PostFix,CoMEnergy):
    
    if not os.path.exists(SubRootDir):
        os.makedirs(SubRootDir)
    myfile = TFile(SubRootDir + Name +CoMEnergy+ '.root')
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
def MakeTheHistogram(channel,NormMC,CoMEnergy,chl,Binning):
    
    
    TauScaleOut = [ ""]
    
    
    myOut = TFile("TotalRootForLimit_"+channel + NormMC+".root" , 'RECREATE') # Name Of the output file
    
    icat=-1
    for NameCat in category:
        icat =icat +1
        print "\n\n\n  starting NameCat and channel and HistoName ", NameCat, channel, NormMC
        
        tDirectory= myOut.mkdir(channelDirectory[chl] + str(NameCat))
        tDirectory.cd()
        for tscale in range(len(TauScale)):
            
#            #           ################################################
#            #           #   Filling Signal
#            #           ################################################
#            for sig in range(len(signal)):
#                for m in range(len(mass)):#    for m in range(110, 145, 5):
#                    
#                    print "Now is processing", signal[sig],mass[m]
#                    tDirectory.cd()
#                    
#                    Name= str(signal[sig])+str(mass[m])
#                    NameOut= str(signalName[sig]) +str(mass[m])+str(TauScaleOut[tscale])
#                    
#                    
#                    NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
#                    NormHisto=NormFile.Get("XXX")
#                    
#                    ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
#                    ShapeHisto=ShapeFile.Get("XXX")
#                    
#                    ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
#                    RebinedHist= ShapeHisto.Rebin(RBN_)
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
            RebinedHist= ShapeHisto.Rebin(RBN_)
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

            if  ShapeHisto:
                ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
                RebinedHist= ShapeHisto.Rebin(RBN_)
                tDirectory.WriteObject(RebinedHist,NameOut)
            

            ################################################
            #  Filling TOP
            ################################################
            print "Doing TOP, BG estimation"
            print "--------------------------------------------------->     Processing TOP"
            tDirectory.cd()

            Name= "TTJets"
            NameOut= "TT"+str(TauScaleOut[tscale])

            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
        
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")

            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(RBN_)
            tDirectory.WriteObject(RebinedHist,NameOut)
            
            ################################################
            #  Filling ZTT
            ################################################
            print "Doing ZTT, BG estimation"
            print "--------------------------------------------------->     Processing ZTT"
            tDirectory.cd()

            Name= "DYJetsToLL"
            NameOut= "ZTT"+str(TauScaleOut[tscale])
            
            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
            
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")
            
            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(RBN_)
            tDirectory.WriteObject(RebinedHist,NameOut)


            ################################################
            #  Filling W
            ################################################
            print "--------------------------------------------------->     Processing W"
            print "Doing W, BG estimation"
            tDirectory.cd()

            Name="WJetsToLNu"
            NameOut= "W"+str(TauScaleOut[tscale])

            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
            
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")
            
            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(RBN_)
            tDirectory.WriteObject(RebinedHist,NameOut)

#            ################################################
#            #  Filling QCD
#            ################################################
#            print "Doing QCD, BG estimation"
#            tDirectory.cd()
#
#
#            Name= "TTJets"
#            TTSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
#            TTSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, TauScale[tscale],CoMEnergy)
#
#            Name= "DYJetsToLL"
#            ZTTSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
#            ZTTSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, TauScale[tscale],CoMEnergy)
#
#            Name= "WJetsToLNu"
#            WSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
#            WSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, TauScale[tscale],CoMEnergy)
#                        
#            Name="Data"
#            DataSampleQCDNorm= _FileReturn(Name, channel,NameCat, NormQCD, TauScale[tscale],CoMEnergy)
#            DataSampleQCDShape= _FileReturn(Name, channel,NameCat, ShapeQCD, TauScale[tscale],CoMEnergy)
#
#
#            TTSampleQCDShapeHist=TTSampleQCDShape.Get("XXX")
#            ZTTSampleQCDShapeHist=ZTTSampleQCDShape.Get("XXX")
#            WSampleQCDShapeHist=WSampleQCDShape.Get("XXX")
#            DataSampleQCDShapeHist=DataSampleQCDShape.Get("XXX")
#
#            DataSampleQCDShapeHist.Add(TTSampleQCDShapeHist, -1)
#            DataSampleQCDShapeHist.Add(ZTTSampleQCDShapeHist, -1)
#            DataSampleQCDShapeHist.Add(WSampleQCDShapeHist, -1)
#
#
#            TTSampleQCDNormHist=TTSampleQCDNorm.Get("XXX")
#            ZTTSampleQCDNormHist=ZTTSampleQCDNorm.Get("XXX")
#            WSampleQCDNormHist=WSampleQCDNorm.Get("XXX")
#            DataSampleQCDNormHist=DataSampleQCDNorm.Get("XXX")
#            
#
#            QCDEstimation= (DataSampleQCDNormHist.Integral()- (TTSampleQCDNormHist.Integral()+ZTTSampleQCDNormHist.Integral()+WSampleQCDNormHist.Integral())) * OS_SS_Ratio
#
#            NameOut= "QCD"+str(TauScaleOut[tscale])
#            DataSampleQCDShapeHist.Scale(QCDEstimation/DataSampleQCDShapeHist.Integral())  # The shape is from btag-Loose Need get back norm
#            RebinedHist= DataSampleQCDShapeHist.Rebin(RBN_)
#            tDirectory.WriteObject(RebinedHist,NameOut)

            ################################################
            #  Filling Data
            ################################################
            print "--------------------------------------------------->     Processing Data"
            print "Doing Data estimation"
            tDirectory.cd()

            Name='Data'
            NameOut='data_obs'

            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
        
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy) #for data Shape and Norm should be the same
            ShapeHisto=ShapeFile.Get("XXX")
            
#            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(RBN_)
            tDirectory.WriteObject(RebinedHist,NameOut)




    myOut.Close()




if __name__ == "__main__":
    Binning = array.array("d",[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300,400,500])
    PlotName= ["_VisMass_OS","_NumJet_OS","_NumBJet_OS","_MET_OS","_ST_MET_OS","_ST_DiJet_OS","_ElePt_OS","_MuPt_OS","_EleEta_OS","_MuEta_OS"]
    
    
    for NormMC in PlotName:        
        MakeTheHistogram("MuEle",NormMC,"",0,Binning)

