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
from ROOT import TMath
from ctypes import *
import ROOT as r
import array

gROOT.Reset()
import os




ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.ProcessLine('.x rootlogon.C')
#SubRootDir = 'OutFiles_WEstim/'
#SubRootDir = 'OutFiles_WEstim_NoCutOnTauPt/'
#SubRootDir = 'OutFiles_TMass60_noBjet20Gev/'
SubRootDir = 'OutFiles_WEstim_RelIso02/'

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

#channelDirectory = ["MuTau", "EleTau"]
channelDirectory = ["MuTau"]

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
def MakeTheHistogram(channel,NormQCD,ShapeQCD,CoMEnergy,chl,Binning,doBinning,NameCat):




#    myOut = TFile("WEstimation_TotalRootForLimit_"+channel + NormMC+".root" , 'RECREATE') # Name Of the output file
#
#    icat=-1
#    for NameCat in category:
#        icat =icat +1
#        print "starting NameCat and channel and HistoName ", NameCat, channel, NormMC
#
#        tDirectory= myOut.mkdir(channelDirectory[chl] + str(NameCat))
#        tDirectory.cd()
#            NameCat="_inclusive"
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


#            if (SingleTSampleQCDShapeHist) : DataSampleQCDShapeHist.Add(SingleTSampleQCDShapeHist, -1)
#            if (VVSampleQCDShapeHist): DataSampleQCDShapeHist.Add(VVSampleQCDShapeHist, -1)
#            DataSampleQCDShapeHist.Add(TTSampleQCDShapeHist, -1)
#            DataSampleQCDShapeHist.Add(ZTTSampleQCDShapeHist, -1)
#            DataSampleQCDShapeHist.Add(WSampleQCDShapeHist, -1)


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
            
            
            print "Data before subtraction is = ", DataSampleQCDNormHist.Integral()
            QCDEstimation= (DataSampleQCDNormHist.Integral()- (TT_qcd+ZTT_qcd+W_qcd+SingleT_qcd+VV_qcd))
            print "Data aftre ____ subtraction is = ", QCDEstimation

#            NameOut= "QCD"+str(TauScaleOut[tscale])
            DataSampleQCDShapeHist.Scale(QCDEstimation/DataSampleQCDShapeHist.Integral())  # The shape is from btag-Loose Need get back norm
            if doBinning:    RebinedHist= DataSampleQCDShapeHist.Rebin(len(Binning)-1,"",Binning)
            else : RebinedHist= DataSampleQCDShapeHist
#            tDirectory.WriteObject(RebinedHist,NameOut)

            NewShapeForQCD=TFile("Extra/XXX.root","RECREATE")
            NewShapeForQCD.WriteObject(RebinedHist,"XXX")
            NewShapeForQCD.WriteObject(DataSampleQCDNormHist,"data")
            NewShapeForQCD.WriteObject(WSampleQCDNormHist,"W")
            NewShapeForQCD.WriteObject(ZTTSampleQCDNormHist,"ZTT")
            NewShapeForQCD.WriteObject(TTSampleQCDNormHist,"TT")
            NewShapeForQCD.WriteObject(VVSampleQCDNormHist,"VV")
            NewShapeForQCD.WriteObject(SingleTSampleQCDNormHist,"SingleT")
            return NewShapeForQCD
            








#############################################################################################################
##   Fit Function
#############################################################################################################

#def _FIT_FAKE(x, p):
#    Land = p[1] * TMath.Landau(x[0], p[2], p[3])
#    Pol0 = p[0]
#    return Land + Pol0
def _FIT_FAKE(x, p):
    Land = p[2] * TMath.Landau(x[0], p[3], p[4])
    Pol0 = p[0]+p[1]*x[0]
    return Land + Pol0
def _FIT_Jet_Function(x, p):
    Land = p[2] * TMath.Landau(x, p[3], p[4])
    Pol0 = p[0]+p[1]*x
    return Land + Pol0



#def fitFunc_Linear2Par(x,par):
#    return par[0] + (par[1] * x[0])
#def Func_Linear2Par(x,par0,par1):
#    return par0 +  (par1 * x)
#
def Func_Exp3Par( x,  par) :
    return par[0] + par[1]* math.exp(par[2]* x[0])
#    return par0 + par1 * math.exp(par2 * x)
#def Func_Exp3Par( x,  par) :
#    return par[0] / (par[0]+ par[1]*math.exp(par[2] * x[0]))

def Func_Exp3Par_retunr( x,  par0,par1,par2) :
    return par0 / (par0+ par1*math.exp(par2 * x))

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
    Binning = array.array("d",[0,20,30,40,50,60,70,80,90,100,120,140,160,180,200,240,280,320,360,400])
    NormQCD="_CloseJetTauPt_LowMT_SS_TauIsoLepAntiIso"
#    NormQCD="_TauPt_LowMT_SS_TauIsoLepAntiIso"
#    NormQCD="_TauPt_LowMT_SS"
#    NormQCD="_TauPt_LowMT_SS_TauIso"
    ShapeNum=MakeTheHistogram("MuTau",NormQCD,NormQCD,"",0,Binning,1,"_inclusive")
    HistoNum=ShapeNum.Get("XXX")
#    HistoNum= HistoNum.Rebin(len(Binning_PT)-1,"",Binning_PT)
#    HistoNum.Scale(1000/HistoNum.Integral())

    
    
    
#    Binning = array.array("d",[0,20,30,40,50,60,70,80,90,100,120,150,200,300,400])
    NormQCD="_CloseJetTauPt_LowMT_SS_LepAntiIso"
#    NormQCD="_TauPt_LowMT_SS_LepAntiIso"
#    NormQCD="_TauPt_LowMT_SS_LepIso"
#    NormQCD="_TauPt_LowMT_SS_Total"

#    NormQCD="_TauPt_LowMT_SS_TauIso"

    ShapeDeNum=MakeTheHistogram("MuTau",NormQCD,NormQCD,"",0,Binning,1,"_inclusive")
    HistoDeNum=ShapeDeNum.Get("XXX")
#    HistoDeNum= HistoDeNum.Rebin(len(Binning_PT)-1,"",Binning_PT)
#    HistoDeNum.Scale(1000/HistoDeNum.Integral())

    HistoNum.Divide(HistoDeNum)
    
    canv = TCanvas("canv", "histograms", 600, 600)
    HistoNum.SetMinimum(0.5)
    #    HistoNum.GetXaxis().SetRangeUser(0,60)
    HistoNum.GetXaxis().SetRangeUser(0,400)
    canv.SetGridx()
    canv.SetLogy()
    canv.SetGridy()
    HistoNum.SetTitle("")
    HistoNum.GetXaxis().SetTitle("#tau p_{T} [GeV]")
    HistoNum.GetYaxis().SetTitle("Tau Fake Rate ")
    HistoNum.GetYaxis().SetTitleOffset(1.3)
    HistoNum.GetYaxis().SetRangeUser(.001,1)
#    HistoNum.GetYaxis().SetRangeUser(.002,0.2)
    HistoNum.SetStats(0)
    HistoNum.SetMarkerStyle(20)
    
    theFit=TF1("theFit",_FIT_FAKE,50,500,5)
    theFit.SetParLimits(0,    0,     0.5);
    theFit.SetParameter(0, 0.03)
    theFit.SetParameter(1, 0)
    theFit.SetParameter(2, 0.6)
    theFit.SetParameter(3, -0.6)
    theFit.SetParameter(4, 96.6)
#    theFit.SetParameter(5, 1)

    
    nPar = 3 # number of parameters in the fit
#    theFit=TF1("theFit", "TMath::Landau(x,[0],[1],0)",50,200)
#    theFit=TF1("theFit", Func_Exp3Par, 50, 400,nPar)
#    theFit.SetParameter(0, .2)
#    theFit.SetParameter(1, .5)
##    theFit.SetParLimits(1, 1, 50)
#    theFit.SetParameter(2, -1)

    HistoNum.Fit("theFit", "R0")
    HistoNum.Draw("E1")
#    theFit.SetLineWidth(3)
#    theFit.SetLineColor(3)
#    FitParam=theFit.GetParameters()
#    FitParamEre=theFit.GetParErrors()
    theFit.Draw("SAME")
    canv.SaveAs("FR_Tau_fitResults_TauFakeRate"+catName+channelName+".pdf")
    canv.SaveAs("FR_Tau_fitResults_TauFakeRate"+catName+channelName+".root")    
#
#    FitMarameter=[FitParam[0],FitParam[1],FitParam[2]]
#    FitMarameterUnc=[FitParamEre[0],FitParamEre[1],FitParamEre[2]]
#    return FitMarameter,FitMarameterUnc

    return 0,10

    ##########################################    ##########################################    ##########################################
    ##########################################    ##########################################    ##########################################
    ##########################################    ##########################################    ##########################################

if __name__ == "__main__":
    FR_FitMaram=Make_Tau_FakeRate()[1]
#    print "\n\n ---->   ", FR_FitMaram[0], FR_FitMaram[1], FR_FitMaram[2]
#    ##########################################
#    Binning = array.array("d",[0,100,200,300,400,500,600,700,800,900,1000])
#    NormQCD="_TauPt_OS"
#    ShapeQCD="_TauPt_OS_Total"
#    FileQCDCR=MakeTheHistogram("MuTau",NormQCD,ShapeQCD,"",0,Binning,0,"_DiJet")
##    FileQCDCR=MakeTheHistogram("MuTau",NormQCD,ShapeQCD,"",0,Binning,0,"_inclusive")
#    HistoQCDCR=FileQCDCR.Get("XXX")
##    HistoQCDCR.Rebin(2)
#    newcan = TCanvas("canv", "histograms", 600, 600)
#    HistoQCDCR.Draw()
#    qcdEstim=0
#    for bin in xrange(0,300):
#        value=HistoQCDCR.GetBinContent(bin)
#        if value < 0 : value=0
#        FR= Func_Exp3Par_retunr(bin+1.5,FR_FitMaram[0],FR_FitMaram[1],FR_FitMaram[2] )
#        qcdEstim += value * FR/(1-FR)
#    print  "------> Final estimate is", sum
#    newcan.SaveAs("tauFROnedplts.pdf")
#    newcan.SaveAs("tauFROnedplts.root")

#    NormQCD="_ST_JetBJet_HighMT_OS"
#    ShapeQCD="_ST_JetBJet_HighMT_OS_TauIsoLepAntiIso"
#    FinalWPlots=MakeTheHistogram("MuTau",NormQCD,ShapeQCD,"",0,Binning,0,"_DiNonBJet")
##    FinalWPlots=MakeTheHistogram("MuTau",NormQCD,ShapeQCD,"",0,Binning,0,"_inclusive")
#
#    TT=FinalWPlots.Get("TT")
#    TT_rb=TT.Rebin(len(Binning)-1,"",Binning)
#
#    ZTT=FinalWPlots.Get("ZTT")
#    ZTT_rb=ZTT.Rebin(len(Binning)-1,"",Binning)
#
#    SingleT=FinalWPlots.Get("SingleT")
#    SingleT_rb=SingleT.Rebin(len(Binning)-1,"",Binning)
#
#    VV=FinalWPlots.Get("VV")
#    VV_rb=VV.Rebin(len(Binning)-1,"",Binning)
#
#    W=FinalWPlots.Get("W")
#    W_rb=W.Rebin(len(Binning)-1,"",Binning)
#
#    Data=FinalWPlots.Get("data")
#    Data_rb=Data.Rebin(len(Binning)-1,"",Binning)
#
#    
#    QCD=FinalWPlots.Get("XXX")
#    QCD_rb=QCD.Rebin(len(Binning)-1,"",Binning)
#    QCD_rb.Scale(qcdEstim/QCD_rb.Integral())
#
#    dataMCScale=(Data.Integral()- ( qcdEstim+TT.Integral()+VV.Integral()+ZTT.Integral()+SingleT.Integral())) / W.Integral()
#    print "Scale Factor is =",     dataMCScale
#    print "Num is  =", Data.Integral()- ( qcdEstim + TT.Integral()+VV.Integral()+ZTT.Integral()+SingleT.Integral())
#    print "Denum is =",  W.Integral()
#
#    myOut = TFile("fileWEstim.root" , 'RECREATE') # Name Of the output file
#    
#    
#        
#    tDirectory= myOut.mkdir("beforeScale")
#    tDirectory.cd()
#    tDirectory.WriteObject(VV_rb,"VV")
#    tDirectory.WriteObject(W_rb,"W")
#    tDirectory.WriteObject(TT_rb,"TT")
#    tDirectory.WriteObject(SingleT_rb,"SingleTop")
#    tDirectory.WriteObject(ZTT_rb,"ZTT")
#    tDirectory.WriteObject(QCD_rb,"QCD")
#    tDirectory.WriteObject(Data_rb,"data_obs")
#
#    tDirectory= myOut.mkdir("afterScale")
#    tDirectory.cd()
#    tDirectory.WriteObject(VV_rb,"VV")
#    W_rb.Scale(  dataMCScale)
#    tDirectory.WriteObject(W_rb,"W")
#    tDirectory.WriteObject(TT_rb,"TT")
#    tDirectory.WriteObject(SingleT_rb,"SingleTop")
#    tDirectory.WriteObject(ZTT_rb,"ZTT")
#    tDirectory.WriteObject(QCD_rb,"QCD")
#    tDirectory.WriteObject(Data_rb,"data_obs")
#
#    myOut.Close()





