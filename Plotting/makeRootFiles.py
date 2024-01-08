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
    parser.add_argument('-v', action="store", dest="version", type=str, default="1")
    parser.add_argument('-n', action="store", dest="inelec", type=float, default=125000.0)
    args = parser.parse_args()

    # outRootFileName = "raw_lightbylight_xi"+str(args.xi)+"_gamma"+str(args.gamma)+"_histograms.root"
    # inRootFileName  = "raw_lightbylight_xi"+str(args.xi)+"_gamma"+str(args.gamma)+".root"
    outRootFileName = "raw_e320_xi"+str(args.xi)+"_gamma"+str(args.gamma)+"_v"+args.version+"_histograms.root"
    inRootFileName  = "raw_e320_xi"+str(args.xi)+"_gamma"+str(args.gamma)+"_v"+args.version+".root"
    inRootFile      = TFile("rootFiles/"+inRootFileName, "READ")
    treeName        = inRootFile.Get("tt")

    print("Input file: ", "rootFiles/"+inRootFileName)
    print("Output file: ", "outputDirectory/"+outRootFileName)
    
    inElectronEnergy = 0.0

    if args.gamma=="0p7":
        inElectronEnergy = 700.0
    elif args.gamma=="0p35":
        inElectronEnergy = 350.0
    elif args.gamma=="3p7":
        inElectronEnergy = 3700.0
    elif args.gamma=="7p0":
        inElectronEnergy = 7000.0
    elif args.gamma=="10":
        inElectronEnergy = 10000.0
    else:
        pass

    print("Electron energy: ", inElectronEnergy)

    outRootFile     = TFile("outputDirectory/"+outRootFileName, "RECREATE")
    outRootFile.cd()

    hEnergy_Electron        = TH1F("hEnergy_Electron", "hEnergy_Electron; E [MeV]; Entries/primary electron", 1100, 0, 11000)
    hEnergy_Electron_In     = TH1F("hEnergy_Electron_In", "hEnergy_Electron_In; E [MeV]; Entries/primary electron", 100, 9900, 10100)
    hPhi_Electron           = TH1F("hPhi_Electron", "hPhi_Electron; #phi [rad]; Entries/primary electron", 64, -3.2, 3.2)
    hTheta_Electron         = TH1F("hTheta_Electron", "hTheta_Electron; #theta [rad]; Entries/primary electron", 320, 0, 3.2)
    hEnergyVsTheta_Electron = TH2D("hEnergyVsTheta_Electron", "hEnergyVsTheta_Electron; #theta [rad]; E [MeV]", 320, 0, 3.2, 1100, 0, 11000)

    hEnergy_Photon          = TH1F("hEnergy_Photon", "hEnergy_Photon; E [MeV]; Entries/primary electron", 1100, 0, 11000)
    hPhi_Photon             = TH1F("hPhi_Photon", "hPhi_Photon; #phi [rad]; Entries/primary electron", 64, -3.2, 3.2)
    hTheta_Photon           = TH1F("hTheta_Photon", "hTheta_Photon; #theta [rad]; Entries/primary electron", 320, 0, 3.2)
    hEnergyVsTheta_Photon   = TH2D("hEnergyVsTheta_Photon", "hEnergyVsTheta_Photon; #theta [rad]; E [MeV]", 320, 0, 3.2, 1100, 0, 11000)


    hEnergy_Positron        = TH1F("hEnergy_Positron", "hEnergy_Positron; E [MeV]; Entries/primary electron", 1100, 0, 11000)
    hPhi_Positron           = TH1F("hPhi_Positron", "hPhi_Positron; #phi [rad]; Entries/primary electron", 64, -3.2, 3.2)
    hTheta_Positron         = TH1F("hTheta_Positron", "hTheta_Positron; #theta [rad]; Entries/primary electron", 320, 0, 3.2)
    hEnergyVsTheta_Positron = TH2D("hEnergyVsTheta_Positron", "hEnergyVsTheta_Positron; #theta [rad]; E [MeV]", 320, 0, 3.2, 1100, 0, 11000)

    counter = 0
    for event in treeName:
        print("In the loop")
        for ientries, energy in enumerate(event.E):
            counter += 1
            if counter%10000==0:
                print("Processed: ",counter)

            if event.pdgId[ientries] == 11:
                hEnergy_Electron.Fill(energy, event.wgt[ientries])
                hEnergy_Electron_In.Fill(inElectronEnergy, event.wgt[ientries])
                hPhi_Electron.Fill(event.phi[ientries], event.wgt[ientries])
                hTheta_Electron.Fill(event.theta[ientries], event.wgt[ientries])
                hEnergyVsTheta_Electron.Fill(event.theta[ientries], energy, event.wgt[ientries])

            if event.pdgId[ientries] == 22:
                hEnergy_Photon.Fill(energy, event.wgt[ientries])
                hPhi_Photon.Fill(event.phi[ientries], event.wgt[ientries])
                hTheta_Photon.Fill(event.theta[ientries], event.wgt[ientries])
                hEnergyVsTheta_Photon.Fill(event.theta[ientries], energy, event.wgt[ientries])

            if event.pdgId[ientries] == -11:
                hEnergy_Positron.Fill(energy, event.wgt[ientries])
                hPhi_Positron.Fill(event.phi[ientries], event.wgt[ientries])
                hTheta_Positron.Fill(event.theta[ientries], event.wgt[ientries])
                hEnergyVsTheta_Positron.Fill(event.theta[ientries], energy, event.wgt[ientries])
    
    #### normalized to the number of input electrons
    hEnergy_Electron.Scale(1./args.inelec)
    hEnergy_Electron_In.Scale(1./args.inelec)
    hPhi_Electron.Scale(1./args.inelec)
    hTheta_Electron.Scale(1./args.inelec)
    hEnergyVsTheta_Electron.Scale(1./args.inelec)

    hEnergy_Photon.Scale(1./args.inelec)
    hPhi_Photon.Scale(1./args.inelec)
    hTheta_Photon.Scale(1./args.inelec)
    hEnergyVsTheta_Photon.Scale(1./args.inelec)

    hEnergy_Positron.Scale(1./args.inelec)
    hPhi_Positron.Scale(1./args.inelec)
    hTheta_Positron.Scale(1./args.inelec)
    hEnergyVsTheta_Positron.Scale(1./args.inelec)


    ##### prepare the plots

    outRootFile.Write()
    outRootFile.Close()

if __name__=="__main__":
    main()