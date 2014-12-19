# -*- coding: utf-8 -*-

from coeffs import Coeffs

class Coeffs_bond(Coeffs):
    """stores, reads, and writes the coeffs for bond.
    additionally, can be used to match an bond_type object to a bond object.
    the matching functionality will be implemented later"""
    
    def __init(self):
        """initializes the parent class Coeffs"""
        super(Coeffs_bond, self).__init__()
        
#g = Coeffs_bond()
#g.read(["1", "10", "2"], 0)
#print g.write()