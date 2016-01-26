#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.
#http://root.cern.ch/viewvc/trunk/tutorials/pyroot/hsimple.py?revision=20881&view=markup
__author__ = "abdollahmohammadi"
__date__ = "$Feb 23, 2013 10:39:33 PM$"

import os

InputFileLocation = '../ROOT/NewTot2/'
OutPutFileLocation = 'OutFiles/'
Sample = os.popen(("ls " + InputFileLocation + " | sort "))
OutFile = open("RunFullSamples.txt", 'w')
firstCommand = "./Make.sh TreeReader.cc\n"
firstCommand += "rm OutFiles/*.root \n"
firstCommand += "mv *.root *.pdf  OLD/\n"
OutFile.write(firstCommand)
outCommand = ""
for files in Sample.readlines():
    outCommand = outCommand + "./TreeReader.exe  " + OutPutFileLocation + "out_" + files.replace('\n','') + " " + InputFileLocation + files


OutFile.write(outCommand)
    