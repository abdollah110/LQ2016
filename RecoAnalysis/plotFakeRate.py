import math
import ROOT
from ROOT import TCanvas
from ROOT import TFile
from ROOT import TH1F
from ROOT import TGraph
from ROOT import gROOT
from ROOT import gStyle
from ROOT import gSystem
from ROOT import TGraphErrors
import array




Binning_PT = array.array("d",[0,20,30,40,50,60,70,80,90,100,120,150,200,300,400])
OutFile=TFile("OutFiles_WEstim/Data.root")

HistoNum=OutFile.Get("MuTau_TauPt_LowMT_SS_TauIsoLepAntiIso_inclusive")
HistoNum= HistoNum.Rebin(len(Binning_PT)-1,"",Binning_PT)

HistoDeNum=OutFile.Get("MuTau_TauPt_LowMT_SS_LepAntiIso_inclusive")
HistoDeNum= HistoDeNum.Rebin(len(Binning_PT)-1,"",Binning_PT)

fakeRate=ROOT.TGraphAsymmErrors(HistoNum, HistoDeNum, "")

canv = TCanvas("canv", "histograms", 0, 0, 600, 600)
canv.SetLogy()
fakeRate.SetMinimum(0.001)
fakeRate.SetMaximum(1)
fakeRate.GetXaxis().SetRangeUser(0,400)
fakeRate.GetXaxis().SetTitle("#tau p_{T} [GeV]")
fakeRate.GetYaxis().SetRangeUser(0.01,0.1)
fakeRate.SetTitle('Jet to Tau Fake Rate')
fakeRate.SetMarkerStyle(20)


fakeRate.Draw()

canv.SaveAs("jetToTauFR.pdf")
