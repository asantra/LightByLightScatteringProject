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
    # infoDict = {  "0.2": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_0p2"},
    #               "0.5": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_0p5"},
    #               "0.8": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_0p8"},
    #               "1.0": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_1p0"},
    #               "2.0": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_2p0"},
    #               "3.0": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_3p0"},
    #               "4.0": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_4p0"},
    #               "5.0": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_5p0"},
    #               "6.0": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_6p0"},
    #               "7.0": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_7p0"},
    #               "8.0": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_8p0"},
    #               "9.0": {"suf": "_xF1B", "wt": 5e-7, "name":"a0_9p0"},
    #               "10.0":{"suf": "_xF1B", "wt": 5e-7, "name":"a0_10p0"},
    #               }

    infoDict = {    "0.35": {"suf": "_xF1B_Eachh5Weightedto1BX", "wt": 5e-7, "circular":[201,300],"linear":[601,1000]},
                    "0.32": {"suf": "_xF1B_Eachh5Weightedto1BX", "wt": 5e-7, "circular":[201,300],"linear":[1001,1400]},
                    "0.4": {"suf": "_xF1B_Eachh5Weightedto1BX", "wt": 5e-7, "circular":[1,100],"linear":[101,200]}
                #   "0.8": {"suf": "_xF1_Eachh5Weightedto1BX", "wt": 5e-7},
                #   "1.0": {"suf": "_xF1_Eachh5Weightedto1BX", "wt": 5e-7}
                }

    weightedSignal      = []
    weightedSignalError = []
    a0List              = []
    polari              = sys.argv[1]





    for a0 in infoDict:
        if float(a0) > 1.0: continue
        print("a0 ------- ", a0, " ---- ")

        fIns = glob.glob("/storage/agrp/arkas/E320_h5Files_Lowa0_xF10T_4xmoreprimaryelectrons/"+infoDict[a0]["name"]+"/*.h5")

        photonList      = []
        positronList    = []
        positronWeight  = []
        electronList    = []

        for name in fIns:
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

        print("photons list: ", photonList)
        print("electrons list: ", electronList)
        print("positrons list: ", positronList)
        print("positrons weight list: ", positronWeight)

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


        print("Total positron: ", posit, " electron: ", elect, " photon: ", phot)
        print("Total files: positron ", len(positronList), " electron: ", len(electronList), " photon: ", len(photonList))
    #     # print("Positron weights: ", positronWeight)

    #     ## constant factor
    #     # weightedPositron = posit*infoDict[a0]["wt"]/float(len(positronList))
    #     ## variable factor
    #     weightedPositron = wtPosit/float(len(positronList))
    #     a0List.append(float(a0))
    #     weightedSignal.append(weightedPositron)
    #     weightedSignalError.append(0.0)

    # fig, ax0 = plt.subplots()
    # ax0.errorbar(a0List, weightedSignal, yerr=weightedSignalError, fmt='-o')



    # ax0.set_yscale('log')
    # ax0.set(xlabel='a0', ylabel='Positrons/BX',
    #        title='E320 signal multiplicity')
    # ax0.grid()

    # fig.savefig("E320_PositronMultiplicity_Weighted.png")
    # fig.savefig("E320_PositronMultiplicity_Weighted.pdf")
    # # plt.show()

    # read_list(a0List, "a0List.pkl")
    # read_list(weightedSignal, "weightedSignal.pkl")
    


if __name__=="__main__":
    main()
