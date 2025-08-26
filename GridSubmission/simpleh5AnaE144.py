### simple script to analyze the h5 files

import h5py
import glob
import sys
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pickle


# write list to binary file
def write_list(a_list, names):
    # store list in binary file so 'wb' mode
    with open(names, 'wb') as f:
       pickle.dump(a_list, f)

# Read list to memory
def read_list(names):
    # for reading also binary mode is important
    with open(names, 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list


def main():
    infoDict = {    "0.32": {"suf": "_xF1B_Eachh5Weightedto1BX_1mmEBeamLength", "wt": 5e-7, "circular":[201,300],"linear":[1001,1400]},
                    "0.4": {"suf": "_xF1B_Eachh5Weightedto1BX_1mmEBeamLength", "wt": 5e-7, "circular":[1,100],"linear":[101,200]},
                    "0.35": {"suf": "_xF1B_Eachh5Weightedto1BX_1mmEBeamLength", "wt": 5e-7, "circular":[401,500],"linear":[601,1000]}
                }

    weightedSignal      = []
    weightedSignalError = []
    a0List              = []
    polari              = sys.argv[1]

    
    for a0 in infoDict:
        fIns = []
        errorFile = 0
        print("a0 ------- ", a0, " ---- ")


        for i in range(infoDict[a0][polari][0], infoDict[a0][polari][1]+1):
            fIns.append("/storage/agrp/arkas/E144WorkArea_a0_"+a0+infoDict[a0]["suf"]+"/run_"+str(i)+"/E144_profile_Iteration"+str(i)+"_particles.h5")

        # print(fIns)
        photonList      = []
        positronList    = []
        positronWeight  = []
        electronList    = []
        
        for name in fIns:
            try:
                fIn             = h5py.File(name, 'r')
                id_photon       = fIn['final-state/photon']['id'][()]
                id_electron     = fIn['final-state/electron']['id'][()]
                id_positron     = fIn['final-state/positron']['id'][()]
                weight_positron = fIn['final-state/positron']['weight'][()]
                photonList.append(len(id_photon))
                positronList.append(len(id_positron))
                electronList.append(len(id_electron))
                if len(id_positron) > 0:
                    positronWeight.append(weight_positron)
            except: 
                print("Error reading file: ", name)
                errorFile += 1
                continue

        posit   = 0
        elect   = 0
        phot    = 0
        wtPosit = 0
        for i in positronList:
            posit += i
        for j in electronList:
            elect += j
        for k in photonList:
            phot  += k
        for w in positronWeight:
            for x in w:
                wtPosit += x

        print("Polarization: ", polari)
        print("Total positron: ", posit, " electron: ", elect, " photon: ", phot)
        print("Total files: positron ", len(positronList), " electron: ", len(electronList), " photon: ", len(photonList))
        print("Total error files: ", errorFile)
        # print("Positron weights: ", positronWeight)

        ## constant factor
        # weightedPositron = posit*infoDict[a0]["wt"]/float(len(positronList))
        ## variable factor
        weightedPositron = wtPosit/float(len(positronList))
        print("Weighted Positron: ", weightedPositron)
        a0List.append(float(a0))
        weightedSignal.append(weightedPositron)
        weightedSignalError.append(0.0)

    '''
    fig, ax0 = plt.subplots()
    ax0.errorbar(a0List, weightedSignal, yerr=weightedSignalError, fmt='-o')



    ax0.set_yscale('log')
    ax0.set(xlabel='a0', ylabel='Positrons/BX',
           title='E320 signal multiplicity')
    ax0.grid()

    fig.savefig("E320_PositronMultiplicity_Weighted.png")
    fig.savefig("E320_PositronMultiplicity_Weighted.pdf")
    # plt.show()
    '''
    write_list(a0List, "a0List_E144.pkl")
    write_list(weightedSignal, "weightedSignal_E144.pkl")


if __name__=="__main__":
    main()
