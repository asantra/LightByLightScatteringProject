import os, sys
import math, time
import h5py
from array import array
import numpy as np
import ROOT
from ROOT import TFile, TTree, TLorentzVector
import glob
# import subprocess
# from subprocess import call
import argparse



meMeV = 0.5109989461 ## MeV
meGeV = meMeV/1000.
MeV2GeV = 1./1000.

def main():
    needPhoton   = True
    needElectron = True
    needPositron = True
    parser = argparse.ArgumentParser(description='Code to get root files from h5')
    parser.add_argument('-x', action="store", dest="xi", type=str, default="5.0")
    parser.add_argument('-g', action="store", dest="gamma", type=str, default="10.0")
    parser.add_argument('-v', action="store", dest="version", type=str, default="1")
    parser.add_argument('-i', action="store", dest="iteration", type=str, default="1")
    args         = parser.parse_args()
    xiInput      = args.xi
    gammaInput   = args.gamma
    ver          = args.version
    iter         = args.iteration

    ### for grid files, E320 files unweighted
    # inputDir  = "/storage/agrp/arkas/E320Files/ForGeant4Processing/Onlyh5Files/"
    # storage   = inputDir
    # storage   = "/storage/agrp/arkas/E320Files/ForGeant4Processing/RootFiles/"
    
    ### for grid files, E320 files weighted
    # inputDir  = "/storage/agrp/arkas/E320Files/E320WorkArea_a0_10.0_positronpairrate_xF1M/"
    # storage   = inputDir

    inputDir  = "/storage/agrp/arkas/E320Files/E320WorkArea_a0_5.0_xF1B_Eachh5Weightedto1BX/"
    storage   = inputDir
    # storage   = "/storage/agrp/arkas/E320Files/ForGeant4Processing/RootFiles/"
    
    
    # ### for grid files on ELINP
    # inputDir  = "/storage/agrp/arkas/ELINP_a0_20.0_LMAFiles/"
    # # storage   = inputDir
    # storage   = "/storage/agrp/arkas/ELINP_a0_20.0_LMAFiles/"

    ### for multi-threaded processing
    # p         = subprocess.Popen("mkdir -p "+storage, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # out, err  = p.communicate()

    # # ### for E320, grid, only positron, no positron generation factor
    # tf = TFile( storage+'run_'+iter+'/raw_e320_a0_'+str(xiInput)+'_gamma'+str(gammaInput)+'_Iteration'+iter+'_v'+ver+'_positrons_only.root', 'recreate' )
    # print("The output file: ", storage+'run_'+iter+'/raw_e320_a0_'+str(xiInput)+'_gamma'+str(gammaInput)+'_Iteration'+iter+'_v'+ver+'_positrons_only.root', 'recreate')

    # # ### for E320, grid, only positron, positron generation factor of 1M
    tf = TFile( storage+'run_'+iter+'/raw_e320_a0_'+str(xiInput)+'_gamma'+str(gammaInput)+'_Iteration'+iter+'_v'+ver+'_xF1B_Eachh5Weightedto1BX.root', 'recreate' )
    print("The output file: ", storage+'run_'+iter+'/raw_e320_a0_'+str(xiInput)+'_gamma'+str(gammaInput)+'_Iteration'+iter+'_v'+ver+'_xF1B_Eachh5Weightedto1BX.root')



    ### ELINP files
    # tf = TFile( storage+'raw_elinp_a0_'+str(xiInput)+'_Iteration'+iter+'_v'+ver+'_positrons_only.root', 'recreate' )
    # print("The output file: ", storage+'raw_elinp_a0_'+str(xiInput)+'_Iteration'+iter+'_v'+ver+'_positrons_only.root')

    
    ### for E320, grid, all particles
    # tf = TFile( storage+'run_'+iter+'/raw_e320_a0_'+str(xiInput)+'_gamma'+str(gammaInput)+'_Iteration'+iter+'_v'+ver+'.root', 'recreate' )
    # print("The output file: ", storage+'run_'+iter+'/raw_e320_a0_'+str(xiInput)+'_gamma'+str(gammaInput)+'_Iteration'+iter+'_v'+ver+'.root')

    
    #### store the runids to the branch
    runid = int(iter)

    tt_out    = TTree( 'tt','tt' )
    vx_out    = ROOT.std.vector( float )()
    vy_out    = ROOT.std.vector( float )()
    vz_out    = ROOT.std.vector( float )()
    px_out    = ROOT.std.vector( float )()
    py_out    = ROOT.std.vector( float )()
    pz_out    = ROOT.std.vector( float )()
    eta_out   = ROOT.std.vector( float )()
    theta_out = ROOT.std.vector( float )()
    phi_out   = ROOT.std.vector( float )()
    E_out     = ROOT.std.vector( float )()
    pdgId_out = ROOT.std.vector( int )()
    a0_out    = ROOT.std.vector( float )()
    mpid_out  = ROOT.std.vector( str )()
    wgt_out   = ROOT.std.vector( float )()
    time_out  = ROOT.std.vector( float )()
    xi_out    = ROOT.std.vector( float )()
    Id_out    = ROOT.std.vector( int )()
    parentId_out= ROOT.std.vector( int )()
    runId_out = ROOT.std.vector( int )()

    tt_out.Branch('vx', vx_out)
    tt_out.Branch('vy', vy_out)
    tt_out.Branch('vz', vz_out)
    tt_out.Branch('px', px_out)
    tt_out.Branch('py', py_out)
    tt_out.Branch('pz', pz_out)
    tt_out.Branch('eta', eta_out)
    tt_out.Branch('theta', theta_out)
    tt_out.Branch('phi', phi_out)
    tt_out.Branch('E',  E_out)
    tt_out.Branch('wgt',  wgt_out)
    tt_out.Branch('pdgId',pdgId_out)
    tt_out.Branch('a0out',a0_out)
    tt_out.Branch('mpId',mpid_out)
    tt_out.Branch('time',time_out)
    tt_out.Branch('xi',xi_out)
    tt_out.Branch('id',Id_out)
    tt_out.Branch('parentId',parentId_out)
    tt_out.Branch('runId',runId_out)

    
    ### for E320, grid
    print("The input h5 file directory: ", inputDir+"run_"+iter+"/E320_profile_Iteration"+iter+"_particles.h5")
    fIns = glob.glob(inputDir+"run_"+iter+"/E320_profile_Iteration"+iter+"_particles.h5")
    

    # print("The input h5 file directory: ", inputDir+"E320_profile_Iteration"+iter+"_particles.h5")
    # fIns = glob.glob(inputDir+"E320_profile_Iteration"+iter+"_particles.h5")


    ### for ELI-NP
    # print("The input h5 file directory: ", inputDir+"ELINP_profile_Iteration"+iter+"_particles.h5")
    # fIns = glob.glob(inputDir+"ELINP_profile_Iteration"+iter+"_particles.h5")

    print("The input h5 file: ",fIns)   
    photonNumberList = []
    ##### work only on the events having same order of tracks as that of the highest tracked event
    for name in fIns:
        #### input file
        fIn = h5py.File(name, 'r')
        id_value_photon = fIn['final-state/photon']['id'][()]
        photonNumberList.append(len(id_value_photon))

    #### sort the list in maximum to minimum
    photonNumberList.sort(reverse=True)

    for name in fIns:
        
        #### input file
        fIn = h5py.File(name, 'r')
        print("reading: ",name)
                
        ### photons
        photonNumber = 0
        if(needPhoton):
            id_value_photon       = fIn['final-state/photon']['id'][()]
            parentid_value_photon = fIn['final-state/photon']['parent_id'][()]
            momentum_value_photon = fIn['final-state/photon']['momentum'][()]
            position_value_photon = fIn['final-state/photon']['position'][()]
            weight_value_photon   = fIn['final-state/photon']['weight'][()]
            a0_out_               = fIn['final-state/photon']['a0_at_creation'][()]
            print("this file has ",len(id_value_photon)," photons")

            #### if(highestPhotonEvents>50):
            ####     if len(id_value_photon) < highestPhotonEvents/2.0: 
            ####         print("This file ",name," has very few photons ",len(id_value_photon), " ---- NOT PROCESSING")
            ####         continue
            #### else:
            ####     if len(id_value_photon) < highestPhotonEvents/10.0: 
            ####         print("This file ",name," has very few photons ",len(id_value_photon), " ---- NOT PROCESSING")
            ####         continue

            for j in range(0, len(id_value_photon)):
                if(photonNumber%1000==0): print("processed: ", photonNumber," photons")
                ### clear output tree branches
                mpid_out.clear()
                pdgId_out.clear()
                a0_out.clear()
                wgt_out.clear()
                vx_out.clear()
                vy_out.clear()
                vz_out.clear()
                px_out.clear()
                py_out.clear()
                pz_out.clear()
                eta_out.clear()
                theta_out.clear()
                phi_out.clear()
                E_out.clear()
                xi_out.clear()
                time_out.clear()
                Id_out.clear()
                parentId_out.clear()
                runId_out.clear()

                #### this is the wrong convention, as Ptarmigan saves position 4-vectors in (ct, \vec{r}) format - NOT (x,y,z,t) format as is done here.
                vx0    = position_value_photon[j][0]*1.e3 ## m to mm
                vy0    = position_value_photon[j][1]*1.e3 ## m to mm
                vz0    = position_value_photon[j][2]*1.e3 ## m to mm
                t0     = position_value_photon[j][3]


                
                Energy = momentum_value_photon[j][0]*1.e-3 ## MeV to GeV
                px0    = momentum_value_photon[j][1]*1.e-3 ## MeV to GeV
                py0    = momentum_value_photon[j][2]*1.e-3 ## MeV to GeV
                pz0    = momentum_value_photon[j][3]*1.e-3 ## MeV to GeV

                photonVec = TLorentzVector() 
                photonVec.SetPxPyPzE(px0, py0, pz0, Energy)

                eta0   = photonVec.Eta()
                theta0 = photonVec.Theta()
                phi0   = photonVec.Phi()

                pdgId0 = 22
                a0Value= a0_out_[j]
                wgt0   = weight_value_photon[j]
                MP_ID  = str(id_value_photon[j])+"_"+str(pdgId0)
                xi0    = float(xiInput)
                id     = id_value_photon[j]
                parentid = parentid_value_photon[j]

                mpid_out.push_back(str(MP_ID))
                wgt_out.push_back(wgt0)  
                pdgId_out.push_back(int(pdgId0))
                a0_out.push_back(a0Value)
                vx_out.push_back(vx0)
                vy_out.push_back(vy0)
                vz_out.push_back(vz0)
                px_out.push_back(px0)
                py_out.push_back(py0)
                pz_out.push_back(pz0)
                eta_out.push_back(eta0)
                theta_out.push_back(theta0)
                phi_out.push_back(phi0)
                E_out.push_back(Energy)
                time_out.push_back(t0)
                xi_out.push_back(xi0)
                Id_out.push_back(int(id))
                parentId_out.push_back(int(parentid))
                runId_out.push_back(runid)


                photonNumber += 1
                tt_out.Fill()


        electronNumber = 0
        if(needElectron):
            ### electrons are only collected for g+laser
            id_value_electron       = fIn['final-state/electron']['id'][()]
            print("this file has ",len(id_value_electron)," electrons")
            parentid_value_electron = fIn['final-state/electron']['parent_id'][()]
            momentum_value_electron = fIn['final-state/electron']['momentum'][()]
            position_value_electron = fIn['final-state/electron']['position'][()]
            weight_value_electron   = fIn['final-state/electron']['weight'][()]
            ### electrons don't have a0_at_creation
            for j in range(0, len(id_value_electron)):
                if(electronNumber%1000==0): print("processed: ", electronNumber," electrons")
                mpid_out.clear()
                pdgId_out.clear()
                a0_out.clear()
                wgt_out.clear()
                vx_out.clear()
                vy_out.clear()
                vz_out.clear()
                px_out.clear()
                py_out.clear()
                pz_out.clear()
                eta_out.clear()
                theta_out.clear()
                phi_out.clear()
                E_out.clear()
                xi_out.clear()
                time_out.clear()
                Id_out.clear()
                parentId_out.clear()
                runId_out.clear()

                #### this is the wrong convention, as Ptarmigan saves position 4-vectors in (ct, \vec{r}) format - NOT (x,y,z,t) format as is done here.
                vx0    = position_value_electron[j][0]*1.e3 ## m to mm
                vy0    = position_value_electron[j][1]*1.e3 ## m to mm
                vz0    = position_value_electron[j][2]*1.e3 ## m to mm
                t0     = position_value_electron[j][3]
                Energy = momentum_value_electron[j][0]*1.e-3 ## MeV to GeV
                px0    = momentum_value_electron[j][1]*1.e-3 ## MeV to GeV
                py0    = momentum_value_electron[j][2]*1.e-3 ## MeV to GeV
                pz0    = momentum_value_electron[j][3]*1.e-3 ## MeV to GeV

                electronVec = TLorentzVector()
                electronVec.SetPxPyPzE(px0, py0, pz0, Energy)

                eta0   = electronVec.Eta()
                theta0 = electronVec.Theta()
                phi0   = electronVec.Phi()


                pdgId0 = 11
                a0Value = -999 ## dummy value
                wgt0   = weight_value_electron[j]
                MP_ID  = str(id_value_electron[j])+"_"+str(pdgId0)
                xi0    = float(xiInput)
                id     = id_value_electron[j]
                parentid = parentid_value_electron[j]


                mpid_out.push_back(str(MP_ID))
                wgt_out.push_back(wgt0)
                pdgId_out.push_back(int(pdgId0))
                a0_out.push_back(a0Value)
                vx_out.push_back(vx0)
                vy_out.push_back(vy0)
                vz_out.push_back(vz0)
                px_out.push_back(px0)
                py_out.push_back(py0)
                pz_out.push_back(pz0)
                eta_out.push_back(eta0)
                theta_out.push_back(theta0)
                phi_out.push_back(phi0)
                E_out.push_back(Energy)
                time_out.push_back(t0)
                xi_out.push_back(xi0)
                Id_out.push_back(int(id))
                parentId_out.push_back(int(parentid))
                runId_out.push_back(runid)

                electronNumber += 1
                tt_out.Fill()
        

        positronNumber = 0
        if(needPositron):
            ### positrons are only collected for g+laser
            id_value_positron       = fIn['final-state/positron']['id'][()]
            print("this file has ",len(id_value_positron)," positrons")
            parentid_value_positron = fIn['final-state/positron']['parent_id'][()]
            momentum_value_positron = fIn['final-state/positron']['momentum'][()]
            position_value_positron = fIn['final-state/positron']['position'][()]
            weight_value_positron   = fIn['final-state/positron']['weight'][()]
            a0_out_                 = fIn['final-state/positron']['a0_at_creation'][()]
            for j in range(0, len(id_value_positron)):
                if(positronNumber%10==0): print("processed: ", positronNumber," positrons")
                
                mpid_out.clear()
                pdgId_out.clear()
                a0_out.clear()
                wgt_out.clear()
                vx_out.clear()
                vy_out.clear()
                vz_out.clear()
                px_out.clear()
                py_out.clear()
                pz_out.clear()
                eta_out.clear()
                theta_out.clear()
                phi_out.clear()
                E_out.clear()
                xi_out.clear()
                time_out.clear()
                Id_out.clear()
                parentId_out.clear()
                runId_out.clear()

                #### this is the wrong convention, as Ptarmigan saves position 4-vectors in (ct, \vec{r}) format - NOT (x,y,z,t) format as is done here.
                vx0    = position_value_positron[j][0]*1.e3 ## m to mm
                vy0    = position_value_positron[j][1]*1.e3 ## m to mm
                vz0    = position_value_positron[j][2]*1.e3 ## m to mm
                t0     = position_value_positron[j][3]
                Energy = momentum_value_positron[j][0]*1.e-3 ## MeV to GeV
                px0    = momentum_value_positron[j][1]*1.e-3 ## MeV to GeV
                py0    = momentum_value_positron[j][2]*1.e-3 ## MeV to GeV
                pz0    = momentum_value_positron[j][3]*1.e-3 ## MeV to GeV

                positronVec = TLorentzVector()
                positronVec.SetPxPyPzE(px0, py0, pz0, Energy)

                eta0   = positronVec.Eta()
                theta0 = positronVec.Theta()
                phi0   = positronVec.Phi()


                pdgId0 = -11
                a0Value= a0_out_[j]
                wgt0   = weight_value_positron[j]
                MP_ID  = str(id_value_positron[j])+"_"+str(pdgId0)
                xi0    = float(xiInput)
                id     = id_value_positron[j]
                parentid = parentid_value_positron[j]


                mpid_out.push_back(str(MP_ID))
                wgt_out.push_back(wgt0)  
                pdgId_out.push_back(int(pdgId0))
                a0_out.push_back(a0Value) 
                vx_out.push_back(vx0)
                vy_out.push_back(vy0)
                vz_out.push_back(vz0)
                px_out.push_back(px0)
                py_out.push_back(py0)
                pz_out.push_back(pz0)
                eta_out.push_back(eta0)
                theta_out.push_back(theta0)
                phi_out.push_back(phi0)
                E_out.push_back(Energy)
                time_out.push_back(t0)
                xi_out.push_back(xi0)
                Id_out.push_back(int(id))
                parentId_out.push_back(int(parentid))
                runId_out.push_back(runid)

                
                positronNumber += 1
                tt_out.Fill()
            

        
        print("electrons ", electronNumber, " photons ", photonNumber, " and positrons ", positronNumber, " in file ", name)
        
    tt_out.Write()
    tf.Write()
    tf.Write()
    tf.Close()


if __name__=="__main__":
    intime = time.time()
    main()
    print("----- the time taken ", time.time() - intime, " s")
