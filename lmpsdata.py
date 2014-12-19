# -*- coding: utf-8 -*-

import body_data
from body_data import Body_data
from header_data import Header_data
from molecule import Molecule
from reactor import Reactor

class Lmpsdata(Body_data, Header_data):
    """stores the information associated with body data and header data keywords.
    allows access to both body data and header data methods. Allows reading and
    writing of LAMMPS data files."""
    def __init__(self, atom_style, file = ''):
        """initializes body_data, and header_data. than attempts to read the file.
        atom_style is a string. file is a string that defaults to empty."""
        Body_data.__init__(self, atom_style)
        Header_data.__init__(self)
        self.body_keywords = []
        self.header_keywords = []
        self.read(file)
        
    def read(self, file):
        """read LAMMPS data file. file is a string. if the string is empty this
        method does nothing. if the string does not match an existing file, 
        an error occurs."""
        if file == '':
            print "No file name is given. Call read method again with a file name."
            return
        f = open(file, 'r')
        f.readline() #skipping comment line
        self._read_header(f)
        self._read_body(f)
        f.close()
        
    def _read_header(self, file):
        """reads the LAMMPS header data from the file. file is a open file object."""
        for line in file:
            row = line.split()
            if len(row) != 0:
                found, keyword = self.check_header_keyword(row)
                if found:
                    self.header_keywords.append(keyword)
                    Header_data.read(self, row, keyword)
                else:
                   if self.check_body_keyword(row)[0]:
                       self.body_keywords.append(self.check_body_keyword(row)[1])
                       return
                   else:
                       raise IOError("text on line contains neither a header keyword nor a body keyword") 
        
    def _read_body(self, file):
        """reads the LAMMPS body data from the file. file is a open file object."""
        blank_line = 0
        keyword = self.body_keywords[0]
        for line in file:
            row = line.split()
            if len(row) == 0:
                blank_line += 1
            else:
                if blank_line > 1:
                   found, keyword = self.check_body_keyword(row)
                   if found:
                       self.body_keywords.append(keyword)
                       blank_line = 0
                   else:
                       raise IOError("text on line contains no body keyword")
                elif keyword == "Pair Coeffs" or keyword == "PairIJ":
                    item = self.create(keyword)
                    item.read(row, 0)
                    self.get_body_data(keyword).append(item)
                else:
                    item = self.create(keyword)
                    item.read(row, 1)
                    self.get_body_data(keyword)[int(row[0])] = item

                
    def write(self, file, comment_line = ''):
        """write LAMMPS data file. file is a string. comment_line is a string that
        is written as the first line of the LAMMPS data file. The comment_line 
        defaults to an empty string."""
        if file == '':
            print "No file name is given. Call write method again with a file name."
            return
        f = open(file, 'w')
        f.write("{0}\n".format(comment_line))
        self._write_header(f)
        f.write("\n")#a space between header and body
        self._write_body(f)
        f.close()
        
    def _write_header(self, file):
        """writes the LAMMPS header data to the file. file is an open file object."""
        for keyword in self.header_keywords:
            file.write("{0}\n".format(Header_data.write(self, keyword)))
    
    def _write_body(self, file):
        """writes the LAMMPS body data to the file. file is an open file object."""
        for keyword in self.body_keywords:
            file.write("{0}\n".format(keyword)) #body keyword
            file.write("\n") #blank line after body keyword
            data = self.get_body_data(keyword)
            try:
                for key, item in data.items():
                    file.write("{0} {1}\n".format(key, item.write()))
            except AttributeError:
                for item in data:
                    file.write("{0}\n".format(item.write()))
            file.write("\n") #blank line after data
            
    #def join(self,): write this later and link to body_data's join method
            
#header data has been completely tested just through reading and writing
#for body data; get_body_data, create, check_body_keyword, _in_body_list, _initialize factory
#_initialize_body_keyword_map have been successfully tested from writing and reading in lmpsdata
#lmpsdata has been completely tested at this point
#read write completely succesful //!also tested pmma85compositedata.initeq to see if velocity works
            #and it does
#test_one = Lmpsdata('full', 'data.pmma100')
#f = open('data.pmma100', 'r')
#comment = f.readline()
#test_one.write('data.test', comment)
#test_two = Lmpsdata('full', 'data.test')
#test_two.write('data.test2', comment)
            
test_one = Lmpsdata('full', 'pmma85compositedata.initeq')
#testing delete_body_data whiich works perfectly
#test_one.delete_body_data("Bonds")
#print test_one.bonds
#test_one.write("testing")

#test for molecule class
#finding atoms, velocities, angles, bonds, dihedrals and impropers with 
#the correct molecule id works perfectly
#copyies coefficients perfectly
#extract method from body_data works perfectly
#find method tested with method set to key for keywords other than "Pair Coeffs" or "PairIJ" 
test_molecule = Molecule(test_one, 1)
#print test_molecule.bonds
#for key, atom in test_molecule.impropers.items():
#   print key, atom.write()

#find method with method set to "dict" successful
#type_6 = test_molecule.find("Atoms", "type", 6, "dict")
#for key, value in type_6.items():
#    print key, value.write()
    
##find method for pair coefficients successful
#type_2 = test_molecule.find("Pair Coeffs", "info", "2", "dict")
#print type_2

#initializing reactor
molecule_reactor = Reactor(test_molecule)
print molecule_reactor._data.bonds

#need to test add_data and add_atoms, _compatible_format,
#_find_new_data, _add_new_data from body_data
#need to write two more methods join and add_body_data

#need to test density module

#than need to write reactor class, and nano particle clas
#also need to write a conversion modulue/class
