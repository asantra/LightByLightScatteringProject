#!/usr/bin/python
import os
import ROOT

BXs = [[1,500], [501,1000], [1001,1500], [1501,2000], [2001,2500], [2501, 3000], [3001, 3500], [3501, 4000], [4001, 4500], [4501, 5000], [5001, 5500], [5501, 6000]]

allbxfiles = ""
for BX in BXs:
    sBX = str(BXs.index(BX)+1)
    inputfiles = ""
    targetfile = "BX"+sBX+"_positrons_only.root"
    allbxfiles += targetfile+" "
    for i in range(BX[0],BX[1]+1): 
        si = str(i)
        inputfiles += f"run_{si}/raw_e320_a0_10.0_gamma10.0_Iteration{si}_v1_positrons_only.root "
    print("The command: hadd -f ", targetfile," ", inputfiles)
    ROOT.gSystem.Exec(f"hadd -f {targetfile} {inputfiles}")

allbxcomb = "BX_all_positrons_only.root"
print("The final command: hadd ", allbxcomb," ", allbxfiles)
ROOT.gSystem.Exec(f"hadd {allbxcomb} {allbxfiles}")