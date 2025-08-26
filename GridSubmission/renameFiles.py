import glob, os, sys

inFiles = glob.glob("run_*")
renameNumber = 451
for folder in inFiles:
    print("folder: ", folder)
    runNumber = folder.split('_')[1]
    print("runNumber: ", runNumber)
    finalRunNumber = renameNumber + int(runNumber)
    print("renaming files for ",folder)
    print("mv run_"+runNumber+"/E320_profile_Iteration"+runNumber+".conf run_"+runNumber+"/E320_profile_Iteration"+str(finalRunNumber)+".conf")
    print("mv run_"+runNumber+"/E320_profile_Iteration"+runNumber+"_particles.h5 run_"+runNumber+"/E320_profile_Iteration"+str(finalRunNumber)+"_particles.h5")
    print("mv run_"+runNumber+"/E320_profile_Iteration"+runNumber+"_electron_energy.dat run_"+runNumber+"/E320_profile_Iteration"+str(finalRunNumber)+"_electron_energy.dat")
    print("mv run_"+runNumber+"/E320_profile_Iteration"+runNumber+"_photon_energy.dat run_"+runNumber+"/E320_profile_Iteration"+str(finalRunNumber)+"_photon_energy.dat")
    print("mv run_"+runNumber+" run_"+str(finalRunNumber))

    try:
        os.system("mv run_"+runNumber+"/E320_profile_Iteration"+runNumber+".conf run_"+runNumber+"/E320_profile_Iteration"+str(finalRunNumber)+".conf")
        os.system("mv run_"+runNumber+"/E320_profile_Iteration"+runNumber+"_particles.h5 run_"+runNumber+"/E320_profile_Iteration"+str(finalRunNumber)+"_particles.h5")
        os.system("mv run_"+runNumber+"/E320_profile_Iteration"+runNumber+"_electron_energy.dat run_"+runNumber+"/E320_profile_Iteration"+str(finalRunNumber)+"_electron_energy.dat")
        os.system("mv run_"+runNumber+"/E320_profile_Iteration"+runNumber+"_photon_energy.dat run_"+runNumber+"/E320_profile_Iteration"+str(finalRunNumber)+"_photon_energy.dat")
        os.system("mv run_"+runNumber+" run_"+str(finalRunNumber))
    except:
        print("!!!!!! something wrong on run_",runNumber)


