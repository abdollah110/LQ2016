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
SubRootDir = 'OutFiles_WEstimNoMETcut/'
#SubRootDir = 'OutFiles_WEstim_OLD/'
#SubRootDir = 'OutFiles_WEstim_NoCutOnTauPt/'
#SubRootDir = 'OutFiles_WEstim_RelIso03_Loose/'

verbos_ = False
TauScale = [ ""]



def add_lumi():
    lowX=0.69
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.03)
    lumi.SetTextFont (   42 )
    lumi.AddText("2.3 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.21
    lowY=0.75
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.05)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

def add_Preliminary():
    lowX=0.21
    lowY=0.68
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.05)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def make_legend():
    output = ROOT.TLegend(0.45, 0.75, 0.88, 0.88, "", "brNDC")
    output.SetLineWidth(0)
    output.SetLineStyle(0)
    output.SetFillStyle(0)
    output.SetBorderSize(0)
    output.SetTextFont(62)
    output.SetTextSize(0.035)
    return output




############################################################################################################
def _FileReturn(Name, channel,cat,HistoName,PostFix,CoMEnergy):
    if not os.path.exists(SubRootDir):
        os.makedirs(SubRootDir)
    myfile = TFile(SubRootDir + Name +CoMEnergy+ '.root')
    Histo =  myfile.Get(channel+HistoName + cat+ PostFix)
#    print "0--------->>>>>>  ", channel+HistoName + cat+ PostFix
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
            
            

            print "\n ----> Data before subtraction for " , NormQCD , " is = ", DataSampleQCDNormHist.Integral()
            QCDEstimation= (DataSampleQCDNormHist.Integral()- (TT_qcd+ZTT_qcd+W_qcd+SingleT_qcd+VV_qcd))
            print "\n ---->  Data aftre ____ subtraction for " , NormQCD , " is = = ", QCDEstimation
            

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
##   Fit Functions
#############################################################################################################
def _FIT_Jet(x, p):
    Land = p[2] * TMath.Landau(x[0], p[3], p[4])
    Pol0 = p[0]+p[1]*x[0]
    return Land + Pol0
def _FIT_Jet_Function(x, p):
    Land = p[2] * TMath.Landau(x, p[3], p[4])
    Pol0 = p[0]+p[1]*x
    return Land + Pol0



def _FIT_Lepton( x,  par) :
    return par[0] / (par[0]+ par[1]*math.exp(par[2] * x[0]))
def _FIT_Lepton_Function( x,  par) :
    if x < 300:
        return par[0] / (par[0]+ par[1]*math.exp(par[2] * x))
    else:
        return par[0] / (par[0]+ par[1]*math.exp(par[2] * 300))


#category_FakeEstim= "_DiJet"
category_FakeEstim= "_inclusive"
#category_FakeApply= "_DiJet"
category_FakeApply= "_DiNonBJet"
channelName="MuTau"
FR_vs_LeptonPT=0
if FR_vs_LeptonPT:
    ObjectPT="_LepPt"
    BinningFake = array.array("d",[0,20,30,40,50,55,60,65,70,75,80,85,90,100,120,150,200,250,300])
else:
    ObjectPT="_CloseJetMuPt"
    BinningFake = array.array("d",[0,20,30,40,50,60,70,80,90,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400])
#HistoFakeNum=ObjectPT+"_LowMT_SS_TauAntiIsoLepIso"
#HistoFakeDeNum=ObjectPT+"_LowMT_SSTauAntiIso"
#HistoFakeNum=ObjectPT+"_LowMT_SS"
#HistoFakeDeNum=ObjectPT+"_LowMT_SS_TauIso"
HistoFakeNum=ObjectPT+"_LowMT_SS_LepIso"
HistoFakeDeNum=ObjectPT+"_LowMT_SS_Total"

#############################################################################################################
##   Calculating the Fake Rate ---> "Linear Fit, 2 parameters"
#############################################################################################################
def Make_Tau_FakeRate():
    

    ShapeNum=MakeTheHistogram(channelName,HistoFakeNum,HistoFakeNum,"",0,BinningFake,1,category_FakeEstim)
    HistoNum=ShapeNum.Get("XXX")
    ShapeDeNum=MakeTheHistogram(channelName,HistoFakeDeNum,HistoFakeDeNum,"",0,BinningFake,1,category_FakeEstim)
    HistoDeNum=ShapeDeNum.Get("XXX")


    HistoNum.Divide(HistoDeNum)
    
    
    
    canv = TCanvas("canv", "histograms", 600, 600)
#    HistoNum.SetMinimum(0.5)
#    HistoNum.GetXaxis().SetRangeUser(0,400)
#    canv.SetLogy()
#    canv.SetGridx()
    canv.SetGridy()
    HistoNum.SetTitle("")
    if FR_vs_LeptonPT: HistoNum.GetXaxis().SetTitle("#mu p_{T} [GeV]")
    else: HistoNum.GetXaxis().SetTitle("Jet p_{T} [GeV]")
    HistoNum.GetYaxis().SetTitle("Muon Fake Rate  (Tight Iso + Id / Id)")
    HistoNum.GetYaxis().SetTitleOffset(1.3)
    HistoNum.GetYaxis().SetRangeUser(0.001,1)
    HistoNum.SetStats(0)
    HistoNum.SetMarkerStyle(20)
    
    
#    ######  Fit parameters for fake rate v.s. Jet Pt

#####  Fit parameters for fake rate v.s. muon Pt
 # number of parameters in the fit
    if FR_vs_LeptonPT:
        nPar = 3
        theFit=TF1("theFit", _FIT_Lepton, 50, 300,nPar)
        theFit.SetParameter(0, .2)
        theFit.SetParLimits(0, 0.1, 0.4)
        theFit.SetParameter(1, 4)
        theFit.SetParameter(2, -.30)

    else:
        nPar = 5
        theFit=TF1("theFit",_FIT_Jet,53,400,nPar)
#        theFit.SetParLimits(0,    0,     0.5);
#        theFit.SetParameter(0, 0.03)
#        theFit.SetParameter(1, 0)
        theFit.SetParameter(2, 0.6)
#        theFit.SetParameter(3, -0.6)
#        theFit.SetParameter(4, 96.6)



    HistoNum.Fit("theFit", "R0")
    HistoNum.Draw("E1")
    theFit.SetLineWidth(3)
    theFit.SetLineColor(3)
    FitParam=theFit.GetParameters()
    theFit.Draw("SAME")



    legende=make_legend()
    legende.AddEntry(HistoNum,"Data (Jet#rightarrow#mu rate)","lp")
    if FR_vs_LeptonPT:
        legende.AddEntry(theFit,"Fit (Exp. Function)","lp")
    else:
        legende.AddEntry(theFit,"Fit (Landau + Pol1)","lp")
    
    
    legende.Draw()
    
    l1=add_lumi()
    l1.Draw("same")
    l2=add_CMS()
    l2.Draw("same")
    l3=add_Preliminary()
    l3.Draw("same")
    

    canv.SaveAs("muFakeRate"+category_FakeEstim+channelName+".pdf")
    canv.SaveAs("muFakeRate"+category_FakeEstim+channelName+".root")


    if FR_vs_LeptonPT:
        return FitParam[0],FitParam[1],FitParam[2]
    else:
        return FitParam[0],FitParam[1],FitParam[2],FitParam[3],FitParam[4]


    ##########################################    ##########################################    ##########################################
    ##########################################    ##########################################    ##########################################
    ##########################################    ##########################################    ##########################################

if __name__ == "__main__":
    FR_FitMaram=Make_Tau_FakeRate()


    ##########################################
    Binning = array.array("d",[0,100,200,300,400,500,600,700,800,900,1000])
    
    if FR_vs_LeptonPT:
        NormQCD="_LepPt_HighMT_OS_TauIsoLepAntiIso"
        ShapeQCD="_LepPt_HighMT_OS_TauIsoLepAntiIso"
    else:
        NormQCD="_CloseJetMuPt_HighMT_OS_TauIsoLepAntiIso"
        ShapeQCD="_CloseJetMuPt_HighMT_OS_TauIsoLepAntiIso"
#        NormQCD="_CloseJetMuPt_HighMT_OS_LepAntiIso"
#        ShapeQCD="_CloseJetMuPt_HighMT_OS_Total"


    FileQCDCR=MakeTheHistogram(channelName,NormQCD,ShapeQCD,"",0,Binning,0,category_FakeApply)
    HistoQCDCR=FileQCDCR.Get("XXX")
    newcan = TCanvas("canv", "histograms", 600, 600)
    HistoQCDCR.Draw()
    qcdEstim=0
    for bin in xrange(50,400):
        value=HistoQCDCR.GetBinContent(bin)
#        if value < 0 : value=0  #********FIXME****** running out of Stat will create problem
        if FR_vs_LeptonPT:
            FR= _FIT_Lepton_Function(bin+1.5,FR_FitMaram)
        else:
            FR= _FIT_Jet_Function(bin+1.5,FR_FitMaram)
        qcdEstim += value * FR/(1-FR)
#    qcdEstim /= 2
    print  "\n\n\n\n------> Final QCD estimate is", qcdEstim, "\n\n\n\n"
    newcan.SaveAs("Onedplts.pdf")
    newcan.SaveAs("Onedplts.root")











Binning = array.array("d",[0,100,200,300,400,500,600,700,800,900,1000])
def Make_W_Control_Plots(NormQCD,ShapeQCD):
    
    FinalWPlots=MakeTheHistogram(channelName,NormQCD,ShapeQCD,"",0,Binning,0,category_FakeApply)

    TT=FinalWPlots.Get("TT")
    TT=TT.Rebin(10)

    ZTT=FinalWPlots.Get("ZTT")
    ZTT=ZTT.Rebin(10)

    SingleT=FinalWPlots.Get("SingleT")
    SingleT=SingleT.Rebin(10)

    VV=FinalWPlots.Get("VV")
    VV=VV.Rebin(10)

    W=FinalWPlots.Get("W")
    W=W.Rebin(10)

    Data=FinalWPlots.Get("data")
    Data=Data.Rebin(10)


    QCD=FinalWPlots.Get("XXX")
    QCD=QCD.Rebin(10)
    QCD.Scale(qcdEstim/QCD.Integral())

    dataMCScale=(Data.Integral()- ( qcdEstim+TT.Integral()+VV.Integral()+ZTT.Integral()+SingleT.Integral())) / W.Integral()
    print "\n\n************************************************************"
    print "Scale Factor is =",     dataMCScale
    print "Num is  =", Data.Integral()- ( qcdEstim + TT.Integral()+VV.Integral()+ZTT.Integral()+SingleT.Integral())
    print "Denum is =",  W.Integral()
    print "************************************************************\n\n"
    myOut = TFile("WEstimation"+NormQCD+".root" , 'RECREATE') # Name Of the output file


        
    tDirectory= myOut.mkdir("beforeScale")
    tDirectory.cd()
    tDirectory.WriteObject(VV,"VV")
    tDirectory.WriteObject(W,"W")
    tDirectory.WriteObject(W,"W120")
    tDirectory.WriteObject(W,"W125")
    tDirectory.WriteObject(TT,"TT")
    tDirectory.WriteObject(SingleT,"SingleTop")
    tDirectory.WriteObject(ZTT,"ZTT")
    tDirectory.WriteObject(QCD,"QCD")
    tDirectory.WriteObject(Data,"data_obs")

    tDirectory= myOut.mkdir("afterScale")
    tDirectory.cd()
    tDirectory.WriteObject(VV,"VV")
    W.Scale(  dataMCScale)
    tDirectory.WriteObject(W,"W")
    tDirectory.WriteObject(TT,"TT")
    tDirectory.WriteObject(SingleT,"SingleTop")
    tDirectory.WriteObject(ZTT,"ZTT")
    tDirectory.WriteObject(QCD,"QCD")
    tDirectory.WriteObject(Data,"data_obs")

    myOut.Close()




Make_W_Control_Plots("_tmass_HighMT_OS","_tmass_HighMT_OS_TauIsoLepAntiIso")
Make_W_Control_Plots("_ST_MET_HighMT_OS","_ST_MET_HighMT_OS_TauIsoLepAntiIso")
Make_W_Control_Plots("_LepPt_HighMT_OS","_LepPt_HighMT_OS_TauIsoLepAntiIso")
Make_W_Control_Plots("_TauPt_HighMT_OS","_TauPt_HighMT_OS_TauIsoLepAntiIso")
Make_W_Control_Plots("_ST_DiJet_HighMT_OS","_ST_DiJet_HighMT_OS_TauIsoLepAntiIso")
Make_W_Control_Plots("_MET_HighMT_OS","_MET_HighMT_OS_TauIsoLepAntiIso")
Make_W_Control_Plots("_LepEta_HighMT_OS","_LepEta_HighMT_OS_TauIsoLepAntiIso")
Make_W_Control_Plots("_TauEta_HighMT_OS","_TauEta_HighMT_OS_TauIsoLepAntiIso")


