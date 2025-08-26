### simple script to analyze the h5 files

import h5py
import glob

infoDict = {  "0.5": {"suf": "_xF1B", "wt": 5e-7},
              "1.0": {"suf": "_xF1B", "wt": 5e-7},
              "2.0": {"suf": "_xF1B", "wt": 5e-7},
              "3.0": {"suf": "_xF1B", "wt": 5e-7},
              "4.0": {"suf": "_xF1B", "wt": 5e-7},
              "5.0": {"suf": "_xF1B", "wt": 5e-7},
              "6.0": {"suf": "_xF1B", "wt": 5e-7},
              "7.0": {"suf": "_xF1M", "wt": 5e-4},
              "8.0": {"suf": "_xF1M", "wt": 5e-4},
              "9.0": {"suf": "_xF1M", "wt": 5e-4},
              "10.0":{"suf": "_xFOne", "wt":5.0},
              }



for a0 in infoDict:
    if (a0!='10.0'): continue
    print("a0 ------- ", a0, " ---- ")
    
    fIns = glob.glob("/storage/agrp/arkas/PtarmiganWorkAreaHorizontal_a0_"+a0+infoDict[a0]["suf"]+"/run_*/*.h5")
    
    photonList = []
    positronList = []
    electronList = []

    photonWeight = []
    positronWeight = []
    electronWeight = []
    
    for name in fIns:
        fIn = h5py.File(name, 'r')
        id_photon = fIn['final-state/photon']['id'][()]
        id_positron = fIn['final-state/positron']['id'][()]
        id_electron = fIn['final-state/electron']['id'][()]
        
        weight_photon = fIn['final-state/photon']['weight'][()]
        weight_positron = fIn['final-state/positron']['weight'][()]
        weight_electron = fIn['final-state/electron']['weight'][()]

        photonList.append(len(id_photon))
        positronList.append(len(id_positron))
        electronList.append(len(id_electron))

        photonWeight.append(weight_photon)
        electronWeight.append(weight_electron)
        positronWeight.append(weight_positron)

    print("photons list: ", photonList)
    print("electrons list: ", electronList)
    print("positrons list: ", positronList)

    phot  = 0
    posit = 0
    elect = 0
    
    wtPhot  = 0
    wtPosit = 0
    wtElec  = 0
    
    for i in positronList:
        posit += i
    for w in positronWeight:
        for x in w:
            wtPosit += x

    for j in electronList:
        elect += j
    for we in electronWeight:
        for wt in we:
            wtElec += wt

    for k in photonList:
        phot  += k
    for wp in photonWeight:
        for wtp in wp:
            wtPhot += wtp
    


    print("Total positron: ", posit, " electron: ", elect, " photon: ", phot)
    print("Total files: positron ", len(positronList), " electron: ", len(electronList), " photon: ", len(photonList))
    
    weightedPhoton   = wtPhot/float(len(photonList))
    weightedPositron = wtPosit/float(len(positronList))
    weightedElectron = wtElec/float(len(electronList))
    
    print("Weighted photon per BX: ", weightedPhoton)
    print("Weighted electron per BX: ", weightedElectron)
    print("Weighted positron per BX: ", weightedPositron)