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