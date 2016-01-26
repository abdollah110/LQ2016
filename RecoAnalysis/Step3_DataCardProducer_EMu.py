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
SubRootDir = 'OutFilesEMu/'


verbos_ = False
OS_SS_Ratio=1.06


TauScale = [ ""]
#POSTFIX=["","Up","Down"]

signal = ['bba1GenFil_']
signalName = ['bba1']
mass = [25,30,  35, 40, 45, 50, 55,  60, 65, 70, 75, 80]

lenghtSig = len(signal) * len(mass) +1

#category = ["_inclusive", "_nobtag", "_btag", "_btagLoose"]
#category = ["_inclusive",  "_DiJet", "_JetBJet"]
category = ["_inclusive"]

channelDirectory = ["MuEle"]

####################################################
##   Functions
####################################################






############################################################################################################
def _FileReturn(Name, channel,cat,HistoName,PostFix,CoMEnergy):

    myfile = TFile(SubRootDir + Name +CoMEnergy+ '.root')
    Histo =  myfile.Get(channel+HistoName + cat+ PostFix)
    NewFile=TFile("Extra/XXX.root","RECREATE")
    NewFile.WriteObject(Histo,"XXX")
    myfile.Close()
    return NewFile


####################################################
##   Start Making the Datacard Histograms
####################################################
def MakeTheHistogram(channel,NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,CoMEnergy,chl,Binning):


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
#           ################################################
#            for sig in range(len(signal)):
#                for m in range(len(mass)):#    for m in range(110, 145, 5):
#
#                    print "Now is processing", signal[sig],mass[m]
#                    tDirectory.cd()
#                    Histogram = Observable+"_mTLess30_OS"
#                    XLoc= icat + len(category)*chl + 1
#                    YLoc= sig * len(mass) + m + 1
#                    normal = NormTable[tscale].GetBinContent(XLoc,YLoc)    #Get the Noralization
#                    Name= str(signal[sig])+str(mass[m])
#                    NameOut= str(signalName[sig]) +str(mass[m])+str(TauScaleOut[tscale])
#
#                    SampleFile= _FileReturn(Name, channel,NameCat, Histogram, TauScale[tscale],CoMEnergy,False)
#                    SampleHisto=SampleFile.Get("XXX")
#                    if SampleHisto:
#                        SampleHisto.Scale(normal/SampleHisto.Integral())
#                    else:
#                        SampleFile= _FileReturn(Name, channel,"_inclusive", Histogram, TauScale[tscale],CoMEnergy,False)
#                        SampleHisto=SampleFile.Get("XXX")
#                        SampleHisto.Scale(.0000001)
#                        
#                    RebinedHist= SampleHisto.Rebin(len(Binning)-1,"",Binning)
#                    tDirectory.WriteObject(RebinedHist,NameOut)
#                    


            ################################################
            #  Filling TOP
            ################################################
            print "Doing TOP, BG estimation"
            tDirectory.cd()

            Name= "TTJets"
            NameOut= "TT"+str(TauScaleOut[tscale])

            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
        
            ShapeFile= _FileReturn(Name, channel,NameCat, ShapeMC, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")

            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)
            
            ################################################
            #  Filling ZTT
            ################################################
            print "Doing ZL, BG estimation"
            tDirectory.cd()

            Name= "DYJetsToLL"
            NameOut= "ZTT"+str(TauScaleOut[tscale])
            
            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
            
            ShapeFile= _FileReturn(Name, channel,NameCat, ShapeMC, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")
            
            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)


            ################################################
            #  Filling W
            ################################################
            print "Doing W, BG estimation"
            tDirectory.cd()

            Name="WJetsToLNu"
            NameOut= "W"+str(TauScaleOut[tscale])

            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
            
            ShapeFile= _FileReturn(Name, channel,NameCat, ShapeW, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")
            
            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)

            ################################################
            #  Filling QCD
            ################################################
            print "Doing QCD, BG estimation"
            tDirectory.cd()


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


            TTSampleQCDShapeHist=TTSampleQCDShape.Get("XXX")
            ZTTSampleQCDShapeHist=ZTTSampleQCDShape.Get("XXX")
            WSampleQCDShapeHist=WSampleQCDShape.Get("XXX")
            DataSampleQCDShapeHist=DataSampleQCDShape.Get("XXX")

            DataSampleQCDShapeHist.Add(TTSampleQCDShapeHist, -1)
            DataSampleQCDShapeHist.Add(ZTTSampleQCDShapeHist, -1)
            DataSampleQCDShapeHist.Add(WSampleQCDShapeHist, -1)


            TTSampleQCDNormHist=TTSampleQCDNorm.Get("XXX")
            ZTTSampleQCDNormHist=ZTTSampleQCDNorm.Get("XXX")
            WSampleQCDNormHist=WSampleQCDNorm.Get("XXX")
            DataSampleQCDNormHist=DataSampleQCDNorm.Get("XXX")
            

            QCDEstimation= (DataSampleQCDNormHist.Integral()- (TTSampleQCDNormHist.Integral()+ZTTSampleQCDNormHist.Integral()+WSampleQCDNormHist.Integral())) * OS_SS_Ratio

            NameOut= "QCD"+str(TauScaleOut[tscale])
            DataSampleQCDShapeHist.Scale(QCDEstimation/DataSampleQCDShapeHist.Integral())  # The shape is from btag-Loose Need get back norm
            RebinedHist= DataSampleQCDShapeHist.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)

            ################################################
            #  Filling Data
            ################################################
            print "Doing Data estimation"
            tDirectory.cd()

            Name='Data'
            NameOut='data_obs'

            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
            NormHisto=NormFile.Get("XXX")
        
            ShapeFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy) #for data Shape and Norm should be the same
            ShapeHisto=ShapeFile.Get("XXX")
            
#            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)




    myOut.Close()





            
if __name__ == "__main__":
    
    ##########################################
    Binning = array.array("d",[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300])
    NormMC="_VisMass_NoMT_OS"
    ShapeMC="_VisMass_NoMT_OS"
    ShapeW="_VisMass_NoMT"
    NormQCD="_VisMass_NoMT_SS"
    ShapeQCD="_VisMass_NoMT_SS_RelaxIso"
    MakeTheHistogram("MuEle",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)


    ##########################################
    Binning = array.array("d",[0,1,2,3,4,5,6,7,8,9,10])
    NormMC="_NumJet_NoMT_OS"
    ShapeMC="_NumJet_NoMT_OS"
    ShapeW="_NumJet_NoMT_OS"
    NormQCD="_NumJet_NoMT_SS"
    ShapeQCD="_NumJet_NoMT_SS_RelaxIso"
    MakeTheHistogram("MuEle",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)


    ##########################################
    Binning = array.array("d",[0,1,2,3,4,5,6,7,8,9,10])
    NormMC="_NumBJet_NoMT_OS"
    ShapeMC="_NumBJet_NoMT_OS"
    ShapeW="_NumBJet_NoMT_OS"
    NormQCD="_NumBJet_NoMT_SS"
    ShapeQCD="_NumBJet_NoMT_SS_RelaxIso"
    MakeTheHistogram("MuEle",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)

    ##########################################
    Binning = array.array("d",[0,50,100,150,200,250,300,350,400,450,500,550,600,700])
    NormMC="_ST_JetBJet_NoMT_OS"
    ShapeMC="_ST_JetBJet_NoMT_OS"
    ShapeW="_ST_JetBJet_NoMT_OS"
    NormQCD="_ST_JetBJet_NoMT_SS"
    ShapeQCD="_ST_JetBJet_NoMT_SS_RelaxIso"
    MakeTheHistogram("MuEle",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)

    
    ##########################################
    Binning = array.array("d",[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200])
    NormMC="_tmass_NoMT_OS"
    ShapeMC="_tmass_NoMT_OS"
    ShapeW="_tmass_NoMT_OS"
    NormQCD="_tmass_NoMT_SS"
    ShapeQCD="_tmass_NoMT_SS_RelaxIso"
    MakeTheHistogram("MuEle",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)

