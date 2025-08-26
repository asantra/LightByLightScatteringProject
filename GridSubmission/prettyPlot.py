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

    a0List              = read_list("a0List.pkl")
    weightedSignal_Full      = read_list("weightedSignal.pkl")
    weightedSignal        = [i*1 for i in weightedSignal_Full]
    weightedSignalError = [0 for i in range(0, len(weightedSignal))]

    fig, ax0 = plt.subplots()
    ax0.plot(a0List, weightedSignal, 'ko', linewidth=1, linestyle="--",markersize=6)


    for i in range(0, len(a0List)):
        print("a0: ", a0List[i], " weightedSignal: ", weightedSignal[i])

    ax0.set_yscale('log')
    # ax0.set_xscale('log')
    ax0.set_xbound(1.0, 11.0)
    # ax0.xticks(fontsize=10)
    # ax0.yticks(fontsize=14)
    ax0.set_xlabel(r'$a_{0}$',loc='right',fontsize = 14)
    ax0.set_ylabel('Positrons/BX',loc='top',fontsize = 14)
    ax0.set_xticks([1,2,3,4,5,6,7,8,9,10])
    ax0.set_yticks([1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1,1e1,1e2,1e3])
    ax0.tick_params(axis='x', labelsize=12)
    ax0.tick_params(axis='y', labelsize=12)
    ax0.text(1.3, 6.6, r'E320', fontsize=14)
    ax0.text(2.4, 6.6, r'simulation', fontsize=12, style='italic')
    ax0.text(1.4, 1.6, r'Made with Ptarmigan', fontsize=12)
    ax0.set_title(r'beam E: 10 GeV, r: 40 $\mu$m, l: 20 $\mu$m. laser 800 nm, 50 fs, 2 $\mu$m.', fontsize=12,loc='center')
    fig.subplots_adjust(right=0.98, top=0.93)
    # fig.text(60, .025, r'E320')
    ax0.grid(True, which='major', color='gray', linestyle='dotted', linewidth=1)

    fig.savefig("E320_PositronMultiplicity_Weighted_PrettyPlot.png")
    fig.savefig("E320_PositronMultiplicity_Weighted_PrettyPlot.pdf")
    plt.show()
    


if __name__=="__main__":
    main()
