To compuet the limit here are the procedure:

1) Run the code in the /Users/abdollah1/GIT_abdollah110/LQ2016/RecoAnalysis to get the two following root files (one for mutau and the oter for eletau)
scp TotalRootForLimit_MuTau_ST_JetBJetFinal_NoMT_OS.root abdollah@cmslpc27:/uscms_data/d3/abdollah/Analysis/Limit/CMSSW_7_1_5/src/auxiliaries/shapes/lq_mt.inputs-sm-13TeV.root
scp TotalRootForLimit_EleTau_ST_JetBJetFinal_NoMT_OS.root  abdollah@cmslpc27:/uscms_data/d3/abdollah/Analysis/Limit/CMSSW_7_1_5/src/auxiliaries/shapes/lq_et.inputs-sm-13TeV.root

scp TotalRootForLimit_MuTau_ST_JetBJetFinal_NoMT_OS.root abdollah@cmslpc27:/uscms_data/d3/abdollah/Analysis/Limit/CMSSW_7_1_5/src/auxiliaries/shapes/RHW_mt.inputs-sm-13TeV.root
scp TotalRootForLimit_EleTau_ST_JetBJetFinal_NoMT_OS.root  abdollah@cmslpc27:/uscms_data/d3/abdollah/Analysis/Limit/CMSSW_7_1_5/src/auxiliaries/shapes/RHW_et.inputs-sm-13TeV.root


2) Update the ExampleLQFull.cpp code with systematics and channels ....

3) scram b

4) ExampleLQ    ../../../../bin/slc6_amd64_gcc481/ExampleRHW

5) cd output/lq6_cards/

6)
python ../../../../../HiggsAnalysis/HiggsToTauTau/scripts/limit.py --asymptotic LIMITS/*
python ../../../scripts/combineTool.py -M CollectLimits -i */*/higgsCo* -o rhw.json
python ../../../scripts/plotBSMxsBRLimit_RHW.py --file=rhw.json

get the postfir plots: Mine
limit.py --max-likelihood --stable --rMin -5 --rMax 5 outputLQ/lq3_cards_ST_MET_HighPtLep50/LIMITS/1000
PostFitShapes -d outputLQ/lq3_cards_ST_MET_HighPtLep50/LIMITS/1000/lq_mt_1_13TeV.txt -o lq_mt.inputs-sm-13TeV.root -m 1000 -f mlfit.root:fit_s --postfit --sampling --print



from cecile:
[13/04/16 10:57:24] Cécile Caillol: I use combine directly, and not limit.py anymore
[13/04/16 10:57:57] Cécile Caillol: text2workspace.py mydatacard.txt
combine -M MaxLikelihoodFit mydatacard.root --robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --cminFallbackAlgo \"Minuit2,0:1.\"  --rMin 0.5 --rMax 1.5
PostFitShapesFromWorkspace -o ztt_mt_shapes.root -m 125 -f mlfit.root:fit_s --postfit --sampling --print -d mydatacard.txt -w mydatacard.root
python HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit.root -A -a --stol 0.99 --stol 0.99 --vtol 99. --vtol2 99. -f text mlfit.root > mlfit.txt
[13/04/16 10:58:03] Cécile Caillol: this is what I do
[13/04/16 10:58:24] Cécile Caillol: PostFitShapesFromWorkspace scales the signal by the signal strength




step1:   limit.py --max-likelihood --stable --rMin -5 --rMax 5 outputLQ/lq9_FinalPreTalk//LIMITS/700/
=combineCards.py -S lq_et_1_13TeV=lq_et_1_13TeV.txt lq_mt_1_13TeV=lq_mt_1_13TeV.txt
=text2workspace.py -b /tmp/tmpWWHo59 -o ./tmp.root -m 700 --default-morphing shape2
=combine -M MaxLikelihoodFit -m 700  --robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.01 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.001 --cminFallbackAlgo "Minuit,0:0.001" --keepFailures --rMin -5 --rMax 5   --saveNormalizations --saveShapes --saveWithUncertainties  ./tmp.root --out=out


ste2:cd outputLQ/lq9_FinalPreTalk/LIMITS/700/out

step 3:  PostFitShapes -o final_lq_mt_700.root -m 700 -f mlfit.root:fit_s --postfit --sampling --print -d ../lq_mt_1_13TeV.txt

