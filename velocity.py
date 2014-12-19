# -*- coding: utf-8 -*-

class Velocity(object):
    """stores, reads and writes the different types of velocities in
    LAMMPS. Current valid types are: angle, atomic, bond,
    charge, colloid, full, and molecular. If your type is not listed 
    here you can add the functionality to this class easily."""
    def __init__(self, atom_style):
        """initializes a LAMMPS velocity and sets the atom_style to be used.
        some of the information stored in this class has been commented out
        because they are not used by the currently implemented atom_styles"""
        self.atom_style = atom_style        
        self.translate = []
        #types of velocities below are not implemented since they are currently
        #not supported in atom.py
        #self.angular = [] #angular momentum or angular velocity
        #self.electron = float #electron radial velocity
        
    def read(self, input, index):
        """converts a list of strings into the information stored in Velocity
        input is a list of strings
        index is the list index to begin at"""
        if self.atom_style == "angle" or self.atom_style == "atomic" or\
        self.atom_style == "bond" or self.atom_style == "charge" or\
        self.atom_style == "colloid" or self.atom_style == "full" or\
        self.atom_style == "molecular":
            index = self._read_translate(input, index)
        else: #error condition
            raise RuntimeError("the {0} atom_style is either invalid or has not been implemented"\
            .format(self.atom_style))
        #check if index now matches len of input
        if (index != len(input)):
            raise IOError("input is too long to be a velocity with the {0} atom_style"\
            .format(self.atom_style))
    
    def _read_translate(self, input, index):
        """converts a list of strings into translate"""
        for i in range(3):
           self.translate.append(float(input[index]))
           index += 1
        return index
          
    def write(self):
        """converts the information stored in velocity to a string.
        uses atom_style to produce the correct string.
        returns the string."""
        if self.atom_style == "angle" or self.atom_style == "atomic" or\
        self.atom_style == "bond" or self.atom_style == "charge" or\
        self.atom_style == "colloid" or self.atom_style == "full" or\
        self.atom_style == "molecular":
            return "{0}".format(self._write_translate())
        else: #error condition
            raise RuntimeError("the {0} atom_style is either invalid or has not been implemented"\
            .format(self.atom_style))
    
    def _write_translate(self):
        """converts translate into a string seperated by spaces"""
        #line below is written this way to ensure that self.atom
        #is at least a length of 3 when being written.
        return " ".join(str(self.translate[i]) for i in range(3))
    
    def _check_format(self, atom_style):
        """check if the format of the velocity object's atom style and the inputed
        atom style are compatible. if they are compatible return true. otherwise
        return false."""
        format1, format2 = self._return_format(atom_style)
        return format1 == format2
            
    def _return_format(self, atom_style):
        """returns two integers corresponding to the velocity object's atom style
        and the inputed atom style. if the numbers are the same the atom styles
        are compatible."""
        formats = {"angle": 1, "atomic": 1, "bond": 1, "charge": 1,\
        "colloid":1, "full": 1, "molecular":1}
        return formats[self.atom_style], formats[atom_style]
        
#testing = Velocity("atomic")
#testing.read(["4.2", "3.7", "2.1"],0)
#print testing.write()
#print testing.translate
#print testing.atom_style