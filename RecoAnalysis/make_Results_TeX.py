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

####################################################################
BLIND = False
####################################################################
channel = ["mt", "et"]
signal = ['LQ','RHW']
signalname = ['LQ','RHW']
mass = [700, 2000]

lenghtSig = len(signal) * len(mass)
round_sig = 3
round_BG = 2





def MakeTheHistogram(RootFile,Category,text_file):
#    Table_File = TFile("Yield"+CoMEnergy+""+".root")
#    Table_Hist = Table_File.Get('FullResults')
#    Table_Error = Table_File.Get('FullError')

    RName=["lq_mt"]

    RootFile=TFile("lq_mt.inputs-sm-13TeV.root")
    Category="MuTau_JetBJet"
    signal  = RootFile.Get(Category+"/LQ_700").Integral()
    ZTT  = RootFile.Get(Category+"/ZTT").Integral()
    TT  = RootFile.Get(Category+"/TT").Integral()
    QCD  = RootFile.Get(Category+"/QCD").Integral()
    W  = RootFile.Get(Category+"/W").Integral()
    SingleTop  = RootFile.Get(Category+"/SingleTop").Integral()
    VV  = RootFile.Get(Category+"/VV").Integral()
    Data=RootFile.Get(Category+"/data_obs").Integral()
    
    Samples = [signal, ZTT, TT,QCD,W,SingleTop, VV,Data]
    
    text_file.write('\\begin{tabular}{|c|c|c|c|c|c|c|c|c|}\n')
    text_file.write('\\hline\n')
    text_file.write('Channel & Signal & ZZ & TT & QCD & W &SingleTop & VV & Data \\\\ \n')
    text_file.write('\\hline\n')
#    for chl in range(len(channel)):
#        text_file.write("%s" %channel[chl])
#        ###################################### Filling Signal ZH and WH ########
#        for sig in range(len(signal)):
#            for m in range(len(mass)):#    for m in range(110, 145, 5):
#
#                normal = round(Table_Hist.GetBinContent(chl + 1, sig * len(mass) + m + 1),round_sig)
#                normalEr = round(Table_Error.GetBinContent(chl + 1, sig * len(mass) + m + 1),round_sig)
#                if (mass[m] == 125): text_file.write('& %.3f  $\pm$ %.3f ' %(normal,normalEr))
#                if (mass[m] == 125): print '& %.3f  $\pm$ %.3f ' %(normal,normalEr) ,
#
#        ###################################### Filling Reducible ########
#        normal = round(Table_Hist.GetBinContent(chl + 1, lenghtSig  + 2),round_BG)
#        normalEr = round(Table_Error.GetBinContent(chl + 1, lenghtSig  + 2),round_BG)
#        text_file.write('&%.2f  $\pm$ %.2f ' %(normal,normalEr))
#        print '&%.2f  $\pm$ %.2f ' %(normal,normalEr) ,
#        ###################################### Filling ZZ and Data ########
    for bg in range (len(Samples)):

        text_file.write('&%.2f  $\pm$ %.2f ' %(Samples[bg],Samples[bg]))
        print '&%.2f  $\pm$ %.2f ' %(Samples[bg],Samples[bg])

            
        print ""
        text_file.write('\\\\\n')
    text_file.write('\\hline\n')
    text_file.write('\\end{tabular}')



if __name__ == "__main__":
    
    RootFile=TFile("lq_et.inputs-sm-13TeV.root")
    Category="EleTau_JetBJet"
    text_file = open("TEX_lq.tex", "w")
    MakeTheHistogram(RootFile,Category,text_file)



#
#
#    MakeTheHistogram("_8TeV",text_file)
#    text_file.close()
#
#    text_file = open("Full7TeVTableZH.tex", "w")
#    MakeTheHistogram("_7TeV",text_file)
#    text_file.close()