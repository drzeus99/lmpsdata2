# -*- coding: utf-8 -*-

class Coeffs(object):
    """Stores reads and writes the coefficients"""
    def __init__(self):
        """initializes LAMMPS coefficients"""
        self.info = []
    
    def read(self, input, index):
        """copies the list of strings into the class
        input is a list of strings
        index is the starting index for copying"""
        for i in range(index, len(input)):
            self.info.append(input[i])
        
    def write(self):
        """converts the list of strings stored in this class into one string
        returns the string"""
        return "{0}".format(self._write_info())
        
    def _write_info(self):
        """converts info into a string seperated by spaces"""
        return " ".join(i for i in self.info)
        
#a = Coeffs()
#a.read(["1", '2', '3'], 0)
#print a.write()
#print a.info