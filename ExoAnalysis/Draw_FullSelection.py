#!/usr/bin/env python
import ROOT
import re
from array import array

RB_=10
def add_lumi():
    lowX=0.69
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.06)
    lumi.SetTextFont (   42 )
    lumi.AddText("2.3 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.21
    lowY=0.70
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.08)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi

def add_Preliminary():
    lowX=0.21
    lowY=0.63
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.06)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Preliminary")
    return lumi

def make_legend():
        output = ROOT.TLegend(0.65, 0.4, 0.92, 0.82, "", "brNDC")
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillStyle(0)
        output.SetBorderSize(0)
        output.SetTextFont(62)
        return output


def MakePlot(FileName,categoriy,HistName,Xaxis,MaxRange,sig,sigLeg):
    ROOT.gStyle.SetFrameLineWidth(3)
    ROOT.gStyle.SetLineWidth(3)
    ROOT.gStyle.SetOptStat(0)
    RB_=1

    c=ROOT.TCanvas("canvas","",0,0,600,600)
    c.cd()

    file=ROOT.TFile(FileName,"r")

    adapt=ROOT.gROOT.GetColor(12)
    new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1
#    trans=ROOT.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(),adapt.GetBlue(), "",0.5)

#    categories=["MuTau_DiJet","MuTau_JetBJet"]
#    ncat=

    Data=file.Get(categoriy).Get("data_obs")
    Data.Rebin(RB_)
    QCD=file.Get(categoriy).Get("QCD")
    QCD.Rebin(RB_)
    W=file.Get(categoriy).Get("W")
    W.Rebin(RB_)
    TT=file.Get(categoriy).Get("TT")
    TT.Rebin(RB_)
    VV=file.Get(categoriy).Get("VV")
    VV.Rebin(RB_)
    #W.Add(VV)
    SingleT=file.Get(categoriy).Get("SingleTop")
    SingleT.Rebin(RB_)
    DYS=file.Get(categoriy).Get("ZTT")
    DYS.Rebin(RB_)
    
    Signal=file.Get(categoriy).Get(sig)
    Signal.Scale(10)
    Signal.Rebin(RB_)
#    Signal.SetFillStyle(0.)
    Signal.SetLineStyle(11)
#    Signal.SetLineWidth(3.)
#    Signal.SetLineColor(kBlue)

    
    

    Data.GetXaxis().SetTitle("")
    Data.GetXaxis().SetTitleSize(0)
    Data.GetXaxis().SetNdivisions(505)
    Data.GetYaxis().SetLabelFont(42)
    Data.GetYaxis().SetLabelOffset(0.01)
    Data.GetYaxis().SetLabelSize(0.06)
    Data.GetYaxis().SetTitleSize(0.075)
    Data.GetYaxis().SetTitleOffset(1.04)
    Data.SetTitle("")
    Data.GetYaxis().SetTitle("Events")



    QCD.SetFillColor(ROOT.TColor.GetColor(408, 106, 154))
    W.SetFillColor(ROOT.TColor.GetColor(200, 2, 285))
    TT.SetFillColor(ROOT.TColor.GetColor(208, 376, 124))
    SingleT.SetFillColor(ROOT.TColor.GetColor(150, 132, 232))
    VV.SetFillColor(ROOT.TColor.GetColor(200, 282, 232))
    DYS.SetFillColor(ROOT.TColor.GetColor(108, 226, 354))

    Data.SetMarkerStyle(20)
    Data.SetMarkerSize(1)
    QCD.SetLineColor(ROOT.TColor.GetColor(408, 106, 154))
    W.SetLineColor(ROOT.TColor.GetColor(200, 2, 285))
    TT.SetLineColor(ROOT.TColor.GetColor(208, 376, 124))
#    DYS.SetLineColor(ROOT.EColor.kBlack)
#    VV.SetLineColor(ROOT.EColor.kBlack)
#    SingleT.SetLineColor(ROOT.EColor.kBlack)
#    Data.SetLineColor(ROOT.EColor.kBlack)
    Data.SetLineWidth(2)

    stack=ROOT.THStack("stack","stack")
    stack.Add(QCD)
    stack.Add(W)
    stack.Add(VV)
    stack.Add(DYS)
    stack.Add(SingleT)
    stack.Add(TT)

    errorBand = QCD.Clone()
    errorBand.Add(W)
    errorBand.Add(TT)
    errorBand.Add(VV)
    errorBand.Add(SingleT)
    errorBand.Add(DYS)
    errorBand.SetMarkerSize(0)
    errorBand.SetFillColor(16)
    errorBand.SetFillStyle(3001)
    errorBand.SetLineWidth(1)

    pad1 = ROOT.TPad("pad1","pad1",0,0.35,1,1)
    pad1.Draw()
    pad1.cd()
    pad1.SetFillColor(0)
    pad1.SetBorderMode(0)
    pad1.SetBorderSize(10)
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad1.SetLeftMargin(0.18)
    pad1.SetRightMargin(0.05)
    pad1.SetTopMargin(0.122)
    pad1.SetBottomMargin(0.026)
    pad1.SetFrameFillStyle(0)
    pad1.SetFrameLineStyle(0)
    pad1.SetFrameLineWidth(3)
    pad1.SetFrameBorderMode(0)
    pad1.SetFrameBorderSize(10)

    Data.GetXaxis().SetLabelSize(0)
    Data.SetMaximum(Data.GetMaximum()*2)
    Data.GetXaxis().SetRangeUser(0,MaxRange)
    Data.SetMinimum(0)
    Data.Draw("e")
    print "Full Data in ", FileName ," is ------>", Data.Integral()
    stack.Draw("histsame")
    print "Full Back ground in ", FileName ," is ------>", errorBand.Integral(), "\n\n\n"
    errorBand.Draw("e2same")
    Data.Draw("esame")
    Signal.Draw("lsame")

    legende=make_legend()
    legende.AddEntry(Data,"Observed","elp")
    legende.AddEntry(Signal,sigLeg,"elp")
    legende.AddEntry(TT,"t#bar{t}+jets","f")
    legende.AddEntry(SingleT,"SingleTop","f")
    legende.AddEntry(DYS,"DY #rightarrowll ","f")
    legende.AddEntry(VV,"VV","f")
    legende.AddEntry(W,"W","f")
    legende.AddEntry(QCD,"QCD multijet","f")
    legende.AddEntry(errorBand,"Uncertainty","f")

    legende.Draw()

    l1=add_lumi()
    l1.Draw("same")
    l2=add_CMS()
    l2.Draw("same")
    l3=add_Preliminary()
    l3.Draw("same")

    pad1.RedrawAxis()

    categ  = ROOT.TPaveText(0.21, 0.5+0.013, 0.43, 0.70+0.155, "NDC")
    categ.SetBorderSize(   0 )
    categ.SetFillStyle(    0 )
    categ.SetTextAlign(   12 )
    categ.SetTextSize ( 0.06 )
    categ.SetTextColor(    1 )
    categ.SetTextFont (   41 )
    #       if i==1 or i==3: 
    categ.AddText(HistName)
    #       else :
    #        categ.AddText("SS")
    categ.Draw()

    c.cd()
    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.35);
    pad2.SetTopMargin(0.05);
    pad2.SetBottomMargin(0.35);
    pad2.SetLeftMargin(0.18);
    pad2.SetRightMargin(0.05);
    pad2.SetTickx(1)
    pad2.SetTicky(1)
    pad2.SetFrameLineWidth(3)
    pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    
    h1=errorBand.Clone()
    h1.SetMaximum(2)
    h1.SetMinimum(0.1)
    h1.SetMarkerStyle(20)
    
    h3=Data.Clone()
    
    h3.Sumw2()
    h1.Sumw2()
    
    
    h1.SetStats(0)
    h3.SetStats(0)
    h1.SetTitle("")
    
    h1.Divide(errorBand)
    h3.Divide(errorBand)
    
    
    h1.GetXaxis().SetTitle(Xaxis)
    h1.GetXaxis().SetRangeUser(0,MaxRange)
    h1.GetXaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetTitle("Obs./Exp.")
    h1.GetXaxis().SetNdivisions(505)
    h1.GetYaxis().SetNdivisions(5)
    h1.GetXaxis().SetTitleSize(0.15)
    h1.GetYaxis().SetTitleSize(0.15)
    h1.GetYaxis().SetTitleOffset(0.56)
    h1.GetXaxis().SetTitleOffset(1.04)
    h1.GetXaxis().SetLabelSize(0.11)
    h1.GetYaxis().SetLabelSize(0.11)
    h1.GetXaxis().SetTitleFont(42)
    h1.GetYaxis().SetTitleFont(42)
    
    h1.Draw("e2")
    h3.Draw("epsame")

    c.cd()
    pad1.Draw()

    ROOT.gPad.RedrawAxis()

    c.Modified()
    c.SaveAs("_Fullplot_"+categoriy+".pdf")
    #       c.SaveAs("mvis"+categoriy+".png")

Category = ["_DiJet","_JetBJet"]

FileNamesInfo=[

               ["RHW_mt.inputs-sm-13TeV.root","MuTau_DiJet","ST_{l#taujjMET}  (GeV)","MuTau ",2000,"RHW_2000","RH W 2TeV (x 10)"],
               ["lq_mt.inputs-sm-13TeV.root","MuTau_JetBJet","ST_{l#taujjMET}  (GeV)","MuTau ",2000,"LQ_700","LQ 700 GeV (x 10)"],
               

               ["RHW_et.inputs-sm-13TeV.root","EleTau_DiJet","ST_{l#taujjMET}  (GeV)","EleTau ",2000,"RHW_2000","RH W 2TeV (x 10)"],
               ["lq_et.inputs-sm-13TeV.root","EleTau_JetBJet","ST_{l#taujjMET}  (GeV)","EleTau ",2000,"LQ_700","LQ 700 GeV (x 10)"],
               

               
               
               ]


#for ch in channelDirectory:
#    for cat in Category:
for i in range(0,len(FileNamesInfo)):

#    FileName="ztt_"+ch+"_shapes.root"
    MakePlot(FileNamesInfo[i][0],FileNamesInfo[i][1],FileNamesInfo[i][3],FileNamesInfo[i][2],FileNamesInfo[i][4],FileNamesInfo[i][5],FileNamesInfo[i][6])

