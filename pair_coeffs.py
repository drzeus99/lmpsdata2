# -*- coding: utf-8 -*-

from coeffs import Coeffs

class Pair_coeffs(Coeffs):
    """stores, reads, and writes the coeffs for pair.
    Unlike the other children classes of Coeffs,
    This class will not add any extra behaviour.
    The seperate class is just here to easily identify that the class
    is for pairs of atoms"""
    def __init__(self):
        """initializes parent class Coeffs"""
        super(Pair_coeffs, self).__init__()
        
#q = Pair_coeffs()
#q.read(["1", '2', '3'], 0)
#print q.write()
#print q.info