import h5py
import numpy as np
import pandas as pd
import random, math, sys
import matplotlib.pyplot as plt 
from matplotlib import colors
import os

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
    outDir = "lcfa_interaction"
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    inFile = "/Users/arkasantra/arka/Tom_Work_Theory/testPtarmigan/ptarmigan/examples/ELINP_profile_1_particles.h5"
    fIn    = h5py.File(inFile, "r")
    finalParticleType = ['positron', 'electron', 'photon']

    for particle in finalParticleType:
        onlyE  = []
        onlyPx = []
        onlyPy = []
        onlyPz = []
        xPos   = []
        yPos   = []
        zPos   = []
        ct     = []

        ### get the energy and pz momentum distribution
        pList = fIn['final-state/'+particle+'/momentum'][()]
        print("number of ", particle, " --> ", len(pList))
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
        plt.xlabel('E [MeV]') 
        plt.ylabel('Entries/bin')
        plt.savefig(outDir+"/EnergyDistribution_"+particle+"_Output.png")
        plt.title("Energy distribution for "+particle)
        plt.show()
        plt.clf()

        plt.hist(onlyPx, bins=100)
        plt.xlabel('Px [MeV]') 
        plt.ylabel('Entries/bin') 
        plt.savefig(outDir+"/PxDistribution_"+particle+"_Output.png")
        plt.title("Px distribution for "+particle)
        plt.show()
        plt.clf()

        plt.hist(onlyPy, bins=100)
        plt.xlabel('Py [MeV]') 
        plt.ylabel('Entries/bin') 
        plt.savefig(outDir+"/PyDistribution_"+particle+"_Output.png")
        plt.title("Py distribution for "+particle)
        plt.show()
        plt.clf()

        plt.hist(onlyPz, bins=100)
        plt.xlabel('Pz [MeV]') 
        plt.ylabel('Entries/bin') 
        plt.savefig(outDir+"/PzDistribution_"+particle+"_Output.png")
        plt.title("Pz distribution for "+particle)
        plt.show()
        plt.clf()

        ### get the position x,y
        positionList = fIn['final-state/'+particle+'/position'][()]
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
        plt.xlabel('ct [m]') 
        plt.ylabel('Entries/bin') 
        plt.title('ct distribution for '+particle) 
        # Display the plot 
        plt.savefig(outDir+"/ctdistribution_"+particle+"_Output.png")
        plt.show()
        plt.clf()

        if particle!="electron":
            a0List_Pos = list(fIn['final-state/'+particle]['a0_at_creation'])
            # Create a 1-D histogram 
            plt.hist(a0List_Pos, bins=100) 
            # Add labels and title 
            plt.xlabel('a0') 
            plt.ylabel('Entries/bin') 
            plt.title('a0 at IP ('+particle+')') 
            # Display the plot 
            plt.savefig(outDir+"/a0IPdistribution_"+particle+"_Output.png")
            plt.show()
            plt.clf()

        # Create a 2-D histogram
        plt.clf()
        fig, ax = plt.subplots()
        hh = ax.hist2d(xPos, yPos, bins=100, norm=colors.LogNorm())
        fig.colorbar(hh[3], ax=ax)
        # Add labels and title 
        ax.set_xlabel('vtx_x position [m]') 
        ax.set_ylabel('vtx_y position [m]') 
        ax.set_title('2-D vtx position for '+particle)
        # Display the plot
        fig.savefig(outDir+"/xy_"+particle+"_Output.png")
        plt.show() 




if __name__ == "__main__":
    main()