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
SubRootDir = 'OutFiles/'
#SubRootDir = 'OLD/'


verbos_ = False
OS_SS_Ratio=1.06


TauScale = [ ""]
#POSTFIX=["","Up","Down"]

signal = ['LQ_']
signalName = ['LQ_']
mass = [200,250, 300, 350, 400, 450, 500, 550,  600, 650, 700, 750, 800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]

lenghtSig = len(signal) * len(mass) +1

#category = ["_inclusive"]
#category = ["_inclusive",  "_JetBJet"]
category = ["_JetBJet"]

channelDirectory = ["MuTau", "EleTau"]
#channelDirectory = ["muTau"]

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
            for sig in range(len(signal)):
                for m in range(len(mass)):#    for m in range(110, 145, 5):

                    print "--------------------------------------------------->     Processing LQ Signal ", signal[sig],mass[m]
                    tDirectory.cd()

                    Name= str(signal[sig])+str(mass[m])
                    NameOut= str(signalName[sig]) +str(mass[m])+str(TauScaleOut[tscale])

                            
                    NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
                    NormHisto=NormFile.Get("XXX")
            
                    ShapeFile= _FileReturn(Name, channel,NameCat, ShapeMC, TauScale[tscale],CoMEnergy)
                    ShapeHisto=ShapeFile.Get("XXX")
            
                    if (NormHisto):
                        ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
                        RebinedHist= ShapeHisto.Rebin(len(Binning)-1,"",Binning)
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
            
            ShapeFile= _FileReturn(Name, channel,NameCat, ShapeMC, TauScale[tscale],CoMEnergy)
            ShapeHisto=ShapeFile.Get("XXX")
            
            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
            RebinedHist= ShapeHisto.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)
            ################################################
            #  Filling VV
            ################################################
#            print "--------------------------------------------------->     Processing VV"
#            tDirectory.cd()
#        
#            Name= "VV"
#            NameOut= "VV"+str(TauScaleOut[tscale])
#            
#            NormFile= _FileReturn(Name, channel,NameCat, NormMC, TauScale[tscale],CoMEnergy)
#            NormHisto=NormFile.Get("XXX")
#            
#            ShapeFile= _FileReturn(Name, channel,NameCat, ShapeMC, TauScale[tscale],CoMEnergy)
#            ShapeHisto=ShapeFile.Get("XXX")
#            
#            ShapeHisto.Scale(NormHisto.Integral()/ShapeHisto.Integral())
#            RebinedHist= ShapeHisto.Rebin(len(Binning)-1,"",Binning)
#            tDirectory.WriteObject(RebinedHist,NameOut)


            ################################################
            #  Filling TOP
            ################################################
            print "--------------------------------------------------->     Processing TOP"
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
            print "--------------------------------------------------->     Processing ZTT"
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
            print "--------------------------------------------------->     Processing W"
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
            
            SingleT_qcd=0;
            if (SingleTSampleQCDNormHist): SingleT_qcd=SingleTSampleQCDNormHist.Integral()
            VV_qcd=0;
            if (VVSampleQCDNormHist): VV_qcd=VVSampleQCDNormHist.Integral()
            TT_qcd=0;
            if (TTSampleQCDNormHist): TT_qcd=TTSampleQCDNormHist.Integral()
            ZTT_qcd=0;
            if (ZTTSampleQCDNormHist): ZTT_qcd=ZTTSampleQCDNormHist.Integral()
            W_qcd=0;
            if (WSampleQCDNormHist): W_qcd=WSampleQCDNormHist.Integral()
            
            

            QCDEstimation= (DataSampleQCDNormHist.Integral()- (TT_qcd+ZTT_qcd+W_qcd)) * OS_SS_Ratio

            NameOut= "QCD"+str(TauScaleOut[tscale])
            DataSampleQCDShapeHist.Scale(QCDEstimation/DataSampleQCDShapeHist.Integral())  # The shape is from btag-Loose Need get back norm
            RebinedHist= DataSampleQCDShapeHist.Rebin(len(Binning)-1,"",Binning)
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
            RebinedHist= ShapeHisto.Rebin(len(Binning)-1,"",Binning)
            tDirectory.WriteObject(RebinedHist,NameOut)




    myOut.Close()





            
if __name__ == "__main__":
#    
#    ##########################################
    Binning = array.array("d",[0,20,40,60,80,100,120,140,160,180,200])
    NormMC="_VisMass_OS"
    ShapeMC="_VisMass_OS"
    ShapeW="_VisMass_OS"
    NormQCD="_VisMass_SS"
    ShapeQCD="_VisMass_SS_Total"
    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)

    ##########################################
    Binning = array.array("d",[0,1,2,3,4,5,6,7,8,9,10])
    NormMC="_NumJet_OS"
    ShapeMC="_NumJet_OS"
    ShapeW="_NumJet_OS"
    NormQCD="_NumJet_SS"
    ShapeQCD="_NumJet_SS_AntiIso"
#    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
#    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)

    ##########################################
    Binning = array.array("d",[0,1,2,3,4,5,6,7,8,9,10])
    NormMC="_NumBJet_OS"
    ShapeMC="_NumBJet_OS"
    ShapeW="_NumBJet_OS"
    NormQCD="_NumBJet_SS"
    ShapeQCD="_NumBJet_SS_AntiIso"
#    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
#    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)
    ##########################################
    Binning = array.array("d",[0,100,200,300,400,500,600,700,800,900,1000,1200,1500,1800,2100,2400,2700,3000])
    NormMC="_ST_JetBJet_OS"
    ShapeMC="_ST_JetBJet_OS"
    ShapeW="_ST_JetBJet_OS"
    NormQCD="_ST_JetBJet_SS"
    ShapeQCD="_ST_JetBJet_SS_Total"
    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)


    
    ##########################################
    Binning = array.array("d",[0,20,40,60,80,100,120,140,160,180,200])
    NormMC="_tmass_OS"
    ShapeMC="_tmass_OS"
    ShapeW="_tmass_OS"
    NormQCD="_tmass_SS"
    ShapeQCD="_tmass_SS_Total"
    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)


    ##########################################
    Binning = array.array("d",[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30])
    NormMC="_nVtx_OS"
    ShapeMC="_nVtx_OS"
    ShapeW="_nVtx_OS"
    NormQCD="_nVtx_SS"
    ShapeQCD="_nVtx_SS_AntiIso"
#    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
#    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)

    ##########################################
    Binning = array.array("d",[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30])
    NormMC="_nVtx_NoPU_OS"
    ShapeMC="_nVtx_NoPU_OS"
    ShapeW="_nVtx_NoPU_OS"
    NormQCD="_nVtx_NoPU_SS"
    ShapeQCD="_nVtx_NoPU_SS_AntiIso"
#    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
#    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)

    ##########################################
    Binning = array.array("d",[0,50,100,150,200,250,300,350,400,450,500,550,600])
    NormMC="_M_taujet_OS"
    ShapeMC="_M_taujet_OS"
    ShapeW="_M_taujet_OS"
    NormQCD="_M_taujet_SS"
    ShapeQCD="_M_taujet_SS_Total"
    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)

    ##########################################
    Binning = array.array("d",[0,100,200,300,400,500,600,700,800,900,1000,1200,1500,1800,2100,2400,2700,3000])
    NormMC="_ST_JetBJetFinal_OS"
    ShapeMC="_ST_JetBJetFinal_OS"
    ShapeW="_ST_JetBJetFinal_OS"
    NormQCD="_ST_JetBJetFinal_SS"
    ShapeQCD="_ST_JetBJetFinal_SS_Total"
    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)

##########################################
    Binning = array.array("d",[0,100,200,300,400,500,600,700,800,900,1000,1200,1500])
    NormMC="_ST_JetBJetFinal_SS_TauAntiIsoLepIso"
    ShapeMC="_ST_JetBJetFinal_SS_TauAntiIsoLepIso"
    ShapeW="_ST_JetBJetFinal_SS_TauAntiIsoLepIso"
    NormQCD="_ST_JetBJetFinal_SS_TauAntiIsoLepIso"
    ShapeQCD="_ST_JetBJetFinal_SS_Total"
#    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
#    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)

##########################################
    Binning = array.array("d",[0,100,200,300,400,500,600,700,800,900,1000,1200,1500,1800,2100,2400,2700,3000])
    NormMC="_ST_MET_OS"
    ShapeMC="_ST_MET_OS"
    ShapeW="_ST_MET_OS"
    NormQCD="_ST_MET_SS"
    ShapeQCD="_ST_MET_SS_Total"
    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)

##########################################
    Binning = array.array("d",[0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,330,360,400,450,500])
    NormMC="_MET_OS"
    ShapeMC="_MET_OS"
    ShapeW="_MET_OS"
    NormQCD="_MET_SS"
    ShapeQCD="_MET_SS_Total"
    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)

##########################################
    Binning = array.array("d",[0,100,200,300,400,500,600,700,800,900,1000,1200,1500,1800,2100,2400,2700,3000])
    NormMC="_ST_MET_OS_TauIsoLepAntiIso"
    ShapeMC="_ST_MET_OS_TauIsoLepAntiIso"
    ShapeW="_ST_MET_OS_TauIsoLepAntiIso"
    NormQCD="_ST_MET_SS_TauIsoLepAntiIso"
    ShapeQCD="_ST_MET_SS_Total"
    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)



