import h5py
import numpy as np
import pandas as pd
import random, math, sys
import matplotlib.pyplot as plt 
from matplotlib import colors

'''
    beam_axis: a string that is one of +x, -x, +z or -z, indicating the beam propagation direction.
    config/unit/momentum: a UTF-8 formatted string that gives the units of the four-momentum. Ptarmigan will recognise kg/m/s, as well as MeV/c and GeV/c (with or without the /c).
    config/unit/position: a UTF-8 formatted string that gives the units of the four-position. Ptarmigan will recognise um, micron, mm and m.
    final-state/{particle}/weight: an N⁢ × 1 array of doubles that gives the particle weights, i.e. the number of real particles represented.
    final-state/{particle}/momentum: an N⁢ × 4 array of doubles that gives the particle four-momenta 
    final-state/{particle}/position: an N⁢ × 4 array of doubles that gives the particle four-positions
'''

## test an h5 file for the input beam condition of ELI-NP
def main():
    # inFile = sys.argv[1]
    inFile = "inputbeam_electron_ELINP_1nC_1.h5"
    fIn    = h5py.File(inFile, "r")
    onlyE  = []
    onlyPx = []
    onlyPy = []
    onlyPz = []
    xPos   = []
    yPos   = []
    zPos   = []
    ct     = []

    ### get the energy and pz momentum distribution
    pList = fIn['final-state/electron/momentum'][()]
    for p in pList:
        E  = p[0] 
        px = p[1]
        py = p[2]
        pz = p[3]
        
        onlyE.append(E)
        onlyPx.append(px)
        onlyPy.append(py)
        onlyPz.append(pz)

    plt.hist(onlyE, bins=100)
    plt.xlabel('E [GeV]') 
    plt.ylabel('Entries/bin')
    plt.savefig("EnergyDistribution.png")
    plt.show()

    plt.hist(onlyPx, bins=100)
    plt.xlabel('Px [GeV]') 
    plt.ylabel('Entries/bin') 
    plt.savefig("PxDistribution.png")
    plt.show()

    plt.hist(onlyPy, bins=100)
    plt.xlabel('Py [GeV]') 
    plt.ylabel('Entries/bin') 
    plt.savefig("PyDistribution.png")
    plt.show()

    plt.hist(onlyPz, bins=100)
    plt.xlabel('Pz [GeV]') 
    plt.ylabel('Entries/bin') 
    plt.savefig("PzDistribution.png")
    plt.show()

    ### get the position x,y
    positionList = fIn['final-state/electron/position'][()]
    for pos in positionList:
        ctval = pos[0]
        x     = pos[1]
        y     = pos[2]
        z     = pos[3]
        
        xPos.append(x)
        yPos.append(y)
        zPos.append(z)
        ct.append(ctval) 

    # Create a 1-D histogram 
    plt.hist(ct, bins=100) 
    
    # Add labels and title 
    plt.xlabel('ct [um]') 
    plt.ylabel('Entries/bin') 
    plt.title('ct distribution') 
    
    # Display the plot 
    plt.show()
    plt.savefig("ctdistribution.png")


    # Create a 2-D histogram 
    fig, ax = plt.subplots()
    hh = ax.hist2d(xPos, yPos, bins=100, norm=colors.LogNorm())
    fig.colorbar(hh[3], ax=ax)
    
    # Add labels and title 
    ax.set_xlabel('x position [um]') 
    ax.set_ylabel('y position [um]') 
    ax.set_title('2-D electron beam cross-section') 
    
    # Display the plot 
    fig.show()
    fig.savefig("beamprofile.png")


    

if __name__ == "__main__":
    main()