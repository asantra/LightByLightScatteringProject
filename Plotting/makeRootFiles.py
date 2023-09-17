import os, sys
import argparse
from ROOT import *
from copy import copy, deepcopy
sys.path.insert(0, '/Users/arkasantra/arka/include')
from Functions import *
import pprint

def main():
    parser = argparse.ArgumentParser(description='Code to get plots from the root files coming from h5')
    parser.add_argument('-x', action="store", dest="xi", type=str, default="3")
    parser.add_argument('-g', action="store", dest="gamma", type=str, default="0p7")
    args = parser.parse_args()

    outRootFileName = "raw_lightbylight_xi"+str(args.xi)+"_gamma"+str(args.gamma)+"_histograms.root"
    inRootFileName  = "raw_lightbylight_xi"+str(args.xi)+"_gamma"+str(args.gamma)+".root"
    inRootFile      = TFile("rootFiles/"+inRootFileName, "READ")
    treeName        = inRootFile.Get("tt")

    print("Input file: ", "rootFiles/"+inRootFileName)
    print("Output file: ", "outputDirectory/"+outRootFileName)
    
    inElectronEnergy = 0.0

    if args.gamma=="0p7":
        inElectronEnergy = 700.0
    elif args.gamma=="0p35":
        inElectronEnergy = 350.0
    else:
        pass

    print("Electron energy: ", inElectronEnergy)

    outRootFile     = TFile("outputDirectory/"+outRootFileName, "RECREATE")
    outRootFile.cd()

    hEnergy_Electron        = TH1F("hEnergy_Electron", "hEnergy_Electron; E [GeV]; Events/primary electron", 300, 0, 900)
    hEnergy_Electron_In     = TH1F("hEnergy_Electron_In", "hEnergy_Electron_In; E [GeV]; Events/primary electron", 300, 0, 900)
    hPhi_Electron           = TH1F("hPhi_Electron", "hPhi_Electron; #phi [rad]; Events/primary electron", 64, -3.2, 3.2)
    hTheta_Electron         = TH1F("hTheta_Electron", "hTheta_Electron; #theta [rad]; Events/primary electron", 70, 0, 0.35)
    hEnergyVsTheta_Electron = TH2D("hEnergyVsTheta_Electron", "hEnergyVsTheta_Electron; #theta [rad]; E [GeV]", 70, 0, 0.35, 300, 0, 900)

    hEnergy_Photon          = TH1F("hEnergy_Photon", "hEnergy_Photon; E [GeV]; Events/primary electron", 125, 0, 500)
    hPhi_Photon             = TH1F("hPhi_Photon", "hPhi_Photon; #phi [rad]; Events/primary electron", 64, -3.2, 3.2)
    hTheta_Photon           = TH1F("hTheta_Photon", "hTheta_Photon; #theta [rad]; Events/primary electron", 70, 0, 0.35)
    hEnergyVsTheta_Photon   = TH2D("hEnergyVsTheta_Photon", "hEnergyVsTheta_Photon; #theta [rad]; E [GeV]", 35, 0, 0.35, 125, 0, 500)

    counter = 0
    for event in treeName:
        print("In the loop")
        for ientries, energy in enumerate(event.E):
            counter += 1
            if counter%10000==0:
                print("Processed: ",counter)

            if event.pdgId[ientries] == 11:
                hEnergy_Electron.Fill(energy)
                hEnergy_Electron_In.Fill(inElectronEnergy)
                hPhi_Electron.Fill(event.phi[ientries])
                hTheta_Electron.Fill(event.theta[ientries])
                hEnergyVsTheta_Electron.Fill(event.theta[ientries], energy)

            if event.pdgId[ientries] == 22:
                hEnergy_Photon.Fill(energy)
                hPhi_Photon.Fill(event.phi[ientries])
                hTheta_Photon.Fill(event.theta[ientries])
                hEnergyVsTheta_Photon.Fill(event.theta[ientries], energy)
    
    #### normalized to the number of input electrons
    hEnergy_Electron.Scale(1./100000.)
    hEnergy_Electron_In.Scale(1./100000.)
    hPhi_Electron.Scale(1./100000.)
    hTheta_Electron.Scale(1./100000.)
    hEnergyVsTheta_Electron.Scale(1./100000.)

    hEnergy_Photon.Scale(1./100000.)
    hPhi_Photon.Scale(1./100000.)
    hTheta_Photon.Scale(1./100000.)
    hEnergyVsTheta_Photon.Scale(1./100000.)


    ##### prepare the plots

    outRootFile.Write()
    outRootFile.Close()

if __name__=="__main__":
    main()