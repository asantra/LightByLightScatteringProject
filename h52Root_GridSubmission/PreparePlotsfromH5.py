import os, sys
import math, time
import h5py
from array import array
import numpy as np
import ROOT
from ROOT import TFile, TTree, TLorentzVector
import glob
# import subprocess
import argparse
import matplotlib.pyplot as plt



meMeV = 0.5109989461 ## MeV
meGeV = meMeV/1000.
MeV2GeV = 1./1000.

def main():
    needPhoton   = False
    needElectron = False
    needPositron = True
    parser = argparse.ArgumentParser(description='Code to get root files from h5')
    parser.add_argument('-x', action="store", dest="xi", type=str, default="10.0")
    parser.add_argument('-g', action="store", dest="gamma", type=str, default="10.0")
    parser.add_argument('-v', action="store", dest="version", type=str, default="1")
    parser.add_argument('-i', action="store", dest="iteration", type=str, default="1")
    args         = parser.parse_args()
    xiInput      = args.xi
    gammaInput   = args.gamma
    ver          = args.version
    iter         = args.iteration
    ### for grid files
    # inputDir  = "/storage/agrp/arkas/E320WorkArea_a0_10.0_positronpairrate_xF1M/"
    # storage   = "/storage/agrp/arkas/h5AnalyzerPlots/"
    # fIns = glob.glob(inputDir+"run_*/E320_profile_Iteration*_particles.h5")

    inputDir  = "/storage/agrp/arkas/E320Files/ForGeant4Processing/Onlyh5Files/"
    storage   = "/storage/agrp/arkas/h5AnalyzerPlots_Unweighted/"
    fIns = glob.glob(inputDir+"E320_profile_Iteration*_particles.h5")

    

    print("The input h5 file: ",fIns)   
    ##### work only on the events having same order of tracks as that of the highest tracked event
   
    vx0_List = []
    vy0_List = []
    vz0_List = []
    weight_List = []

    positronNumber = 0
    for name in fIns:
        #### input file
        fIn = h5py.File(name, 'r')
        print("reading: ",name)
                
        if(needPositron):
            ### positrons are only collected for g+laser
            id_value_positron       = fIn['final-state/positron']['id'][()]
            print("this file has ",len(id_value_positron)," positrons")
            parentid_value_positron = fIn['final-state/positron']['parent_id'][()]
            momentum_value_positron = fIn['final-state/positron']['momentum'][()]
            position_value_positron = fIn['final-state/positron']['position'][()]
            weight_value_positron   = fIn['final-state/positron']['weight'][()]
            a0_out_                 = fIn['final-state/positron']['a0_at_creation'][()]

            for j in range(0, len(id_value_positron)):
                if(positronNumber%10==0): print("processed: ", positronNumber," positrons")
                
                vx0    = position_value_positron[j][0]*1.e3 ## m to mm
                vy0    = position_value_positron[j][1]*1.e3 ## m to mm
                vz0    = position_value_positron[j][2]*1.e3 ## m to mm
                weight = weight_value_positron[j]

                vx0_List.append(vx0)
                vy0_List.append(vy0)
                vz0_List.append(vz0)
                weight_List.append(weight)

                t0     = position_value_positron[j][3]
                Energy = momentum_value_positron[j][0]*1.e-3 ## MeV to GeV
                px0    = momentum_value_positron[j][1]*1.e-3 ## MeV to GeV
                py0    = momentum_value_positron[j][2]*1.e-3 ## MeV to GeV
                pz0    = momentum_value_positron[j][3]*1.e-3 ## MeV to GeV
                positronNumber += 1


    vx0_np = np.array(vx0_List)
    vy0_np = np.array(vy0_List)
    vz0_np = np.array(vz0_List)

    # Compute weighted mean and weighted standard deviation
    meanx       = np.average(vx0_np, weights=weight_List)
    variancex   = np.average((vx0_np - meanx)**2, weights=weight_List)
    sigmax      = np.sqrt(variancex)

    meany       = np.average(vy0_np, weights=weight_List)
    variancey   = np.average((vy0_np - meany)**2, weights=weight_List)
    sigmay      = np.sqrt(variancey)

    meanz       = np.average(vz0_np, weights=weight_List)
    variancez   = np.average((vz0_np - meanz)**2, weights=weight_List)
    sigmaz      = np.sqrt(variancez)

    


    fig, ax = plt.subplots()
    nbins=200
    ax.hist(vx0_List, bins=nbins, weights=weight_List, histtype='step', color='blue', label='vx0')
    ax.set_ylabel('Number per bin')
    ax.set_xlabel('vx0 (mm)')
    ax.set_title('vx0 distribution')
    textstr = f"Mean = {meanx:.7f}\nSigma = {sigmax:.7f}"
    plt.text(0.95, 0.95, textstr, transform=plt.gca().transAxes,
    fontsize=12, verticalalignment='top', horizontalalignment='right',
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    fig.savefig(storage+"vx0_distribution.png")

    fig, ax = plt.subplots()
    nbins=200
    ax.hist(vy0_List, bins=nbins, weights=weight_List, histtype='step', color='blue', label='vy0')
    ax.set_ylabel('Number per bin')
    ax.set_xlabel('vy0 (mm)')
    ax.set_title('vy0 distribution')
    textstr = f"Mean = {meany:.7f}\nSigma = {sigmay:.7f}"
    plt.text(0.95, 0.95, textstr, transform=plt.gca().transAxes,
    fontsize=12, verticalalignment='top', horizontalalignment='right',
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    fig.savefig(storage+"vy0_distribution.png")

    fig, ax = plt.subplots()
    nbins=200
    ax.hist(vz0_List, bins=nbins, weights=weight_List, histtype='step', color='blue', label='vz0')
    ax.set_ylabel('Number per bin')
    ax.set_xlabel('vz0 (mm)')
    ax.set_title('vz0 distribution')
    textstr = f"Mean = {meanz:.7f}\nSigma = {sigmaz:.7f}"
    plt.text(0.95, 0.95, textstr, transform=plt.gca().transAxes,
    fontsize=12, verticalalignment='top', horizontalalignment='right',
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    fig.savefig(storage+"vz0_distribution.png")
            


if __name__=="__main__":
    intime = time.time()
    main()
    print("----- the time taken ", time.time() - intime, " s")
