# -*- coding: utf-8 -*-

class Atom(object):
    """stores, reads and writes the different types 
    of atom in LAMMPS. Current valid types are: angle, atomic, bond,
    charge, colloid, full, and molecular. If your type is not listed 
    here you can add the functionality to this class easily. Note:
    the current design in this class will not work for hybrid atoms.
    If you need hybrid functionality, you will have to alter this 
    class's design."""
    def __init__(self, atom_style):
        """initializes a LAMMPS atom and sets the atom_style to be used.
        not all of the information stored in this class will be used by
        every atom_style"""
        self.atom_style = atom_style #is a string
        self.type = int #atom-type
        self.molecule = int #molecule-id
        self.position = [] #x y z
        self.charge = float #q
        self.image = [] #image flags
        
    def read(self, input, index):
        """converts a list of strings into the information stored in Atom
        input is a list of strings
        index is the list index to begin at"""
        #read and store information from input for different atom_style
        if self.atom_style == "atomic" or\
        self.atom_style == "colloid":
            index = self._read_type(input, index)
            index = self._read_position(input, index)
        elif self.atom_style == "angle" or\
        self.atom_style == "bond" or\
        self.atom_style == "molecular":
            index = self._read_molecule(input, index)
            index = self._read_type(input, index)
            index = self._read_position(input, index)
        elif self.atom_style == "full":
            index = self._read_molecule(input, index)
            index = self._read_type(input, index)
            index = self._read_charge(input, index)
            index = self._read_position(input, index)
        elif self.atom_style == "charge":
            index = self._read_type(input, index)
            index = self._read_charge(input, index)
            index = self._read_position(input, index)
        else: #error condition
            raise RuntimeError("the {0} atom_style is either invalid or has not been implemented"\
            .format(self.atom_style))
        #read and store image flags from input for all atom_style         
        index = self._read_image(input,index)    
        #check if index now matches len of input
        if (index != len(input)):
            raise IOError("input is too long to be an atom with the {0} atom_style"\
            .format(self.atom_style))
                
    def _read_type(self, input, index):
        """converts a list of strings into type"""
        self.type = int(input[index])
        index += 1
        return index
        
    def _read_molecule(self, input, index):
        """converts a list of strings into molecule"""
        self.molecule = int(input[index])
        index += 1
        return index
        
    def _read_position(self, input, index):
        """converts a list of strings into position"""
        if (len(self.position) != 0): self.position = [] #resets position to an empty list
        for i in range(3):
            self.position.append(float(input[index]))
            index += 1
        return index
        
    def _read_charge(self, input, index):
        """converts a list of strings into charge"""
        self.charge = float(input[index])
        index += 1
        return index
        
    def _read_image(self, input, index):
        """converts a list of strings into image"""
        if (len(self.image) != 0): self.image = [] #resets image to an empty list
        for i in range(3):
            try:
                self.image.append(int(input[index]))
                index += 1
            except IndexError:
                return index
        return index
        
    def write(self):
        """converts the information stored in atom to a string.
        uses atom_style to produce the correct string.
        returns the string.
        if the string contains <type 'int'> or <type 'float'>,
        either atom_style has accidentally been changed or 
        a member used by atom_style was not assigned in the read method of this
        class."""
        #writes information to a string for different atom_style
        if self.atom_style == "atomic" or\
        self.atom_style == "colloid":
            return "{0} {1} {2}".format(self.type, \
            self._write_position(), self._write_image())
        elif self.atom_style == "angle" or\
        self.atom_style == "bond" or\
        self.atom_style == "molecular":
            return "{0} {1} {2} {3}".format(self.molecule, \
            self.type, self._write_position(), self._write_image())
        elif self.atom_style == "full":
            return "{0} {1} {2} {3} {4}".format(self.molecule, \
            self.type, self.charge, self._write_position(), self._write_image())
        elif self.atom_style == "charge":
            return "{0} {1} {2} {3}".format(self.type, \
            self.charge, self._write_position(), self._write_image())
        else: #error condition
            raise RuntimeError("the {0} atom_style is either invalid or has not been implemented"\
            .format(self.atom_style))
             
    def _write_position(self):
        """converts position into a string seperated by spaces"""
        #line below is written this way to ensure that self.position
        #is at least a length of 3 when being written.
        return " ".join(str(self.position[i]) for i in range(3))
        
    def _write_image(self):
        """converts image into a string seperated by spaces"""
        return " ".join(str(i) for i in self.image)
        
    def _check_format(self, atom_style):
        """check if the format of the atom object's atom style and the inputed
        atom style are compatible. if they are compatible return true. otherwise
        return false."""
        format1, format2 = self._return_format(atom_style)
        return format1 == format2
        
    def _return_format(self, atom_style):
        """returns two integers corresponding to the atom object's atom style
        and the inputed atom style. if the numbers are the same the atom styles
        are compatible."""
        formats = {"atomic": 1, "colloid": 1, "angle": 2, "bond": 2,\
        "molecular": 2, "full": 3, "charge": 4}
        return formats[self.atom_style], formats[atom_style]
    
#a = Atom("atomic")
#a.read(["0", "1", "2.1", "3.9"], 0)
#print a.atom_style
#print a.type
#print a.molecule        
#print a.position    
#print a.charge
#print a.image
#print a.write()
#
#b = Atom("molecular")
#b.read(["0", "1", "3","2.1", "3.9", "5", "2", "6"], 0)
#print b.atom_style
#print b.type
#print b.molecule        
#print b.position    
#print b.charge
#print b.image
#print b.write()
#
#c = Atom("full")
#c.read(["0", "1", "3","2", "3.9", "4.0", "5.3", "3"], 1)
#print c.atom_style
#print c.type
#print c.molecule        
#print c.position    
#print c.charge
#print c.image
#print c.write()
#
#d = Atom("charge")
#d.read(["0", "1", "3","2", "3.9", "5", "2"], 0)
#print d.atom_style
#print d.type
#print d.molecule        
#print d.position    
#print d.charge
#print d.image
#print d.write()
