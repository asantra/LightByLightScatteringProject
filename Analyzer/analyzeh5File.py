import h5py
import matplotlib.pyplot as plt
import numpy as np
import sys, os, time

file = h5py.File(sys.argv[1], 'r')

print("file keys: ", list(file.keys()))

print("config list: ", list(file['config'].keys()))
print("config/laser: ",list(file['config/laser'].keys()))
print("config/laser/a0: ",file['config/laser']["a0"][()])
print("config/control: ",list(file['config/control'].keys()))
print("config/beam: ",list(file['config/beam'].keys()))
#print("config/input-file: ",list(file['config/input-file'].keys()))
print("config/output: ",list(file['config/output'].keys()))
print("config/unit: ",list(file['config/unit'].keys()))
print("final-state: ",list(file['final-state'].keys()))
print("final-state positron: ",list(file['final-state/positron']["a0_at_creation"]))
print("intermediate-state: ", list(file['intermediate-state/photon']['a0_at_creation']))
print("positron: ", len(file['final-state/positron']['momentum'][()]))
print("electron: ", len(file['final-state/electron']['momentum'][()]))
print("photon: ", len(file['final-state/photon']['momentum'][()]))
print(file['config/unit']['momentum'][()])
print(file['config/unit']['position'][()])
exit()

print("config/laser keys: ")
for key in list(file['config/laser'].keys()):
    val = file['config/laser'][key][()]
    
    print('{:<15} => {}'.format(key, val))
    
print("final-state/electron keys: ")
for key in list(file['final-state/electron'].keys()):
    val = file['final-state/electron'][key][()]
    
    print('{:<15} => {}'.format(key, val))
    
    for i in range(0,len(val)):
        print(val[i])


pol = file['config/laser/polarization']
print("polarization: ", pol)
print("polarization keys: ", pol[()])
print("polarization metadata: ", pol.dtype.metadata)
#print("polarization: ", pol.value)


print("final-state/positron: ", list(file['final-state/positron']))

x = file['final-state/positron/position'][()]
print("final-state/positron/position: ", x)

id = file['final-state/positron/id'][()]

print("final-state/positron/id: ",id)

p = file['final-state/photon/momentum'][()]

energies = p[:,0]
print("final-state/photon/momentum energies: ", energies)

