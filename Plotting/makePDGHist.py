import os, sys
import argparse
from ROOT import TH1F, TFile
from copy import copy, deepcopy
sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *
import pprint

def main():
    parser = argparse.ArgumentParser(description='Code to get plots from Allpix-squared hit branches text file')
    parser.add_argument('-i', action="store", dest="inFile", type=str, default="signalMC_E320lp_10.0_HitBranchesForAllPix_BX1to72.txt")
    args = parser.parse_args()

    inputDirectory = "/Volumes/Study/Weizmann_PostDoc/AllPix2Study/InputFiles/HitBranchesTxtFiles"

    inFileName = inputDirectory+"/"+args.inFile

    outRootFileName = "E320_PDG_histograms_BX1to72_Bkg.root"

    print("Output file: ", "outputDirectory/"+outRootFileName)
    outRootFile     = TFile("outputDirectory/"+outRootFileName, "RECREATE")
    outRootFile.cd()

    hPDG        = TH1F("hPDG", "hPDG; PDG; Entries/per bin", 2250, -25, 2225)

    counter = 0
    with open(inFileName) as readInFile:
        for lines in readInFile.readlines():
            counter += 1
            if(counter%10000==0): print("Processed: ", counter)
            if "#" in lines: continue
            allWords = lines.rstrip().split()
            pdg = int(allWords[7])
            if (pdg > 30): 
                # if(pdg!=1000140280 or pdg!=1000140290): print("pdg: ", pdg)
                # print("extreme pdg: ", pdg)
                if(pdg==1000140280): pdg = 100
                if(pdg==1000140290): pdg = 101
                if(pdg==1000140300): pdg = 102
            hPDG.Fill(pdg)

    ##### prepare the plots

    outRootFile.Write()
    outRootFile.Close()

if __name__=="__main__":
    main()