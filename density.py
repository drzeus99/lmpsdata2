# -*- coding: utf-8 -*-

import space

class Density(object):
    """contains methods for calculating the density from information stored in
    the body_data class and additionally in the header_data class if needed.
    also contains a method to write the calculated values to a file"""

    @staticmethod
    def shell(data, ringsize, init, final):
        """calculates the density by creating spherical shells from the initial
        radius to the final radius. the spherical shell's thickness is defined 
        by ringsize. data must either be a body_data class or a class that 
        inherited body_data. calculates the mass of particles within each
        spherical shell. calculates the volume of each spherical shell.
        calculates the density in each spherical shell. shells are centered 
        around the origin of the simulation box."""
        rho = []
        r = [init] #initial radius to examine
        radius = init + ringsize
        while radius < final: #finding the rest of the radii to examine
            r.append(radius)
            radius += ringsize    
        magnitudes = space.magnitudes(data.atoms)
        keys = data.atoms.keys()
        pairs = zip(magnitudes, keys)
        for radius in r:
            volume = 4.0/3.0 * 3.1416 * ((radius + ringsize)**3 - radius**3)
            mass = 0.0
            for pair in pairs:
              if pair[0] > radius and pair[0] < (radius + ringsize):
                  mass += data.masses[pair[1]].value
            rho.append(mass/volume)
        return r, rho       
                    
    @staticmethod
    def write(r, rho, file):
        """writes the information returned from density calculation methods to 
        a file. r is the position information. rho is the density information.
        file is the location to write the informatin stored in r and rho to."""
        f = open(file, 'w')
        for i in range(len(r)):
            f.write('{0} {1}\n'.format(r[i], rho[i]))
        f.close()