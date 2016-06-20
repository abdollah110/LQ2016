#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.
#http://root.cern.ch/viewvc/trunk/tutorials/pyroot/hsimple.py?revision=20881&view=markup
__author__ = "abdollahmohammadi"
__date__ = "$Feb 23, 2013 10:39:33 PM$"

import re
from sys import argv, stdout, stderr, exit
from optparse import OptionParser
import math
import ROOT
import sys
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

gROOT.Reset()
import os
ROOT.gROOT.SetBatch(True)


def GetTH1Hist(outFile,sample,Category):
    RootFile= TFile(outFile)
    Hist  = RootFile.Get(Category+"/"+sample)
    HistRB=Hist.Rebin(Hist.GetNbinsX())
    return   HistRB.Integral(), HistRB.GetBinError(1)




##############  LQ   ##############

SampleList = ["LQ_", "ZTT", "TT","QCD","W","SingleTop", "VV","TotBG","data_obs"]
SampleList_BG = [ "ZTT", "TT","QCD","W","SingleTop", "VV"]
text_file = open("TEX_lq.tex", "w")
text_file.write('\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|}\n')
text_file.write('\\caption{LQ}\n')
text_file.write('\\hline\n')
text_file.write('Channel & Signal & ZZ & TT & QCD & W &SingleTop & VV & Total BG&Data \\\\ \n')
text_file.write('\\hline\n')

CH=["mt","et"]

def _getTotBG(channel):
    Integral=0
    Error=0
    for Samples in SampleList_BG:
        
        RootFile="LIMIT/final_lq_"+channel+"_700.root"
        Category="lq_"+channel+"_1_13TeV_postfit"
        Integral = Integral+ GetTH1Hist(RootFile,Samples,Category)[0]
        Error = Error+ GetTH1Hist(RootFile,Samples,Category)[1]
    return Integral,Error
        


for channel in CH:
    text_file.write(channel)
    for Samples in SampleList:
        
        RootFile="LIMIT/final_lq_"+channel+"_700.root"
        Category="lq_"+channel+"_1_13TeV_postfit"
        
        if Samples=="TotBG":
            Integral=_getTotBG(channel)[0]
            Error=_getTotBG(channel)[1]
        else:
            Integral= GetTH1Hist(RootFile,Samples,Category)[0]
            Error= GetTH1Hist(RootFile,Samples,Category)[1]
        
        text_file.write('&%.1f  $\pm$ %.1f ' %(Integral,Error))
        print '&%.1f  $\pm$ %.1f ' %(Integral,Error)
    text_file.write('\\\\\n')
    text_file.write('\\hline\n')
text_file.write('\\label{lq}\n')
text_file.write('\\end{tabular}')

##############  RHW   ##############

SampleList = ["RHW_", "ZTT", "TT","QCD","W","SingleTop", "VV","TotBG","data_obs"]
SampleList_BG = [ "ZTT", "TT","QCD","W","SingleTop", "VV"]
text_file = open("TEX_rw.tex", "w")
text_file.write('\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|}\n')
text_file.write('\\caption{RHW}\n')
text_file.write('\\hline\n')
text_file.write('Channel & Signal & ZZ & TT & QCD & W &SingleTop & VV & Total BG&Data \\\\ \n')
text_file.write('\\hline\n')

CH=["mt","et"]


def _getTotBG(channel):
    Integral=0
    Error=0
    for Samples in SampleList_BG:
        
        RootFile="LIMIT/final_rw_"+channel+"_2000.root"
        Category="RHW__"+channel+"_1_13TeV_postfit"
        Integral = Integral+ GetTH1Hist(RootFile,Samples,Category)[0]
        Error = Error+ GetTH1Hist(RootFile,Samples,Category)[1]
    return Integral,Error


for channel in CH:
    text_file.write(channel)
    for Samples in SampleList:
        
        RootFile="LIMIT/final_rw_"+channel+"_2000.root"
        Category="RHW__"+channel+"_1_13TeV_postfit"
        
        if Samples=="TotBG":
            Integral=_getTotBG(channel)[0]
            Error=_getTotBG(channel)[1]
        else:
            Integral= GetTH1Hist(RootFile,Samples,Category)[0]
            Error= GetTH1Hist(RootFile,Samples,Category)[1]
        
        text_file.write('&%.1f  $\pm$ %.1f ' %(Integral,Error))
        print '&%.1f  $\pm$ %.1f ' %(Integral,Error)
    text_file.write('\\\\\n')
    text_file.write('\\hline\n')
text_file.write('\\label{rhw}\n')
text_file.write('\\end{tabular}')




