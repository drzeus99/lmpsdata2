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

# Read in the alumina nanoparticle
f=open('alumina.pmma85','r')
nanoparticle=[]
for line in f:
	row=line.split()
	nanoparticle.append(row)

# Read in the polymer datafile
data=lmpsdata.Lmpsdata('full', 'pmma85data.finaleq3')

# Add in the mass information for the atom type 7, 8, and 9
# 7 is aluminum cation and 8 is oxgen anion and 9 is the surface aluminum cation
massinfo=[['7','26.981539'],['8','15.9994']] #this is not working
data.add_data(massinfo,'Masses')

#print data.masses

# Add in the alumina nanopartice
data.add_atoms(nanoparticle)

# Delete the data for the velocities and pair coefs
data.delete_body_data('Velocities')
data.delete_body_data('Pair Coeffs')

# Delete Velocities and Pair Coeffs from the keywords
data.body_keywords.remove('Velocities')
data.body_keywords.remove('Pair Coeffs')

# Write the defnsity calculations to the file testden.txt
r,rho=lmpsdata.Density.shells(data,.5,0,32.5)
plot(r,rho)
xlabel('distance (angstrom)')
ylabel('density (amu/angstrom^3)')
#legend(loc=1)
show()


# Write the new nanocomposite into a new datafile
data.write('pmma85_nano_composite_data.initial')
