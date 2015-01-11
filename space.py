# -*- coding: utf-8 -*-

import math

def magnitudes(atoms):
    """calculate the magnitudes of a dictionay of atoms and return the results
    as a list."""
    results = []
    for atom in atoms.values:
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