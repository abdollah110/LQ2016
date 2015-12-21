cd /afs/cern.ch/work/a/abdollah/scratch1/2015NtupleProduction/ggNtuple/CMSSW_7_4_1/src/ggAnalysis/ggNtuplizer/DoSkim
eval `scram runtime -sh`
xrdcp  root://eoscms.cern.ch//eos/cms/store/group/phys_smp/ggNtuples/13TeV/mc/job_spring15_DYJetsToLL_m50_25ns.root /tmp/job_spring15_DYJetsToLL_m50_25ns.root

./Skimmer /tmp/  job_spring15_DYJetsToLL_m50_25ns.root   5


