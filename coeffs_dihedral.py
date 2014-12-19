# -*- coding: utf-8 -*-

from coeffs import Coeffs

class Coeffs_dihedral(Coeffs):
    """stores, reads, and writes the coeffs for dihedral.
    additionally, can be used to match an dihedral_type object to a dihedral object.
    the matching functionality will be implemented later"""
    
    def __init(self):
        """initializes the parent class Coeffs"""
        super(Coeffs_dihedral, self).__init__()
        
#j= Coeffs_dihedral()
#j.read(["1", '2', '3'], 0)
#print j.write()