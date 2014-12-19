# -*- coding: utf-8 -*-

from coeffs import Coeffs

class Coeffs_angle(Coeffs):
    """stores, reads, and writes the coeffs for angle.
    additionally, can be used to match an angle_type object to an angle object.
    the matching functionality will be implemented later"""
    
    def __init__(self):
        """initializes the parent class Coeffs"""
        super(Coeffs_angle, self).__init__()
        
#q = Coeffs_angle()
#q.read(["1", '2', '3'], 0)
#print q.write()
#print q.info
#
#print isinstance(q, Coeffs_angle)
#print isinstance(q, Coeffs)