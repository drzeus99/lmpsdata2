# -*- coding: utf-8 -*-

class Mass(object):
    """stores, reads and writes a LAMMPS mass"""

    def __init__(self):
        """initializes a LAMMPS mass"""
        self.value = float #the mass's value
        
    def read(self, input, index):
        """converts a list of strings into the information stored in Mass 
        input is a list of strings
        index is the list index to begin at"""
        index = self._read_value(input, index)
        #check if index now matches len of input
        if (index != len(input)):
            raise IOError("input is too long to be a mass")
        
    def _read_value(self, input, index):
        """converts a list of strings into value"""
        self.value = float(input[index])
        index += 1
        return index
    
    def  write(self):
        """converts the information stored in Mass to a string
        returns the string"""
        return "{0}".format(self.value)
        
    def __eq__(self, other):
        return self.value == other.value
        
#a = Mass()
#a.read(["1", "2", "3"], 2)
#print a.write()