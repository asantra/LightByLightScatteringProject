#!/usr/bin/python
import os
import os.path
import math
import array
import numpy as np
import ROOT
import glob

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptFit(0)
# ROOT.gStyle.SetOptStat(0)

BXs = {1:(1,500), 2:(501,1000), 3:(1001,1500), 4:(1501,2000), 5:(2001,2500), 6:(2501, 3000), 7:(3001, 3500), 8:(3501,4000), 9:(4001, 4500), 10:(4501, 5000), 11:(5001, 5500), 12:(5501, 6000)}


chain_list = glob.glob('/storage/agrp/arkas/E320WorkArea_a0_10.0/run_*/*_v1.root')
chain = ROOT.TChain("tt")
for fname in chain_list:
    job = int(fname.split("_")[-2].replace("Iteration",""))
    if(job<BXs[1][0] or job>BXs[1][1]): continue
    print(f"Adding file: {fname}")
    chain.AddFile(fname)

histos = {}
histos.update( {"ha0_gam": ROOT.TH1D("ha0_gam",";a_{0};Photons",1000,0,10)} )
histos.update( {"ha0_ele": ROOT.TH1D("ha0_ele",";a_{0};Electrons",1000,0,10)} )
histos.update( {"ha0_pos": ROOT.TH1D("ha0_pos",";a_{0};Positrons",1000,0,10)} )
histos.update( {"hE_gam": ROOT.TH1D("hE_gam",";E [GeV];Photons",1000,0,10)} )
histos.update( {"hE_ele": ROOT.TH1D("hE_ele",";E [GeV];Electrons",1000,0,10)} )
histos.update( {"hE_pos": ROOT.TH1D("hE_pos",";E [GeV];Positrons",1000,0,10)} )
for hname,hist in histos.items(): hist.Sumw2()

print("Starting loop over events in the chain:")
for entry,event in enumerate(chain):
    if(entry>0 and entry%100000==0): print(f"processed {entry+1} events")
    for i in range(event.pdgId.size()):
        sfx = "_gam"
        if  (event.pdgId[i]==22):  sfx = "_gam"
        elif(event.pdgId[i]==+11): sfx = "_ele"
        elif(event.pdgId[i]==-11): sfx = "_pos"
        else: continue
        histos["ha0"+sfx].Fill(event.a0out[i])
        histos["hE"+sfx].Fill(event.E[i])

foutname = "arka.root"
print(f"Saving histograms in {foutname}")
fout = ROOT.TFile(foutname,"RECREATE")
fout.cd()
for hname,hist in histos.items(): hist.Write()
fout.Write()
fout.Close()
