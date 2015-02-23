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
converttodata('pmma85.finaleq3', 'pmma85data.finaleq3')


# Read in the polymer datafile
data=lmpsdata.Lmpsdata('full', 'pmma85data.finaleq3')
#data=lmpsdata.Lmpsdata('data.pmma100','full')

# Write the density calculations to the file testden.txt
r,rho=lmpsdata.Density.shells(data,.5,17.5,31)
lmpsdata.Density.write(r, rho, 'shell_test.txt')
r,rho = lmpsdata.Density.cubes(data, .5 , [18, 18, 18], [31, 31, 31], [22, 22, 22])
lmpsdata.Density.write(r, rho, 'cube_test.txt')
#plot(r,rho)
#xlabel('distance (angstrom)')
#ylabel('density (amu/angstrom^3)')
#xticks(arange(0,21,1))
#legend(loc=1)
#show()

# write out an xyz file
#data.createxyz('pmma85_finaleq.xyz')

# split into molecules and write out xyz files
#pmma=lmpsdata.molecules(data,1,22,'atom')
#for i in range(1,23):
#	pmma[i-1].createxyz('pmma100_molecule_'+str(i)+'.xyz',data)
#for i in range(len(pmma)):
#	pmma[i].createxyz('pmma80_molecule'+str(i)+'_initeq.xyz',data)
#alumina=lmpsdata.molecules(data,5,5,'atom')
#alumina[0].createxyz('alumina_initeq.xyz',data)
