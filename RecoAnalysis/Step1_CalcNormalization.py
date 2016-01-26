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
from ROOT import gStyle
from ROOT import gSystem

gROOT.Reset()
import os
ROOT.gROOT.SetBatch(True)
SubRootDir = 'OutFiles/'
UseTauPolarOff = True


signal = ['bba1GenFil_']
mass = [25,30,  35, 40, 45, 50, 55,  60, 65, 70, 75, 80]
SMHiggs_BackGround = ['ggH_SM125', 'qqH_SM125', 'VH_SM125', 'ggHWW_SM125', 'qqHWW_SM125', 'VHWW_SM125']



category = ["_inclusive",  "_DiJet", "_JetBJet"]
channel = ["MuTau", "EleTau"]
lenghtSig = len(signal) * len(mass) +1

digit = 5
verbos_ = True
lowBin=0





def getHistoIntegral(PostFix,CoMEnergy,Name,chan,cat,Histogram):
    myfileSub = TFile(SubRootDir + Name +CoMEnergy+ '.root')
    HistoSub = myfileSub.Get(chan+Histogram+ cat+PostFix )
    value = 10E-7
    if (HistoSub):
        value = HistoSub.Integral()
        value = round(value, digit)
    return value

##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################


def make2DTable(Observable,PostFix,CoMEnergy):
    myOut = TFile("Yield"+CoMEnergy+PostFix+".root", 'RECREATE')
    FullResultsOS  = TH2F('FullResults', 'FullResults', 8, 0, 8, 30, 0, 30)
    FullResultsSSQCDShape  = TH2F('FullResults', 'FullResults', 8, 0, 8, 30, 0, 30)

    for categ in range(len(category)):
        for chl in range(len(channel)):
            print "\n##################################################################################################"
            print "starting category and channel", category[categ], channel[chl], 'PostFix= ',PostFix
            print "##################################################################################################\n"
#            ##################################################################################################
#            #   Signal Estimation
#            ##################################################################################################
#            print "\nDoing Signal estimation in ", category[categ], channel[chl]
#            for sig in range(len(signal)):
#                for m in range(len(mass)):#    for m in range(110, 145, 5):
#
#                    Histogram = Observable+"_mTLess30_OS"
#                    XLoc= categ + len(category)*chl + 1
#                    YLoc= sig * len(mass) + m + 1
#                    Name= str(signal[sig]) +str(mass[m])
##                    Name= str(signal[sig]) + "_"+str(mass[m])
#
#                    value = getHistoIntegral(PostFix,CoMEnergy,Name ,channel[chl],category[categ],Histogram)
#                    FullResults.SetBinContent(XLoc,YLoc , value)
#                    FullResults.GetYaxis().SetBinLabel(YLoc, Name)
#
#                    if (verbos_): print "Processing ...   =", Name, " coordinate was=",XLoc,YLoc, "  and the value is=",value 
             ##################################################################################################
            #   TT Estimation
            ##################################################################################################
            print "\nDoing TT, BG estimation  in ", category[categ], channel[chl]

            DYIndex = ""
            Name= "TTJets"
            YLoc= lenghtSig  +2
            ## Similar To ALL ##
            XLoc= categ + len(category)*chl + 1
            HistogramOS = Observable+"_OS"+DYIndex
            HistogramSS = Observable+"_SS"+DYIndex


            valueOS = getHistoIntegral(PostFix,CoMEnergy, Name,channel[chl],category[categ],HistogramOS)
            FullResultsOS.SetBinContent(XLoc,YLoc , valueOS)
            FullResultsOS.GetYaxis().SetBinLabel(YLoc, Name)

            valueSSTT = getHistoIntegral(PostFix,CoMEnergy, Name,channel[chl],category[categ],HistogramSS)
            
            if (verbos_): print "Processing ...  =", Name, "  was=",XLoc,YLoc, "  and the OS value is=",valueOS,  "  and the SS value is=",valueSSTT

        ##################################################################################################
        #   ZTT Estimation
        ##################################################################################################
            print "\nDoing ZTT, BG estimation in ", category[categ], channel[chl]
#            for BG_ZTT in range(len(Z_BackGround)):

            DYIndex = ""
#            Name= "Embedded"+channel[chl]
            Name= "DYJetsToLL"
            YLoc= lenghtSig + 3
            XLoc= categ + len(category)*chl + 1

            HistogramOS = Observable+"_OS"+DYIndex
            HistogramSS = Observable+"_SS"+DYIndex
            
            valueOS = getHistoIntegral(PostFix,CoMEnergy, Name,channel[chl],category[categ],HistogramOS)
            FullResultsOS.SetBinContent(XLoc,YLoc , valueOS)
            FullResultsOS.GetYaxis().SetBinLabel(YLoc, Name)
            
            valueSSZTT = getHistoIntegral(PostFix,CoMEnergy, Name,channel[chl],category[categ],HistogramSS)

            if (verbos_): print "Processing ...  =", Name, "  was=",XLoc,YLoc, "  and the OS value is=",valueOS,  "  and the SS value is=",valueSSZTT
        ##################################################################################################
        #   W Estimation
        ##################################################################################################
            print "\nDoing W BG estimation in ", category[categ], channel[chl]
            
            Name= "WJetsToLNu"
            YLoc= lenghtSig + 4
            XLoc= categ + len(category)*chl + 1
            HistogramOS = Observable+"_OS"+DYIndex
            HistogramSS = Observable+"_SS"+DYIndex

            valueOS = getHistoIntegral(PostFix,CoMEnergy, Name,channel[chl],category[categ],HistogramOS)
            FullResultsOS.SetBinContent(XLoc,YLoc , valueOS)
            FullResultsOS.GetYaxis().SetBinLabel(YLoc, Name)
            
            valueSSW = getHistoIntegral(PostFix,CoMEnergy, Name,channel[chl],category[categ],HistogramSS)
            
            if (verbos_): print "Processing ...  =", Name, "  was=",XLoc,YLoc, "  and the OS value is=",valueOS,  "  and the SS value is=",valueSSW
            
        ##################################################################################################
        #   QCD Estimation
        ##################################################################################################
            print "\nDoing QCD  estimation in ", category[categ], channel[chl]
            
            Name= "Data"
            YLoc= lenghtSig + 5
            XLoc= categ + len(category)*chl + 1
#            HistogramOS = Observable+"_OS"
            HistogramSS = Observable+"_SS"
            Nameqcd="QCD"


            valueSSdata = getHistoIntegral(PostFix,CoMEnergy, Name,channel[chl],category[categ],HistogramSS)
            valueOS=(valueSSdata - (valueSSW + valueSSZTT + valueSSTT)) *1.06
            FullResultsOS.SetBinContent(XLoc,YLoc , valueOS)
            FullResultsOS.GetYaxis().SetBinLabel(YLoc, Nameqcd)
            
            if (verbos_): print "Processing ...   =", Name, "  was=",XLoc,YLoc, "  and the SS value is=",valueSSdata
        ##################################################################################################
        #   Data Estimation
        ##################################################################################################
            print "\nDoing Data  estimation in ", category[categ], channel[chl]

            XLoc= categ + len(category)*chl + 1
            YLoc= lenghtSig + 6
            Name='Data'
            HistogramOS = Observable+"_OS"+DYIndex

            valueOS = getHistoIntegral(PostFix,CoMEnergy, Name,channel[chl],category[categ],HistogramOS)
            FullResultsOS.SetBinContent(XLoc,YLoc , valueOS)
            FullResultsOS.GetYaxis().SetBinLabel(YLoc, Name)

            if (verbos_): print "Processing ...   =", Name, " coordinate was=",XLoc,YLoc, "  and the OS value is=",valueOS
            #########################################################################
            FullResultsOS.GetXaxis().SetBinLabel(categ + len(category)*chl + 1, channel[chl]+category[categ])
            #########################################################################
    myOut.WriteObject(FullResultsOS,"FullResultsOS")

    myCanvas = TCanvas()
    gStyle.SetOptStat(0)
    FullResultsOS.Draw('text')
    myCanvas.SaveAs("tableAllOS"+PostFix+CoMEnergy+".pdf")

if __name__ == "__main__":
    make2DTable("_VisMass","", "")
#    make2DTable("_ST_JetBJet","", "")
#    make2DTable("_ST_NumJet","", "")

