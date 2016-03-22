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
from ROOT import TF1
from ROOT import TPaveText
from ctypes import *
import ROOT as r
import array

gROOT.Reset()
import os




ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.ProcessLine('.x rootlogon.C')
SubRootDir = 'OutFiles/'
#SubRootDir = 'OutFiles_TMass60_noBjet20Gev/'

verbos_ = False
OS_SS_Ratio=1.06


TauScale = [ ""]
#POSTFIX=["","Up","Down"]

signal = ['LQ_']
signalName = ['LQ_']
mass = [200,250, 300, 350, 400, 450, 500, 550,  600, 650, 700, 750, 800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]

lenghtSig = len(signal) * len(mass) +1

#category = ["_inclusive"]
category = ["_inclusive","_JetBJet","_DiNonBJet"]
#category = ["_JetBJet"]

channelDirectory = ["MuTau", "EleTau"]
#channelDirectory = ["muTau"]

####################################################
##   Functions
####################################################






############################################################################################################
def _FileReturn(Name, channel,cat,HistoName,PostFix,CoMEnergy):
    print "0--------->>>>>>  ",
    if not os.path.exists(SubRootDir):
        os.makedirs(SubRootDir)
    myfile = TFile(SubRootDir + Name +CoMEnergy+ '.root')
    Histo =  myfile.Get(channel+HistoName + cat+ PostFix)
    print "0--------->>>>>>  ", channel+HistoName + cat+ PostFix
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




#    myOut = TFile("WEstimation_TotalRootForLimit_"+channel + NormMC+".root" , 'RECREATE') # Name Of the output file
#
#    icat=-1
#    for NameCat in category:
#        icat =icat +1
#        print "starting NameCat and channel and HistoName ", NameCat, channel, NormMC
#
#        tDirectory= myOut.mkdir(channelDirectory[chl] + str(NameCat))
#        tDirectory.cd()
            NameCat="_inclusive"
            tscale=0

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
            
            

            QCDEstimation= (DataSampleQCDNormHist.Integral()- (TT_qcd+ZTT_qcd+W_qcd))

#            NameOut= "QCD"+str(TauScaleOut[tscale])
            DataSampleQCDShapeHist.Scale(QCDEstimation/DataSampleQCDShapeHist.Integral())  # The shape is from btag-Loose Need get back norm
            RebinedHist= DataSampleQCDShapeHist.Rebin(len(Binning)-1,"",Binning)
#            tDirectory.WriteObject(RebinedHist,NameOut)

            NewShapeForQCD=TFile("Extra/XXX.root","RECREATE")
            NewShapeForQCD.WriteObject(RebinedHist,"XXX")
            return NewShapeForQCD
            








#############################################################################################################
##   Fit Function
#############################################################################################################

def fitFunc_Linear2Par(x,par):
    return par[0] + (par[1] * x[0])
def Func_Linear2Par(x,par0,par1):
    return par0 +  (par1 * x)

def fitFunc_Exp3Par( x,  par0,  par1,  par2) :
    return par0 + par1 * math.exp(par2 * x)
def Func_Exp3Par( x,  par) :
    return par[0] + par[1]*math.exp(par[2] * x[0])

#def Erf( x,  par0,par1) :
#    return par[0] + math.Erf(par[1] * x[0])

#############################################################################################################
##   Calculating the Fake Rate ---> "Linear Fit, 2 parameters"
#############################################################################################################
def Make_Tau_FakeRate():
    
    ##  ooooooooooooooooooooooooooo   Bcategory change name  ooooooooooooooooooooooooooo
    catName= "_inclusive"
    channelName="mutau"
    ##  ooooooooooooooooooooooooooo   Bcategory change name  ooooooooooooooooooooooooooo
    
    ##########################################
    Binning = array.array("d",[0,20,30,40,50,60,70,80,90,100,120,150,200,300])
    NormMC="_LepPt_LowMT_SS_LepIso"
    ShapeMC="_LepPt_LowMT_SS_LepIso"
    ShapeW="_LepPt_LowMT_SS_LepIso"
    NormQCD="_LepPt_LowMT_SS_LepIso"
    ShapeQCD="_LepPt_LowMT_SS_LepIso"
    ShapeNum=MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
    HistoNum=ShapeNum.Get("XXX")
#    HistoNum= HistoNum.Rebin(len(Binning_PT)-1,"",Binning_PT)
#    HistoNum.Scale(1000/HistoNum.Integral())

    
    
    
    Binning = array.array("d",[0,20,30,40,50,60,70,80,90,100,120,150,200,300])
    NormMC="_LepPt_LowMT_SS_Total"
    ShapeMC="_LepPt_LowMT_SS_Total"
    ShapeW="_LepPt_LowMT_SS_Total"
    NormQCD="_LepPt_LowMT_SS_Total"
    ShapeQCD="_LepPt_LowMT_SS_Total"
    
    ShapeDeNum=MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
    HistoDeNum=ShapeDeNum.Get("XXX")
#    HistoDeNum= HistoDeNum.Rebin(len(Binning_PT)-1,"",Binning_PT)
#    HistoDeNum.Scale(1000/HistoDeNum.Integral())

    HistoNum.Divide(HistoDeNum)
    
    canv = TCanvas("canv", "histograms", 600, 600)
    HistoNum.SetMinimum(0.5)
    #    HistoNum.GetXaxis().SetRangeUser(0,60)
    HistoNum.GetXaxis().SetRangeUser(0,300)
    HistoNum.GetXaxis().SetTitle("#tau p_{T} [GeV]")
    HistoNum.GetYaxis().SetRangeUser(0,2)
    HistoNum.SetStats(0)
    HistoNum.SetMarkerStyle(20)
    
    
    
    nPar = 3 # number of parameters in the fit
    theFit=TF1("theFit", "expo(7)", 30, 300)
    theFit.SetParameter(0, .4)
#    theFit.SetParLimits(0, .3, .5)
    theFit.SetParameter(1, 5)
    theFit.SetParLimits(1, 1, 2)
    theFit.SetParameter(2, 4.2)
    HistoNum.Fit("theFit", "R0")
    #    HistoNum.Fit(theFit, "R0","")
    HistoNum.Draw("E1")
    theFit.SetLineWidth(3)
    theFit.SetLineColor(3)
    FitParam=theFit.GetParameters()
    FitParamEre=theFit.GetParErrors()
    theFit.Draw("SAME")
    fitInfo  =TPaveText(.20,0.7,.60,0.9, "NDC");
    fitInfo.SetBorderSize(   0 );
    fitInfo.SetFillStyle(    0 );
    fitInfo.SetTextAlign(   12 );
    fitInfo.SetTextSize ( 0.03 );
    fitInfo.SetTextColor(    1 );
    fitInfo.SetTextFont (   62 );
    fitInfo.AddText("" + str(round(FitParam[0],2))+" + "+str(round(FitParam[1],3))+"*Exp(" +str(round(FitParam[2],3))+"* X)")
    #    fitInfo.AddText("Par0=" + str(round(FitParam[0],3)) + " #pm " + str(round(FitParamEre[0],3)) + " ,  Par1=" + str(round(FitParam[1],7)) + " #pm " + str(round(FitParamEre[1],7)))
    #    fitInfo.SetTextColor(    2 );
    #    fitInfo.AddText("Chis quare=  " + str(round(theFit.GetChisquare(),2)))
    fitInfo.Draw()
    canv.SaveAs("fitResults_MassDependent_OS_Over_SS_factor"+catName+channelName+".pdf")
    
    
    
#    theFit=TF1("theFit", fitFunc_Linear2Par, 20, 100, 2)
#    theFit.SetParameter(0, 0.6)
#    theFit.SetParameter(1, 0.18)
#    HistoNum.Fit(theFit, "R0","")
#    HistoNum.Draw("E1")
#    theFit.SetLineWidth(3)
#    theFit.SetLineColor(2)
#    FitParam=theFit.GetParameters()
#    FitParamEre=theFit.GetParErrors()
#    theFit.Draw("SAME")
#    fitInfo  =TPaveText(.20,0.7,.60,0.9, "NDC");
#    fitInfo.SetBorderSize(   0 );
#    fitInfo.SetFillStyle(    0 );
#    fitInfo.SetTextAlign(   12 );
#    fitInfo.SetTextSize ( 0.03 );
#    fitInfo.SetTextColor(    1 );
#    fitInfo.SetTextFont (   62 );
#    fitInfo.AddText("Linear Fit=  " + str(round(FitParam[0],3))+" + "+str(round(FitParam[1],9))+"x")
#    fitInfo.AddText("Par0=" + str(round(FitParam[0],3)) + " #pm " + str(round(FitParamEre[0],3)) + " ,  Par1=" + str(round(FitParam[1],7)) + " #pm " + str(round(FitParamEre[1],7)))
#    fitInfo.SetTextColor(    2 );
#    fitInfo.AddText("Chis quare=  " + str(round(theFit.GetChisquare(),2)))
#    fitInfo.Draw()
#    canv.SaveAs("fitResults_TauFR"+catName+channelName+".pdf")

#    return  FitParam[0],FitParam[1]





#
#
#            
if __name__ == "__main__":
    Make_Tau_FakeRate()

##
#
#    ##########################################
#    Binning = array.array("d",[0,20,30,40,50,60,70,80,90,100,110,120,140,160,200,250,300,400,500])
#    NormMC="_tmass_HighMT_OS"
#    ShapeMC="_tmass_HighMT_OS"
#    ShapeW="_tmass_HighMT_OS"
#    NormQCD="_tmass_HighMT_SS"
#    ShapeQCD="_tmass_HighMT_SS_TauIsoLepAntiIso"
#    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
#    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)
#
###########################################
#    Binning = array.array("d",[0,20,30,40,50,60,70,80,90,100,110,120,140,160,200,250,300,400,500])
#    NormMC="_tmass_LowMT_OS"
#    ShapeMC="_tmass_LowMT_OS"
#    ShapeW="_tmass_LowMT_OS"
#    NormQCD="_tmass_LowMT_SS"
#    ShapeQCD="_tmass_LowMT_SS_TauIsoLepAntiIso"
#    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
#    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)
#
###########################################
#    Binning = array.array("d",[0,20,30,40,50,60,70,80,90,100,110,120,140,160,200,250,300,400,500])
#    NormMC="_tmass_LowMT_SS_TauIsoLepAntiIso"
#    ShapeMC="_tmass_LowMT_SS_TauIsoLepAntiIso"
#    ShapeW="_tmass_LowMT_SS_TauIsoLepAntiIso"
#    NormQCD="_tmass_LowMT_SS_TauIsoLepAntiIso"
#    ShapeQCD="_tmass_LowMT_SS_TauIsoLepAntiIso"
#    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
#    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)
#
#
###########################################
#    Binning = array.array("d",[0,20,30,40,50,60,70,80,90,100,110,120,140,160,200,250,300,400,500])
#    NormMC="_tmass_LowMT_SS"
#    ShapeMC="_tmass_LowMT_SS"
#    ShapeW="_tmass_LowMT_SS"
#    NormQCD="_tmass_LowMT_SS"
#    ShapeQCD="_tmass_LowMT_SS"
#    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
#    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)
#
#
#
#
###########################################
#    Binning = array.array("d",[0,20,30,40,50,60,70,80,90,100,110,120,140,160,200,250,300,400,500])
#    NormMC="_LepPt_LowMT_SS_Total"
#    ShapeMC="_LepPt_LowMT_SS_Total"
#    ShapeW="_LepPt_LowMT_SS_Total"
#    NormQCD="_LepPt_LowMT_SS_Total"
#    ShapeQCD="_LepPt_LowMT_SS_Total"
#    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
#    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)
#
#
#
###########################################
#    Binning = array.array("d",[0,20,30,40,50,60,70,80,90,100,110,120,140,160,200,250,300,400,500])
#    NormMC="_LepPt_LowMT_SS_LepIso"
#    ShapeMC="_LepPt_LowMT_SS_LepIso"
#    ShapeW="_LepPt_LowMT_SS_LepIso"
#    NormQCD="_LepPt_LowMT_SS_LepIso"
#    ShapeQCD="_LepPt_LowMT_SS_LepIso"
#    MakeTheHistogram("MuTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",0,Binning)
#    MakeTheHistogram("EleTau",NormMC,ShapeMC,ShapeW,NormQCD,ShapeQCD,"",1,Binning)



