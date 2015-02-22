# -*- coding: utf-8 -*-

import space

class Density(object):
    """contains methods for calculating the density from information stored in
    the body_data class and additionally in the header_data class if needed.
    also contains a method to write the calculated values to a file"""

    @staticmethod
    def shells(data, ringsize, init, final):
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
        from math import pi
        for radius in r:
            volume = 4.0/3.0 * pi * ((radius + ringsize)**3 - radius**3)
            mass = 0.0
            for pair in pairs:
              if pair[0] > radius and pair[0] < (radius + ringsize):
                  mass += data.masses[data.atoms[pair[1]].type].value
            rho.append(mass/volume)
        return r, rho
        
    @staticmethod
    def cubes(data, edge_length, init, final, origin = [0, 0 , 0]):
        """write later"""
        #initial cube centered at origin
        if not isinstance(init, list):
            raise ValueError("init and final are required to be lists of length 3")
        if not isinstance(final, list):
            raise ValueError("init and final are required to be lists of length 3")
        for i in range(3):
            if init[i] > origin[i] or final[i] < origin[i]:
                raise ValueError("init needs to be less than the origin and final needs to be greater than the origin")
        positions = Density._build_cubic_positions(edge_length, init, final, origin)
        #make cubes around the positions
        cubes = []
        from space import Cube
        size = edge_length / 2.0
        volume = edge_length**3
        for position in positions:
            cubes.append(Cube(position, size))
        #extract keys from data
        keys = set(data.atoms.keys())
        rho = []
        #calculate the density in each cube
        #delete keys as they are used in each cube
        for cube in cubes:
            deleted_keys = []
            mass = 0.0
            for key in keys:
                if cube.in_shape(data.atoms[key]):
                    deleted_keys.append(key)
                    mass += data.masses[data.atoms[key].type].value
            rho.append(mass/volume)
            for key in deleted_keys:
                keys.remove(key)
        return positions, rho
                    
    @staticmethod #gotten rid of all of the excessive errors and unused code
    #now need to include origin parameter into the code
    def _build_cubic_positions(edge_length, init, final, origin):
        """Write later"""
       #build up list of x,y,z positions
        xyz = [[], [], []] # [list of x, list of y, list of z]
        for i in range(3):
            xyz[i].append(origin[i])
            value = origin[i] + edge_length
            while value < final[i]:
                xyz[i].append(value)
                value += edge_length
            value = origin[i] -edge_length
            while value > init[i]:
                xyz[i].append(value)
                value -= edge_length
        #convert xyz to a list of positions
        positions = []
        for i in range(len(xyz[0])):
            for j in range(len(xyz[1])):
                for k in range(len(xyz[2])):
                    positions.append([xyz[0][i], xyz[1][j], xyz[2][k]])
        return positions
                    
    @staticmethod #have bug in here am changing radius in code
    def nanoparticle(particle, data, spacing, init, final):
        """Write Later"""
        keys = set(data.atoms.keys())
        from space import Sphere, Cube
        if isinstance(particle.shape, Sphere):
            shapetype = 'sphere'
            center = particle.shape._center.position
            radius = particle.shape._radius
            rotation = None
        elif isinstance(particle.shape, Cube):
            shapetype = 'cube'
            center = particle.shape._center.position
            radius = particle.shape._radius
            rotation = particle.shape._rotation 
        inner_shape = Density._shape_factory(shapetype, center, radius + init, rotation)        
        outer_shape = Density._shape_factory(shapetype, center, radius + final, rotation)
        # find keys to remove that will never need their density calculated
        deleted_keys = []
        for key in keys:
            if inner_shape.in_shape(data.atoms[key]):
                deleted_keys.append(key)
            elif not outer_shape.in_shape(data.atoms[key]):
                deleted_keys.append(key)
        for key in deleted_keys:
            keys.remove(key)
        rho = []
        r = [init] #initial radius to examine
        #changing variable radius
        _radius = init + spacing
        while _radius < final: #finding the rest of the radii to examine
            r.append(_radius)
            _radius += spacing
        #calculate the density in each shape
        #delete keys as they are used in each cube
        for distance in r:
            deleted_keys = []
            mass = 0.0
            shape = Density._shape_factory(shapetype, center, radius + distance + spacing, rotation)
            for key in keys:
                if shape.in_shape(data.atoms[key]):
                    deleted_keys.append(key)
                    mass += data.masses[data.atoms[key].type].value
            #need to calculate volume here
            volume = Density._volume_for_nanoparticle_shell(shapetype, radius + distance, spacing)
            rho.append(mass/volume)
            for key in deleted_keys:
                keys.remove(key)
        return r, rho
     
    @staticmethod
    def _volume_for_nanoparticle_shell(shapetype, distance, spacing):
        """Write Later"""
        from math import pi
        if shapetype == 'sphere':
            return 4.0/3.0 * pi * ((distance + spacing)**3 - distance**3)
        elif shapetype == 'cube':
            return (distance + spacing)**3 - distance**3
     
    @staticmethod
    def _shape_factory(shapetype, center, radius, rotation):
        from space import Sphere, Cube
        if shapetype == 'sphere':
            return Sphere(center, radius)
        elif shapetype == 'cube':
            return Cube(center, radius, rotation)
           
    @staticmethod
    def write(r, rho, file):
        """writes the information returned from density calculation methods to 
        a file. r is the position information. rho is the density information.
        file is the location to write the informatin stored in r and rho to."""
        f = open(file, 'w')
        for i in range(len(r)):
            f.write('{0} {1}\n'.format(r[i], rho[i]))
        f.close()