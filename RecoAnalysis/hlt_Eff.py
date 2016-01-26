#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "abdollahmohammadi"
__date__ = "$Oct 31, 2013 12:02:55 PM$"

#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "abdollahmohammadi"
__date__ = "$Mar 8, 2013 3:00:22 PM$"

import math

import ROOT
from ROOT import Double
from ROOT import TAxis
from ROOT import TCanvas
from ROOT import TFile
from ROOT import TH1F
from ROOT import TH2F
from ROOT import TLatex
from ROOT import TLegend
from ROOT import TNtuple
from ROOT import TProfile
from ROOT import gBenchmark
from ROOT import gROOT
from ROOT import gRandom
from ROOT import gStyle
from ROOT import gSystem
import numpy
import ROOT
from ROOT import TCanvas
from ROOT import TFile
from ROOT import TH1F
from ROOT import TF1
from ROOT import TGraph
from ROOT import TPaveText
from array import array




#Mass=[200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]
Mass=[200,300,350,400,500,550,600,650,700,750,800,850,900,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500]
trgEff=[]

def _PlotMaker(file1, histo1, title, reB,col):


#M=TH1F(Fname,Fname,200,0,200)
    x = array("d", xrange(0,len(Mass)))
    y = array("d", xrange(0,len(Mass)))




    for mm in Mass:
        SigFile=TFile("OutFiles/out_"+str(mm)+".root")
#        numTrg=SigFile.Get("EleTau_ElePt_NoW8_NoMT_OS_inclusive")
#        denumTrg=SigFile.Get("EleTau_ElePt_NoW8_NoMT_OS_NoTrigger_inclusive")
        numTrg=SigFile.Get("MuTau_MuPt_NoW8_NoMT_OS_inclusive")
        denumTrg=SigFile.Get("MuTau_MuPt_NoW8_NoMT_OS_NoTrigger_inclusive")
        trgEff.append(numTrg.GetEntries()/denumTrg.GetEntries())
        print "numTrg.GetEntries()= ", numTrg.GetEntries()
    
    
    
    for inum in range(len(Mass)):
        print "trgEff= ", Mass[inum], "  and", trgEff[inum],  "num="
        x[inum] = Mass[inum]
        y[inum] = trgEff[inum]


    Mycanvas = TCanvas("asdf","asdf",800,800)
    Mycanvas.SetGridx()

    Mycanvas.SetGridy()

    MyGr= TGraph(len(x), x,y)
    MyGr.SetTitle("")
    MyGr.GetYaxis().SetRangeUser(0.5,1)
    MyGr.GetYaxis().SetTitle("Trigger Efficiency")
    MyGr.GetYaxis().SetLabelOffset(0.001)
    MyGr.GetYaxis().SetLabelSize(0.025)
    MyGr.GetXaxis().SetTitle("LQ Mass (GeV)")
#    MyGr.SetGridx()
    MyGr.Draw("AC*")
    Mycanvas.SaveAs("out.pdf")

#
#    canvas = TCanvas("canvas", "", 600, 600)
#    gStyle.SetOptStat(1111111);
#    gStyle.SetOptTitle(0);
#    canvas.SetFillColor(0)
#    canvas.SetTitle("qqqqqq")
#    canvas.SetName("")
#    canvas.SetBorderMode(0)
#    canvas.SetBorderSize(2)
#    canvas.SetFrameBorderMode(0)
#    canvas.SetFrameLineWidth(2)
#    canvas.SetFrameBorderMode(0)
#    canvas.SetLogy();
#
#
#
#    File_1 = TFile(file1, "OPEN")
#    Histo_1 = File_1.Get(histo1)
#
#
#
#    Histo_1.Rebin(reB)
#    Histo_1.SetFillColor(col)
##    Histo_1.SetLineWidth(3)
#    Histo_1.GetXaxis().SetTitle(title)
#    Histo_1.GetYaxis().SetTitle("# of events")
#    Histo_1.GetYaxis().SetTitleOffset(1.3)
##    print Histo_1.GetMaximum()
##    Histo_1.GetYaxis().SetRangeUser(0,2*Histo_1.GetMaximum() );
#    Histo_1.Draw()
##    print  "entery of ", Histo_1.GetName(), "  is= ", Histo_1.Integral(),  "   =  ", Histo_1.Integral()/39996.
#
#
#
#    legend_ = TLegend(0.6, 0.4, 0.9, 0.6)
#    legend_.SetFillColor(0)
#    legend_.SetBorderSize(0)
#    legend_.SetTextSize(.03)
#    legend_.AddEntry(Histo_1,  title + "(GenLevel)", "l")
#   
#    legend_.Draw("hist")
#    
#
#    ChannelName = histo1 + ".pdf"
#    canvas.SaveAs(ChannelName)


if __name__ == "__main__":
    _PlotMaker("newtest_4.root", "Mass-LQ_plus", "M_{#tau^{+}Q^{-}}",1,5)
#    _PlotMaker("newtest_4.root", "Mass-LQ_minus", "M_{#tau^{-}Q^{+}}",1,7)









