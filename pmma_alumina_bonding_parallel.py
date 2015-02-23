# need to edit this one and pmma85 version of this as well. Need to make charges are correct for added atoms.
#  pmma_alumina_bonding.py
#   
#
#  Created by Zachary Kraus on 6/21/12.
#  Copyright (c) 2012 Georgia Tech. All rights reserved.
#
from sys import path
path.append('/Users/zacharykraus/lmpsdata2')
del path[0]
import lmpsdata, copy
data = lmpsdata.Lmpsdata('full', 'pmma90compositedata.initeq')

#copies pmma80compositedata.initeq to a new folder
directory='./bulk/'
data.write(directory+'pmma90_composite_data.initial', 0)

#add mass data for the bonded carbonyl type
massinfo=[['9','15.9994']]
data.add_data(massinfo,'Masses')

from multiprocessing import Pool
p = Pool(4)

#seperate nanocomposite data into polymer and nanoparticle portion
polymer = []
for i in range(1,31):
	polymer.append(p.apply_async(lmpsdata.Molecule, (data, i,)))
for i in range(len(polymer)):
	print 'creating molecule ', i
	polymer[i] = polymer[i].get()
	print 'finished producing molecule ', i

print 'creating nanoparticle'
nanoparticle = lmpsdata.Molecule(data, 65)
print 'finished with nanoparticle'

#add surface to nanoparticle using Nanoparticle class
particle = lmpsdata.Nanoparticle(nanoparticle, 'input', 'sphere', [0.0, 0.0, 0.0], 15, 1.94, ['type'], [8])
print 'finished inputing the nanoparticle and producing a surface'

#setup copies of molecules for different reaction processes
polymer_crosslink = copy.deepcopy(polymer) #crosslink case is 2 bonds formed
polymer_weakbond = copy.deepcopy(polymer)  #weakbond case is 4 bonds formed
polymer_strongbond = copy.deepcopy(polymer) #strongbonds case is 8 bonds formed

#setup copies of particle for different reaction processes
particle_crosslink = copy.deepcopy(particle)
particle_weakbond = copy.deepcopy(particle)
particle_strongbond = copy.deepcopy(particle)

#setup different reactors
crosslink_reactors = []
weakbond_reactors = []
strongbond_reactors = []

#insert polymers into appropriate reactor
for i in range(len(polymer)):
	crosslink_reactors.append(lmpsdata.Reactor(polymer_crosslink[i]))
	weakbond_reactors.append(lmpsdata.Reactor(polymer_weakbond[i]))
	strongbond_reactors.append(lmpsdata.Reactor(polymer_strongbond[i]))

#find possible bonding between crosslink(polymer) and surface_crosslink
bondinglen=0
for reactor in crosslink_reactors:
	reactor.find_particle_bonding_locations(particle_crosslink, 'type', 6, 3.2, 2)
	if len(reactor._particle_bonding_information) != int(len(reactor._particle_bonding_information)/2.0)*2:
		i = len(reactor._particle_bonding_information) - 1
		del reactor._particle_bonding_information[i]
	print 'the length of the bonding information is ', len(reactor._particle_bonding_information)
	bondinglen += len(reactor._particle_bonding_information)
bondinglen = bondinglen/float(len(crosslink_reactors))

#Bond crosslink(polymer) to particle_crosslink
count=1
for reactor in crosslink_reactors:
	print 'the bonding iteration is', count
	reactor.bond_to_ceramic_particle(particle_crosslink, [['type', 9], ['charge', -.7825]], [['type', 1]])
	for j in range(len(reactor._particle_bonding_information)/2):
		print 'adding atom', j
		particle_crosslink.add_atom(['65', '8', '-.945'])
	count += 1

# join molecules to data
data.join(polymer_crosslink)

# add in the crosslinked nanoparticle to data_crosslink
data.add_atoms(particle_crosslink.atoms) #cannot use add_body_data since velocity structure doesn't include the added atoms from the reaction

# delete the data for the velocities and pair coeffs from data_crosslink
data.delete_body_data('Velocities')

# delete the Velocities and Pair Coeffs from the keywords from data_crosslink
data.body_keywords.remove('Velocities')

# write the crosslink bonded nanocomposite into a new data file
directory='./crosslink/'
data.write(directory+'pmma90_composite_data.initial','crosslink test')
# write the crosslink bondinglen into a file in the crosslink directory
f=open(directory+'bondinglen.info','w')
f.write('{0}'.format(bondinglen))
f.close()

#find possible bonding between weakbond(polymer) and particle_weakbond
bondinglen=0
for reactor in weakbond_reactors:
	reactor.find_particle_bonding_locations(particle_weakbond, 'type', 6, 3.2, 4)
	if len(reactor._particle_bonding_information) != int(len(reactor._particle_bonding_information)/2.0)*2:
		i = len(reactor._particle_bonding_information) - 1
		del reactor._particle_bonding_information[i]
	print 'the length of the bonding information is', len(reactor._particle_bonding_information)
	print 'the final bonding information is', reactor._particle_bonding_information
	bondinglen += len(reactor._particle_bonding_information)
bondinglen = bondinglen/float(len(weakbond_reactors))

#Bond weakbond(polymer) to particle_weakbond
count=1
for reactor in weakbond_reactors:
	print 'the bonding iteration is', count
	reactor.bond_to_ceramic_particle(particle_weakbond, [['type', 9], ['charge', -.7825]], [['type', 1]])
	for j in range(len(reactor._particle_bonding_information)/2):
		print 'adding atom', j
		particle_weakbond.add_atom(['65', '8', '-.945'])
	count+=1

# join molecules to data
data.join(polymer_weakbond)

# add in the weakbonded nanoparticle to data_weakbond
data.add_atoms(particle_weakbond.atoms)

# delete the data for the velocities and pair coeffs from data_weakbond
data.delete_body_data('Velocities')

# delete the Velocities and Pair Coeffs from the keywords from data_weakbond
data.body_keywords.remove('Velocities')

# write the weakbond bonded nanocomposite into a new data file
directory='./weakbond/'
data.write(directory+'pmma90_composite_data.initial', 'weakbond test')
# write the weakbond bondinglen into a file in the crosslink directory
f=open(directory+'bondinglen.info','w')
f.write('{0}'.format(bondinglen))
f.close()

#find possible bonding between strongbond(polymer) and particle_strongbond
bondinglen=0
for reactor in strongbond_reactors:
	reactor.find_particle_bonding_locations(particle_strongbond, 'type', 6, 3.2, 8)
	if len(reactor._particle_bonding_information) != int(len(reactor._particle_bonding_information)/2.0)*2:
		i=len(reactor._particle_bonding_information) - 1
		del reactor._particle_bonding_information[i]
	print 'the lenght of the bonding information is', len(reactor._particle_bonding_information)
	print 'the final bonding information is', reactor._particle_bonding_information
	bondinglen += len(reactor._particle_bonding_information)
bondinglen = bondinglen/float(len(strongbond_reactors))
print 'the bonding len is ', bondinglen

#Bond strongbond(polymer) to particle_strongbond
count=1
for reactor in strongbond_reactors:
	print 'the bonding iteration is', count
	reactor.bond_to_ceramic_particle(particle_strongbond, [['type', 9], ['charge', -.7825]], [['type', 1]])
	for j in range(len(reactor._particle_bonding_information)/2):
		print 'adding atom ', j
		particle_strongbond.add_atom(['65', '8', '-.945'])
	count += 1

# join the molecules to data
data.join(polymer_strongbond)

# add in the strongboded nanoparticle to data_strongbond
data.add_atoms(particle_strongbond.atoms)

# delete the data for the velocities and pair coeffs from data_strongbond
data.delete_body_data('Velocities')

# delete the Velocities and Pair Coeffs from the keywords from data_strongbond
data.body_keywords.remove('Velocities')

# write the strongbond bonded nanocomposite into a new data file
directory='./strongbond/'
data.write(directory+'pmma90_composite_data.initial', 'strongbond test')
# write the strongbond bondinglen into a file in the crosslink directory
f=open(directory+'bondinglen.info','w')
f.write('{0}'.format(bondinglen))
f.close()
