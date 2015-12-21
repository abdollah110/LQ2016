
import os
import shutil

TextSamples = open("textSamples.txt", "r")
location=os.getcwd()
RootLoc="root://eoscms.cern.ch//eos/cms/store/group/phys_smp/ggNtuples/13TeV/"

name_submitFile = "GrandSubmit_" + ".sh"
submit_File = open(name_submitFile, 'w')
hadd_File=open("do_hadd.sh",'w')

for sample in TextSamples.readlines():
    if sample[0:-1].split(",")[0]=="#": continue
    for number in range(10):
        print "name=",sample
        dir=sample[0:-1].split(",")[0]
        name=sample[0:-1].split(",")[1]
        nameNotRoot=name.replace(".root","")
        fineName="_filetoSubmit"+nameNotRoot+"_"+str(number)+".sh"
        fileToSubmit=open(fineName, 'w')
        commandLine = ""
        commandLine += "cd " + location + "\n" + "\n"
        commandLine += "eval `scram runtime -sh`" + "\n"
        commandLine += "./Skimmer " + RootLoc+dir + " " + name + " " + str(number) + "\n"
        fileToSubmit.write(commandLine)

        newComLine=""
        newComLine += "bsub  -q 8nh -J " +name+str(number) + " < " + fineName + "\n"
        
        lineHadd =  ""
        lineHadd += "hadd -f  tot_" + name + "\tskimed_*_" +name + "\n"

        fileToSubmit.close()
        submit_File.write(newComLine)
    hadd_File.write(lineHadd)
hadd_File.close()
submit_File.close()
