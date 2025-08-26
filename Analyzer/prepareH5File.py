import h5py
import numpy as np
import pandas as pd
import random, math, sys
import matplotlib.pyplot as plt
import os

'''
    beam_axis: a string that is one of +x, -x, +z or -z, indicating the beam propagation direction.
    config/unit/momentum: a UTF-8 formatted string that gives the units of the four-momentum. Ptarmigan will recognise kg/m/s, as well as MeV/c and GeV/c (with or without the /c).
    config/unit/position: a UTF-8 formatted string that gives the units of the four-position. Ptarmigan will recognise um, micron, mm and m.
    final-state/{particle}/weight: an N⁢ × 1 array of doubles that gives the particle weights, i.e. the number of real particles represented.
    final-state/{particle}/momentum: an N⁢ × 4 array of doubles that gives the particle four-momenta 
    final-state/{particle}/position: an N⁢ × 4 array of doubles that gives the particle four-positions
'''

## create an h5 file for the input beam condition of ELI-NP
def main():
    outDir = "inputDistributionsToPtarmigan"
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    ### read the csv file into a dataframe    
    cols_names= ["Energy", "dNdE"]

    data = (
        pd.read_csv("Spectrum_ELI_fig1_4.csv",
                    header=None,
                    names=cols_names)
            .dropna(axis=1, how="all")
        )
    rowNumber = len(data)
    print("bins in the energy histgram: ", rowNumber)

    # Load data into DataFrame 
    df = pd.DataFrame(data = data); 
  
    plt.scatter(df['Energy'], df['dNdE'],s=0.01)
    plt.savefig(outDir+"/scatterPlot_Input.png")
    # plt.show()
    plt.clf()

    plt.hist(df["Energy"], bins=rowNumber, weights=df["dNdE"])
    plt.savefig(outDir+"/histogram_Input.png")
    # plt.show()
    plt.clf()

    ### 1 nC bunch charge means:
    totalElectron = 6.25e6 ### 1nC = 6.25B electrons
    # totalElectron = 6.25e4 ### 1nC = 6.25B electrons, but at present I divide into 100000 separate files
    totaldNdE = data["dNdE"].sum()
    normalizingFactor = totalElectron/totaldNdE
    data.dNdE *= normalizingFactor
    data.dNdE = round(data.dNdE)
    print("Total number of particles after normalizing: ", data["dNdE"].sum())

    plt.scatter(df['Energy'], df['dNdE'], s=0.01)
    plt.savefig(outDir+"/afternormalizingdf.png")
    # plt.show()
    plt.clf()

    
    plt.hist(df['Energy'], bins=rowNumber, weights=df['dNdE'])
    plt.savefig(outDir+"/beforeLoop_EnergyHist.png")
    # plt.show()
    plt.clf()


    ### mass of electron
    me = 511e-6 ## in GeV
    ### draw random number for position in z, z bunch size FWHM 10 um around 0
    # z position
    mu_z    = 0
    sigma_z = 10./(2*math.sqrt(2*math.log(2)))

    ### draw random number for position in x and y, FWHM 5 um
    mu_r    = 0  
    sigma_r = 5./(2*math.sqrt(2*math.log(2)))

    for j in range(2,3):
        weightVec    = []
        position4Vec = []
        momentum4Vec = []
        dndeList     = []

        counter      = 0
        for index, row in data.iterrows():
            # print("working on index: ", index, " row[dNdE]: ", row["dNdE"])
            resetCounter = 0
            for i in range(0, int(row["dNdE"])):
                counter += 1
                resetCounter += 1
                if(counter%1000==0): print("working on ", counter)
                # if(counter > maximumElectron): break

                ### generate the position 4 vector
                r        = abs(random.gauss(mu_r, sigma_r))
                angle    = random.uniform(0,2*math.pi)
                x        = r*math.cos(angle)
                y        = r*math.sin(angle)
                z        = random.gauss(mu_z, sigma_z)

                time     = random.uniform(0,2)

                posVec   = [time, x, y, z]
                position4Vec.append(posVec)

                ### generate the momentum 4 vector
                energy   = row["Energy"]
                momentum = math.sqrt(energy*energy - me*me)
                px       = random.gauss(0,momentum*0.0001/2.)
                py       = random.gauss(0,momentum*0.0001/2.)
                pz       = math.sqrt(momentum*momentum - px*px - py*py)
                momVec   = [energy, px, py, pz]
                momentum4Vec.append(momVec)
                weightVec.append(1.)
            dndeList.append(resetCounter)

        print("Total number of particles written: ", counter)
        # for index, elem in enumerate(dndeList):
        #     print("dndeList: ", index, elem)

        # df2 = pd.DataFrame(dndeList, columns=['dndeList'])
        # # Extracting columns and combining them into a new dataframe
        # df_combined = pd.DataFrame({'Old': data['dNdE'], 'New': df2["dndeList"], "Subtract": data['dNdE'] - df2["dndeList"]})
        # df_combined.to_csv("comparedNdEValues.csv") 

        pltEnergy = [a[0] for a in momentum4Vec]
        # print(pltEnergy)
        plt.hist(pltEnergy, bins=rowNumber)
        plt.savefig(outDir+"/afterLoop_EnergyHist.png")
        # plt.show()
        plt.clf()

        zPos = [a[3] for a in position4Vec]
        plt.hist(zPos, bins=100)
        plt.savefig(outDir+"/bunchlength.png")
        # plt.show()
        plt.clf()
        
        # Open HDF5 file and write in the data_dict structure and info
        # Save to HDF5
        h5_filename      = outDir+"/inputbeam_electron_ELINP_6p25e6_electrons_"+str(j)+".h5"

        ### add strings to the created h5 file
        axis             = "+z"
        momentumUnit     = "GeV"
        positionUnit     = "um"

        f                = h5py.File(h5_filename, "w")    
        f["beam_axis"]   = axis
        grp1             = f.create_group("config")
        grp2             = grp1.create_group("unit")
        grp2["momentum"] = momentumUnit
        grp2["position"] = positionUnit

        ### now create the momentum and position from the distribution
        grp3             = f.create_group("final-state")
        grp4             = grp3.create_group("electron")
        grp4["weight"]   = weightVec
        grp4["momentum"] = momentum4Vec
        grp4["position"] = position4Vec

        f.close()



if __name__ == "__main__":
    main()