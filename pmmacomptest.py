#
#  npinsert.py
#  For inserting a nanoparticle 
#
#  Created by Zachary Kraus on 6/21/12.
#  Copyright (c) 2012 Georgia Tech. All rights reserved.
#
from sys import path
path.append('/Users/zacharykraus/lmpsdata2')
del path[0]
import lmpsdata
from pylab import *
def converttodata(restartfile,datafile):
	import os
	os.system('../../lammps/tools/restart2data ' + restartfile + ' ' + datafile)

# Convert restart file to datafile
converttodata('pmma85composite.initeq', 'pmma85compositedata.initeq')


# Read in the polymer datafile
data=lmpsdata.Lmpsdata('full', 'pmma85compositedata.initeq')

# Write the density calculations to the file testden.txt
r,rho=lmpsdata.Density.shells(data,.5,0,32.5)
plot(r,rho)
xlabel('distance (angstrom)')
ylabel('density (amu/angstrom^3)')
#xticks(arange(0,21,1))
#legend(loc=1)

#need to test nanoparticle density method
figure()
test_particle = lmpsdata.Nanoparticle(data, 'extract', 'sphere', [0.0, 0.0, 0.0], 15, 1.94, ['type'], [8])
#for i in test_particle.surface:
#	print i , test_particle.atoms[i].write()
#f = open('test_particle.txt', 'w')
#for i, val in test_particle.atoms.items():
#	f.write('{0} {1}\n'.format(i, val.write()))
#print test_particle.shape
#print dir(test_particle)
r_new, r_rho = lmpsdata.Density.nanoparticle(test_particle, data, .5, 0, 17.5)
plot(r_new, r_rho)
lmpsdata.Density.write(r_new, r_rho, 'particle_test.txt')
xlabel('distance (angstrom)')
ylabel('density (amu/angstrom^3)')
show()



# write out an xyz file
#data.createxyz('pmma85composite_initeq.xyz')

# split into molecules and write out xyz files
#pmma=lmpsdata.molecules(data,1,4,'atom')
#for i in range(len(pmma)):
#	pmma[i].createxyz('pmma80_molecule'+str(i)+'_initeq.xyz',data)
#alumina=lmpsdata.molecules(data,5,5,'atom')
#alumina[0].createxyz('alumina_initeq.xyz',data)
