# -*- coding: utf-8 -*-

import math

def magnitudes(atoms):
    """calculate the magnitudes of a dictionay of atoms and return the results
    as a list."""
    results = []
    for atom in atoms.values():
        results.append(magnitude(atom))
    return results
        
def magnitude(atom):
    """calculate the magnitude of an atom and return the result"""
    result = 0.0
    for coord in atom.position:
        result += pow(coord, 2)
    return math.sqrt(result)
    
def distance(atom_1, atom_2):
    """calculate the distance between atom_1 and atom_2 and return the result"""
    result = 0.0
    for i in range(3):
        result += pow(atom_1.position[i] - atom_2.position[i], 2)
    return math.sqrt(result)

def position_times_value(atom, value):
    """write in later"""
    from copy import deepcopy
    result = deepcopy(atom)
    for i in range(3):
        result.position[i] = atom.position[i] * value
    return result

def dot(atom_1, atom_2):
    """write in later"""
    result = 0.0
    for i in range(3):
        result += atom_1.position[i] * atom_2.position[i]
    return result
    
def distance_from_plane(atom, normal_to_plane, normal_magnitude, plane_magnitude):
    """Write in later"""
    result = dot(atom, normal_to_plane) + plane_magnitude
    result /= normal_magnitude
    return result
    
def spherical_to_cartesian(r, theta, phi):
    """Add later"""
    cartesian = []
    from math import cos, sin
    cartesian.append(r * cos(theta) * sin(phi))
    cartesian.append(r * sin(theta) * sin(phi))
    cartesian.append(r * cos(phi))
    return cartesian
    
def add_vectors(vector1, vector2):#note am not using atom math here
    """Add later"""
    if len(vector1) != len(vector2):
        raise SystemError("add_vector method is not possible because the vectors are not the same size")
    result = []
    for i in range(len(vector1)):
        result.append(vector1[i] + vector2[i])
    return result
    
class Sphere(object):
    """Write Later"""
    def __init__(self, center, radius):
        """Write Later"""
        from atom import Atom
        self._center = Atom('atomic')
        self._center.position = center
        self._radius = radius
    
    def nearest_neighbor(self, atom, cutoff_distance):
        """Write Later"""
        distance_from_surface = abs(self._radius - distance(atom, self._center))
        if distance_from_surface <= cutoff_distance:
            return True
        else:
            return False
    
    def in_shape(self, atom):
        """Write Later"""
        distance_from_center = distance(atom, self._center)
        if distance_from_center <= self._radius:
            return True
        else:
            return False
            
    def random_position_on_surface(self, cutoff_distance):
        """Add later"""
        import random
        import math
        #use sphherical coordinates
        r = random.uniform(self._radius - cutoff_distance, self._radius)
        theta = random.uniform(0, 2*math.pi)
        phi = random.uniform(0, math.pi)
        surface_vector = spherical_to_cartesian(r, theta, phi)
        position = add_vectors(self._center.position, surface_vector)
        #return position as a list of strings
        for i in range(len(position)):
            position[i] = str(position[i])
        return position
  
class Cube(object):
    def __init__(self, center, radius, rotation=None): #figure out variables
        """write later"""
        from atom import Atom
        self._center = Atom("atomic")
        self._center.position = center
        self._radius = radius
        self._rotation = rotation
        unit_axes = self._init_unit_axes()
        if rotation != None:
            raise ValueError("Rotation for the cube is not yet implemented")
        #list of vectors perpenedicular to the three planes parallel to the cubes faces
        self._normal_to_plane = []
        for unit_vector in unit_axes:
            self._normal_to_plane.append(position_times_value(unit_vector, self._radius))
        self._plane_magnitude = []
        self._normal_magnitude = []
        for vector in self._normal_to_plane:
            self._plane_magnitude.append(-dot(vector, self._center))
            self._normal_magnitude.append(magnitude(vector))
 
    def nearest_neighbor(self, atom, cutoff_distance):
        """Write later"""
        #the adjustments in radius in this method will not cause the distance_from_plane
        #function to give wrong values. Since the unit vector and point on the plane dont
        #change the distance will still be the same.
        #the change is to if the point is a slightly larger size cube which is 
        #equal to radius + cutoff_distance. If the point is in this cube and 
        #than meets the second nearest neighbor test. It is a real nearest neighbor.
        #if only the second test was done, this method would report false results.
        self._adjust_radius(cutoff_distance)
        if self.in_shape(atom):
            self._adjust_radius(-cutoff_distance)
            for i in range(3):
                distance_from_surface = abs(abs(distance_from_plane(atom, self._normal_to_plane[i],\
                self._normal_magnitude[i], self._plane_magnitude[i])) - self._radius)
                if distance_from_surface <= cutoff_distance:
                    return True
            return False
        self._adjust_radius(-cutoff_distance)
        return False
    
    def in_shape(self, atom):
        """Write Later"""
        for i in range(3):
            if abs(distance_from_plane(atom, self._normal_to_plane[i],\
            self._normal_magnitude[i], self._plane_magnitude[i])) > self._radius:
                return False
        return True
        
    def random_position_on_surface(self, cutoff_distance):
        """Add later"""
        #more than likely will use plane math to find a random position
        import random
        choosen_plane = random.randint(1, 3)
        in_plane = []
        if choosen_plane == 1:
            in_plane.append(2)
            in_plane.append(3)
        elif choosen_plane == 2:
            in_plane.append(1)
            in_plane.append(3)
        else:
            in_plane.append(1)
            in_plane.append(2)
        sign = random.randint(1,2)
        distance = random.uniform(self._radius - cutoff_distance, self._radius)
        if sign == 2:
            distance = -distance
        scaled_distance = distance / self._radius
        atom_in_plane = position_times_value(self._normal_to_plane[choosen_plane], scaled_distance)
        atom_in_plane.position = add_vectors(atom_in_plane.position, self._center)
        for index in in_plane:
            distance = random.uniform(-self._radius, self._radius)
            scaled_distance = distance / self._radius
            direction = position_times_value(self._normal_to_plane[index], scaled_distance)
            atom_in_plane.position = add_vectors(atom_in_plane.position, direction.position)
        position = []
        for i in atom_in_plane.position:
            position.append(str(atom_in_plane.position[i]))
        return position
    
    def _init_unit_axes(self):
        """Write later"""
        from atom import Atom
        unit_axes = [Atom("atomic"), Atom("atomic"), Atom("atomic")]
        unit_axes[0].position = [1, 0, 0]
        unit_axes[1].position = [0, 1, 0]
        unit_axes[2].position = [0, 0, 1]
        return unit_axes
        
    def _adjust_radius(self, amount):
        """Write later"""
        self._radius += amount
    
#test_sphere = Sphere([0, 0, 0], 4)
#from atom import Atom
#test_atom = Atom("atomic")
#for x in range(-1, 4):
#    for y in range(-1, 4):
#        for z in range(-1, 4):
#            test_atom.position = [x, y, z]
#            test = test_sphere.nearest_neighbor(test_atom, 1)
#            if test == True:
#                print "for the position ", test_atom._write_position(), "is a nearest neighbor. the distance is", magnitude(test_atom)
#            else:
#                print "for the position ", test_atom._write_position(), "is not a nearest neighbor. the distance is", magnitude(test_atom)
#
#test_cube = Cube([0, 0, 0], 4)
#for x in range(-5, 1):
#    for y in range(-5, 1):
#        for z in range(-5, 1):
#            test_atom.position = [x, y, z]
#            test = test_cube.in_shape(test_atom)
#            if test == True:
#                print "for the position ", test_atom._write_position(), "is in the shape."
#            else:
#                print "for the position ", test_atom._write_position(), "is not in the shape."