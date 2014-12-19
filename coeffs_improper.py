# -*- coding: utf-8 -*-

from coeffs import Coeffs

class Coeffs_improper(Coeffs):
    """stores, reads, and writes the coeffs for improper.
    additionally, can be used to match an improper_type object to a improper object.
    the matching functionality will be implemented later"""
    
    def __init(self):
        """initializes the parent class Coeffs"""
        super(Coeffs_improper, self).__init__()
        
#j= Coeffs_improper()
#j.read(["1", '2', '3'], 0)
#print j.write()