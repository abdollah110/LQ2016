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
    lumi.AddText("13 TeV")
    return lumi

def add_CMS():
    lowX=0.21
    lowY=0.70
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
    lowY=0.63
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(52)
    lumi.SetTextSize(0.03)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("Simulation")
    return lumi

def make_legend():
    output = ROOT.TLegend(0.45, 0.5, 0.92, 0.82, "", "brNDC")
    output.SetLineWidth(0)
    output.SetLineStyle(0)
    output.SetFillStyle(0)
    output.SetBorderSize(0)
    output.SetTextFont(62)
    return output


def MakePlot(FileName,categoriy,HistName,Xaxis,Info,RB_,channel):
    ROOT.gStyle.SetFrameLineWidth(3)
    ROOT.gStyle.SetLineWidth(3)
    ROOT.gStyle.SetOptStat(0)
    
    c=ROOT.TCanvas("canvas","",0,0,600,600)
#    c.cd()

    file=ROOT.TFile(FileName,"r")
    
#    adapt=ROOT.gROOT.GetColor(12)
#    new_idx=ROOT.gROOT.GetListOfColors().GetSize() + 1
    #    trans=ROOT.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(),adapt.GetBlue(), "",0.5)
    
    #    categories=["MuTau_DiJet","MuTau_JetBJet"]
    #    ncat=
    
    print "--->  ", FileName,categoriy,HistName
    Data=file.Get(categoriy).Get("qcd_obs")
    Data.Rebin(RB_)
    QCD=file.Get(categoriy).Get("QCD")
    QCD.Rebin(RB_)
    
    
    Data.GetXaxis().SetTitle("")
    Data.GetXaxis().SetRangeUser(0,200)
#    Data.GetXaxis().SetTitleSize(0)
#    Data.GetXaxis().SetNdivisions(505)
#    Data.GetYaxis().SetLabelFont(42)
#    Data.GetYaxis().SetLabelOffset(0.01)
#    Data.GetYaxis().SetLabelSize(0.06)
#    Data.GetYaxis().SetTitleSize(0.075)
#    Data.GetYaxis().SetTitleOffset(1.04)
    Data.SetTitle("")
    Data.GetYaxis().SetTitle("Events")
    
    
    
    QCD.SetFillColor(ROOT.TColor.GetColor(408, 106, 154))
    
    
    
    
    ######  Add OverFlow Bin
    QCD.SetBinContent(QCD.GetNbinsX(),QCD.GetBinContent(QCD.GetNbinsX()+1)+QCD.GetBinContent(QCD.GetNbinsX()))
    
    Data.SetBinContent(Data.GetNbinsX(),Data.GetBinContent(Data.GetNbinsX()+1)+Data.GetBinContent(Data.GetNbinsX()))
    
    Data.SetMarkerStyle(20)
    Data.SetMarkerSize(1)
    QCD.SetMarkerStyle(22)
    QCD.SetMarkerSize(1)

    Data.SetLineColor(ROOT.kBlack)
    Data.SetLineWidth(2)

    QCD.SetLineColor(ROOT.kRed)
    QCD.SetLineWidth(2)
    

#    stack=ROOT.THStack("stack","stack")
#    stack.Add(QCD)

    
#    errorBand = QCD.Clone()

#    errorBand.SetMarkerSize(0)
#    errorBand.SetFillColor(16)
#    errorBand.SetFillStyle(3001)
#    errorBand.SetLineWidth(1)

#    pad1 = ROOT.TPad("pad1","pad1",0,0.35,1,1)
#    pad1.Draw()
#    pad1.cd()
#    pad1.SetFillColor(0)
#    pad1.SetBorderMode(0)
#    pad1.SetBorderSize(10)
#    pad1.SetTickx(1)
#    pad1.SetTicky(1)
#    pad1.SetLeftMargin(0.18)
#    pad1.SetRightMargin(0.05)
#    pad1.SetTopMargin(0.122)
#    pad1.SetBottomMargin(0.026)
#    pad1.SetFrameFillStyle(0)
#    pad1.SetFrameLineStyle(0)
#    pad1.SetFrameLineWidth(3)
#    pad1.SetFrameBorderMode(0)
#    pad1.SetFrameBorderSize(10)

    
    Data.GetXaxis().SetTitle(Xaxis)
#    Data.GetXaxis().SetLabelSize(0.08)
#    Data.GetYaxis().SetLabelSize(0.08)
#    Data.GetYaxis().SetTitle("Obs./Exp.")
#    Data.GetXaxis().SetNdivisions(505)
#    Data.GetYaxis().SetNdivisions(5)
#    Data.GetXaxis().SetTitleSize(0.15)
#    Data.GetYaxis().SetTitleSize(0.15)
#    Data.GetYaxis().SetTitleOffset(0.56)
#    Data.GetXaxis().SetTitleOffset(1.04)
#    Data.GetXaxis().SetLabelSize(0.11)
#    Data.GetYaxis().SetLabelSize(0.11)
#    Data.GetXaxis().SetTitleFont(42)
#    Data.GetYaxis().SetTitleFont(42)

    
#    Data.GetXaxis().SetLabelSize(0)
    Data.SetMaximum(Data.GetMaximum()*2.5)
    Data.SetMinimum(0)
    Data.Draw("e")
    QCD.Draw("esame")
#    stack.Draw("esame")
#    errorBand.Draw("e2same")
#    Data.Draw("esame")

    legende=make_legend()
    legende.AddEntry(Data,"QCD ","elp")
    legende.AddEntry(QCD,"QCD estim. from fakerate","elp")
#    legende.AddEntry(errorBand,"Uncertainty","f")

    legende.Draw()
    
    l1=add_lumi()
    l1.Draw("same")
    l2=add_CMS()
    l2.Draw("same")
    l3=add_Preliminary()
    l3.Draw("same")
    
#    pad1.RedrawAxis()

    categ  = ROOT.TPaveText(0.21, 0.5+0.013, 0.43, 0.70+0.155, "NDC")
    categ.SetBorderSize(   0 )
    categ.SetFillStyle(    0 )
    categ.SetTextAlign(   12 )
    categ.SetTextSize ( 0.03 )
    categ.SetTextColor(    1 )
    categ.SetTextFont (   41 )
    #       if i==1 or i==3:
    categ.AddText(channel)
    #       else :
    #        categ.AddText("SS")
    categ.Draw()
    
#    c.cd()
#    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.35);
#    pad2.SetTopMargin(0.05);
#    pad2.SetBottomMargin(0.35);
#    pad2.SetLeftMargin(0.18);
#    pad2.SetRightMargin(0.05);
#    pad2.SetTickx(1)
#    pad2.SetTicky(1)
#    pad2.SetFrameLineWidth(3)
#    pad2.SetGridx()
#    pad2.SetGridy()
#    pad2.Draw()
#    pad2.cd()
#    
#    h1=errorBand.Clone()
#    h1.SetMaximum(2)
#    h1.SetMinimum(0.1)
#    h1.SetMarkerStyle(20)
#    
#    h3=Data.Clone()
#    
#    h3.Sumw2()
#    h1.Sumw2()
#    
#    
#    h1.SetStats(0)
#    h3.SetStats(0)
#    h1.SetTitle("")
#    
#    h1.Divide(errorBand)
#    h3.Divide(errorBand)
#    
#    
#    h1.GetXaxis().SetTitle(Xaxis)
#    h1.GetXaxis().SetLabelSize(0.08)
#    h1.GetYaxis().SetLabelSize(0.08)
#    h1.GetYaxis().SetTitle("Obs./Exp.")
#    h1.GetXaxis().SetNdivisions(505)
#    h1.GetYaxis().SetNdivisions(5)
#    h1.GetXaxis().SetTitleSize(0.15)
#    h1.GetYaxis().SetTitleSize(0.15)
#    h1.GetYaxis().SetTitleOffset(0.56)
#    h1.GetXaxis().SetTitleOffset(1.04)
#    h1.GetXaxis().SetLabelSize(0.11)
#    h1.GetYaxis().SetLabelSize(0.11)
#    h1.GetXaxis().SetTitleFont(42)
#    h1.GetYaxis().SetTitleFont(42)
#    
#    h1.Draw("e2")
#    h3.Draw("epsame")

#    c.cd()
#    pad1.Draw()

#    ROOT.gPad.RedrawAxis()
#
#    c.Modified()
    c.SaveAs("_plot"+HistName+"_"+categoriy+".pdf")
#       c.SaveAs("mvis"+categoriy+".png")


#channelDirectory = ["MuTau", "EleTau"]
channelDirectory = ["MuTau"]
#Category = ["_DiJet","_JetBJet"]
#Category = ["_NoBJet"]
Category = ["_inclusive"]


#PlotName= ["_tmass","_LepPt","_LepEta","_TauPt","_TauEta","_MET"]




FileNamesInfo=[
                              ["_tmass","M_{T}(lep,MET) (GeV)","",20],
#                              ["_VisMass","M_{l#tau} (GeV)","",20],
                              ["_LepPt","lep PT (GeV)","",20],
                              ["_LepEta","lep #eta ","",10],
                              ["_TauPt","#tau PT (GeV)","",20],
                              ["_TauEta","#tau #eta ","",10],
#                              ["_NumJet","Jet multiplicity","",1],
#                              ["_NumBJet","B Jet multiplicity","",1],
               ##               ["_nVtx","# of vertex","",1],
               ##               ["_nVtx_NoPU","# of vertex before PU reweighting","",1],
                              ["_MET","MET  (GeV)","",20],
               #               ["_M_taujet","M_{#tauj}   (GeV)","",40],
               #               ["_LeadJetPt","Leading Jet PT  (GeV)","",20],
               #               ["_SubLeadJetPt","subLeading Jet PT  (GeV)","",20],
               #               ["_ST_DiJet","ST_{l#taujj}  (GeV) ","",10],
               #               ["_ST_MET","ST_{l#taujjMET}  (GeV)","",10],
               
               
               ]
#TotalRootForLimit_MuTau_tmass_LowMT_OS_TauIsoLepAntiIso.root
#TotalRootForLimit_MuTau_MET_OS_TauIso.root

for ch in channelDirectory:
    for cat in Category:
        for i in range(0,len(FileNamesInfo)):
            
            FileName="TotalRootForLimit_"+ch+FileNamesInfo[i][0]+"_OS_TauIso.root"
            MakePlot(FileName,ch+cat,FileNamesInfo[i][0],FileNamesInfo[i][1],FileNamesInfo[i][2],FileNamesInfo[i][3],ch+cat)

