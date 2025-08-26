### simple script to analyze the h5 files

import h5py
import glob
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import ROOT
from ROOT import TFile, TTree



infoDict = {  "0.5": {"suf": "_xF1B", "wt": 5e-7},
              "1": {"suf": "_xF1B", "wt": 5e-7},
              "2": {"suf": "_xF1B", "wt": 5e-7},
              "3": {"suf": "_xF1B", "wt": 5e-7},
              "4": {"suf": "_xF1B", "wt": 5e-7},
              "5": {"suf": "_xF1B", "wt": 5e-7},
              "6": {"suf": "_xF1B", "wt": 5e-7},
              "7": {"suf": "_xF1M", "wt": 5e-4},
              "8": {"suf": "_xF1M", "wt": 5e-4},
              "9": {"suf": "_xF1M", "wt": 5e-4},
              "10":{"suf": "_xF100", "wt":5.0},
              }




for a0 in infoDict:
    if (a0!='10'): continue
    print("a0 ------- ", a0, " ---- ")

    tf = TFile( 'raw_E320_lp_'+a0+'_Horizontal.root', 'recreate' )
    
    tt_out    = TTree( 'tt','tt' )
    vx_out    = ROOT.std.vector( float )()
    vy_out    = ROOT.std.vector( float )()
    vz_out    = ROOT.std.vector( float )()
    time_out  = ROOT.std.vector( float )()
    px_out    = ROOT.std.vector( float )()
    py_out    = ROOT.std.vector( float )()
    pz_out    = ROOT.std.vector( float )()
    E_out     = ROOT.std.vector( float )()
    weight_out= ROOT.std.vector( float )()

    tt_out.Branch('vx', vx_out)
    tt_out.Branch('vy', vy_out)
    tt_out.Branch('vz', vz_out)
    tt_out.Branch('t', time_out)
    tt_out.Branch('px', px_out)
    tt_out.Branch('py', py_out)
    tt_out.Branch('pz', pz_out)
    tt_out.Branch('E', E_out)
    tt_out.Branch('wgt',  weight_out)
    
    fIns = glob.glob("/storage/agrp/arkas/PtarmiganWorkAreaHorizontal_a0_"+a0+infoDict[a0]["suf"]+"/run_*/*.h5")
    
    positronNumber = 0
    for name in fIns:
        fIn = h5py.File(name, 'r')
        momentum_value_positron = fIn['final-state/positron']['momentum'][()]
        position_value_positron = fIn['final-state/positron']['position'][()]
        id_value_positron = fIn['final-state/positron']['id'][()]
        weight_value_positron = fIn['final-state/positron']['weight'][()]

        for j in range(0, len(id_value_positron)):
            vx_out.clear()
            vy_out.clear()
            vz_out.clear()
            time_out.clear()
            px_out.clear()
            py_out.clear()
            pz_out.clear()
            E_out.clear()
            weight_out.clear()

            vx0    = position_value_positron[j][0] # for unit in mm. #*1.e-1 ## mm to cm
            vy0    = position_value_positron[j][1] # for unit in mm. #*1.e-1 ## mm to cm
            vz0    = position_value_positron[j][2] # for unit in mm. #*1.e-1 ## mm to cm
            t0     = position_value_positron[j][3]
            Energy = momentum_value_positron[j][0]
            px0    = momentum_value_positron[j][1]
            py0    = momentum_value_positron[j][2]
            pz0    = momentum_value_positron[j][3]

            vx_out.push_back(vx0)
            vy_out.push_back(vy0)
            vz_out.push_back(vz0)
            px_out.push_back(px0)
            py_out.push_back(py0)
            pz_out.push_back(pz0)
            E_out.push_back(Energy)
            time_out.push_back(t0)
            positronNumber += 1
            tt_out.Fill()
        
    print("positrons in file ", name, " - > ", positronNumber)
        
    tt_out.Write()
    tf.Write()
    tf.Write()
    tf.Close()
