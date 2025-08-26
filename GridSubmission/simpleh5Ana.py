### simple script to analyze the h5 files

import h5py
import glob
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
    infoDict = {  "0.5": {"suf": "_xF1B", "wt": 5e-7},
                  "1.0": {"suf": "_xF1B", "wt": 5e-7},
                  "2.0": {"suf": "_xF1B", "wt": 5e-7},
                  "3.0": {"suf": "_xF1B", "wt": 5e-7},
                  "4.0": {"suf": "_xF1B", "wt": 5e-7},
                  "5.0": {"suf": "_xF1B", "wt": 5e-7},
                  "6.0": {"suf": "_xF1B", "wt": 5e-7},
                  "7.0": {"suf": "_xF1B", "wt": 5e-7},
                  "8.0": {"suf": "_xF1B", "wt": 5e-7},
                  "9.0": {"suf": "_xF1B", "wt": 5e-7},
                  "10.0":{"suf": "_xF1B", "wt": 5e-7},
                  }
    # infoDict = {    "0.32": {"suf": "_xF1B_Eachh5Weightedto1BX", "wt": 5e-7, "circular":[201,300],"linear":[301,400]},
    #                 "0.4": {"suf": "_xF1B_Eachh5Weightedto1BX", "wt": 5e-7, "circular":[1,100],"linear":[101,200]}
    #             #   "0.8": {"suf": "_xF1_Eachh5Weightedto1BX", "wt": 5e-7},
    #             #   "1.0": {"suf": "_xF1_Eachh5Weightedto1BX", "wt": 5e-7}
    #             }

    weightedSignal = []
    weightedSignalError = []
    a0List = []
    # polari = sys.argv[1]

    
    for a0 in infoDict:
        fIns = []
        errorFile = 0
        print("a0 ------- ", a0, " ---- ")

    
        fIns = glob.glob("/storage/agrp/arkas/E320WorkArea_a0_"+a0+infoDict[a0]["suf"]+"/run_*/*.h5")

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
        # print("photons list: ", photonList)
        # print("electrons list: ", electronList)
        # print("positrons list: ", positronList)

        posit = 0
        elect = 0
        phot  = 0
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
        print("Total error files: ", errorFile)
        # print("Positron weights: ", positronWeight)

        ## constant factor
        # weightedPositron = posit*infoDict[a0]["wt"]/float(len(positronList))
        ## variable factor
        weightedPositron = wtPosit/float(len(positronList))
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
    # write_list(a0List, "a0List_a0le1p0.pkl")
    # write_list(weightedSignal, "weightedSignal_a0le1p0.pkl")


if __name__=="__main__":
    main()
