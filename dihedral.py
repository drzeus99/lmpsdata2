# -*- coding: utf-8 -*-

class Dihedral(object):
    """stores, reads and writes a LAMMPS dihedral"""
    def __init__(self):
        """initializes a LAMMPS bond"""
        self.type = int #the bond type 
        self.atom = [] #the atoms connecting the bond
        
    def read(self, input, index):
        """converts a list of strings into the information stored in Dihedral 
        input is a list of strings
        index is the list index to begin at"""
        index = self._read_type(input, index)
        index = self._read_atom(input, index)
        #check if index now matches len of input
        if (index != len(input)):
            raise IOError("input is too long to be a dihedral")
        
    def _read_type(self, input, index):
        """converts a list of strings into type"""
        self.type = int(input[index])
        index += 1
        return index
    
    def _read_atom(self, input, index):
        """converts a list of strings into atom"""
        if (len(self.atom) != 0): self.atom = [] #reset atom to an empty list
        for i in range(4):
            self.atom.append(int(input[index]))
            index += 1
        return index
        
    def write(self):
        """converts the information stored in Dihedral to a string
        returns the string"""
        return "{0} {1}".format(self.type, self._write_atom())
    
    def _write_atom(self):
        """converts atom into a string seperated by spaces"""
        #line below is written this way to ensure that self.atom
        #is at least a length of 4 when being written.
        return " ".join(str(self.atom[i]) for i in range(4))
        
#b = Dihedral()
#b.read(["1", "2", "3", "4", "5", "6"], 1)
#print b.write()
#print b.type
#print b.atom