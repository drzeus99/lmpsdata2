# -*- coding: utf-8 -*-

import body_data
from body_data import Body_data
from header_data import Header_data
from molecule import Molecule
from density import Density
from reactor import Reactor
from nanoparticle import Nanoparticle

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
        self.keyword_relationship = Body_header_keyword_relationship()
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
    
    def _update_unconnected_body_keywords(self):
        """Write later"""
        keywords = ["Pair Coeffs", "PairIJ"]
        for keyword in keywords:
            if len(self.get_body_data(keyword)) != 0:
                try:
                    self.body_keywords.index(keyword)
                except ValueError:
                    self.body_keywords.append(keyword)
            else:
                try:
                    self.body_keywords.remove(keyword)
                except ValueError:
                    pass

    def _update_unconnected_header_keywords(self, data): #write this up later
        """Write later"""
        first_keyword_test = ["extra bond per atom"]
        second_keyword_tests = [ "xlo xhi", "ylo yhi", "zlo zhi"]
        third_keyword_test = "xy xz yz"
        #first keyword test
        #this is a workaround for the fact python does not have a goto statement.
        #only need to test for header_keyword attribute when testing first_keyword_test
        for keyword in first_keyword_test:
            try:
                self.header_keywords.index(keyword)
            except ValueError:
                try:
                    data.header_keywords.index(keyword)
                    self.header_keywords.append(keyword)
                    self.set_header_data(keyword, data.get_header_data(keyword))
                    continue
                except ValueError:
                    continue
                except AttributeError:
                    return
            try:
                data.header_keywords.index(keyword)
            except ValueError:
                continue
            except AttributeError:
                return
            if data.get_header_data(keyword) > self.get_header_data(keyword):
                self.set_header_data(keyword, data.get_header_data(keyword))
        #second keyword tests
        for keyword in second_keyword_tests:
            #testing to see if self contains the keyword
            #if not test to see if data contains the keyword
            #if it does assign the keyword to self and update self's information
            #otherwise skip to next keyword
            try:
                self.header_keywords.index(keyword)
            except ValueError:
                try:
                     data.header_keywords.index(keyword)
                     self.header_keywords.append(keyword)
                     self.set_header_data(keyword, data.get_header_data(keyword))
                     continue
                except ValueError:
                    continue
            #testing to see if data contains the keyword
            #if data does not skip to next keyword
            try:
                data.header_keywords.index(keyword)
            except ValueError:
                continue
            #otherwise compare the information between the two headers
            difference_found = False
            replacement = []
            for i in range(2):
                try:
                    if data.get_header_data(keyword)[i] < self.get_header_data(keyword)[i]:
                        difference_found = True
                        replacement.append(data.get_header_data(keyword)[i])
                    else:
                        replacement.append(self.get_header_data(keyword)[i])
                except IndexError:
                    raise EnvironmentError("Due to a programming bug, a script error or the wrath of god, one of the databases has invalid informantion stored for {}"\
                    .format(keyword))
            if difference_found:
                self.set_header_data(keyword, replacement)
        try:
            self.header_keywords.index(third_keyword_test)
        except ValueError:
            try:
                data.header_keywords.index(third_keyword_test)
                raise EnvironmentError("The information in the two headers cannot be joined because the simulation boxes have two different tilt factors.")
            except ValueError:
                return
        try:
            data.header_keywords.index(third_keyword_test)
        except ValueError:
            raise EnvironmentError("The information in the two headers cannot be joined because the simulation boxes have two different tilt factors.")
        #testing to see if there are any differences between the two header databases for the third_keyword_test
        if self.get_header_data(third_keyword_test) != data.get_header_data(third_keyword_test):
            raise EnvironmentError("The information in the two headers cannot be joined because the simulation boxes have two different tilt factors.")

    def join(self, data_list): #write this later and link to body_data's join method
        """Add Later"""
        #join data_list to body_data portion of lmpsdata
        Body_data.join(self, data_list)
        #updates all body and header keywords that are interconnected
        self.keyword_relationship.update_all_relationships(self) 
        #update the body_keywords that are not connected to header_keywords
        self._update_unconnected_body_keywords()
        #update the header_keywords that are not connected to body_keywords
        for data in data_list:
            self._update_unconnected_header_keywords(data)
        
    def add_body_data(self, data): #start with this one
        """will implement later"""
        Body_data.add_body_data(self,data)
        #updates all body and header keywords that are interconnected
        self.keyword_relationship.update_all_relationships(self)
        #update the body_keywords that are not connected to header_keywords
        self._update_unconnected_body_keywords()
        #update the header_keywords that are not connected to body_keywords
        self._update_unconnected_header_keywords(data)
                                        
    def add_atoms(self, atoms): #Rewrite Comment Block
#        """add a dictionary of atoms or a list of list of strings to the body data
#        dictionary of atoms. if a list of list of strings is given its converted 
#        to a dictionary. returns a dictionary 
#        containing the old and new keys. the old keys are are the atom ids of
#        the input atoms. the new keys are the atom ids of the atoms added to
#        the body data dictionary of atoms. If an incompatibility is detected 
#        between the atom_style of atoms and the body data dictionary of atoms, 
#        a runtime error is raised."""
        Body_data.add_atoms(self,atoms)
        self.keyword_relationship.update_individual_relationship(self, "Atoms")
#       
#        
    def add_data(self, data, keyword): #Rewrite Comment Block
#        """add a dictionary or list of list of strings or a list to the corresponding 
#        item stored in body_data. if a list of list of strings is given its converted
#        to a dictionary or list depending on keyword. if an incompatibility is detected between the atom_style of
#        velocities and the body data dictionary of velocities, a runtime error 
#        is raised. For coefficients runs a method to ensure duplication of data does
#        not occur. For other data types, there is no check for duplication."""
        Body_data.add_data(self, data, keyword)
        if keyword != "Pair Coeffs" and keyword != "PairIJ":
            self.keyword_relationship.update_individual_relationship(self, keyword)
        else:
            self._update_unconnected_body_keywords()
       
class Body_header_keyword_relationship(object):
    """Add later"""
    def __init__(self):
        """Add later"""
        self.relationship = {}
        self._initialize_relationship()
        
    def _initialize_relationship(self):
        """Add later"""
        self.relationship["Atoms"] = "atoms"
        self.relationship["Velocities"] = "atoms"
        self.relationship["Bonds"] = "bonds"
        self.relationship["Angles"] = "angles"
        self.relationship["Dihedrals"] = "dihedrals"
        self.relationship["Impropers"] = "impropers"
        self.relationship["Masses"] = "atom types"
        self.relationship["Bond Coeffs"] = "bond types"
        self.relationship["Angle Coeffs"] = "angle types"
        self.relationship["Dihedral Coeffs"] = "dihedral types"        
        self.relationship["Improper Coeffs"] = "improper types"
 
    def update_all_relationships(self, lmpsdata_object): #write this up later
        """Add Later"""
        keyword_list = ["Atoms", "Masses", "Velocities", "Bonds", "Bond Coeffs",\
        "Angles", "Angle Coeffs", "Dihedrals", "Dihedral Coeffs", "Impropers",\
        "Improper Coeffs"]
        for body_keyword in keyword_list:
            self.update_individual_relationship(lmpsdata_object, body_keyword)

    def update_individual_relationship(self, lmpsdata_object, body_keyword): #write this up later
        """Add Later"""        
        #algorithm if body_keyword is there
        #need to check if body_keyword and corresponding header keyword are still needed
        #if not needed anymore remove keyword and update corresponding header keyword information 
        #otherwise only update corresponding header keyword information
        try:
            body_index = lmpsdata_object.body_keywords.index(body_keyword)
            body_len = len(lmpsdata_object.get_body_data(body_keyword))
            if body_len != 0:
                #update corresponding header keyword information to match body data
                #assume header keyword is already present
                lmpsdata_object.set_header_data(self.relationship[body_keyword], body_len)
            else:
                #remove body_keyword and corresponding header keyword
                lmpsdata_object.body_keywords.pop(body_index)
                try:
                    lmpsdata_object.header_keywords.remove(self.relationship[body_keyword])
                    #update corresponding header_keyword information to base setting
                    lmpsdata_object.set_header_data(self.relationship[body_keyword], int)
                except ValueError:
                    raise EnvironmentError("Either due to a incorrect LAMMPS data file, software bug, or script command the {0} keyword has no relationship with {1} keyword in the current database."\
                    .format(body_keyword, self.relationship[body_keyword]))
        #algorithm if body_keyword is not there
        #need to check if body_keyword and corresponding header_keyword are needed
        #if needed update corresponding header_keyword information
        #otherwise do nothing
        except ValueError:
            body_len = len(lmpsdata_object.get_body_data(body_keyword))
            if body_len != 0:
                #add body_keyword
                lmpsdata_object.body_keywords.append(body_keyword)
                #add corresponding header_keyword, check for duplicaton when Atoms or Velocities keyword is used
                if body_keyword == "Atoms" or body_keyword == 'Velocities':
                    try:
                        lmpsdata_object.header_keywords.index(self.relationship[body_keyword])
                    except ValueError:
                        lmpsdata_object.header_keywords.append(self.relationship[body_keyword])
                else:
                    lmpsdata_object.header_keywords.append(self.relationship[body_keyword])
                #update corresponding header keyword information to match body data
                lmpsdata_object.set_header_data(self.relationship[body_keyword], body_len)
            
#need to test add_data add_atoms and add_body_data in the morning

#have 2253 lines of code. original program was 1945 lines of code
           
#header data has been completely tested just through reading and writing
#for body data; get_body_data, create, check_body_keyword, _in_body_list, _initialize factory
#_initialize_body_keyword_map have been successfully tested from writing and reading in lmpsdata
#lmpsdata has been completely tested at this point
#read write completely succesful //!also tested pmma85compositedata.initeq to see if velocity works
            #and it does
#molecule class completely tested
#extract from body_data works
#find and search method from body-data works           

            
#test_one = Lmpsdata('full', 'pmma85compositedata.initeq')
#print test_one.body_keywords
#print test_one.header_keywords
#test_one.pair_coeffs.append('1')
#print test_one.get_body_data("Pair Coeffs")
#test_one.delete_body_data("Pair Coeffs")
#print test_one.get_body_data("Pair Coeffs")
#test_molecule = Molecule(test_one, 2)
#print test_molecule.velocities
#print test_molecule.get_body_data("Velocities")
#import copy
#test_two = copy.deepcopy(test_one)
#test_two = Lmpsdata('full')
#test_two.add_atoms(test_one.atoms)
#test_two.add_data(test_one.bond_coeffs, 'Bond Coeffs')
#test_two.add_body_data(test_one)
#print "the original atoms are", len(test_one.atoms), "long"
#print "the atoms are", len(test_two.get_body_data("Atoms")), "long"
#print "the orginal bond coeffs are", len(test_one.bond_coeffs), "long"
#print "the bond coeffs are", len(test_two.bond_coeffs), "long"
#print test_two.atom_num
#print test_two.bond_type_num
#print test_two.header_keywords
#print test_two.body_keywords
#print
#print test_two.atoms
#print test_two.velocities
#for key, value in test_one.get_body_data("Impropers").items():
#    print key, value.write()


#combo_data = [test_one, test_two]
##test_three = Lmpsdata('full')
#test_three = copy.deepcopy(test_one)
#test_three.join(combo_data)
#print "the original atoms are", len(test_one.atoms), "long"
#print "the atoms are", len(test_three.get_body_data("Atoms")), "long"
#print "the orginal bonds are", len(test_one.bonds), "long"
#print "the bonds are", len(test_three.bonds), "long"
##print test_three.get_body_data("Bond Coeffs")
##print test_three.get_body_data("Pair Coeffs")
#print test_three.header_keywords
#print test_three.body_keywords
#old_new = test_two.add_atoms(test_one.atoms)
##old_new = test_one.add_atoms(test_two.atoms)
#print test_two.atoms == test_one.atoms
#test_one.delete_body_data("Atoms")
#print test_two.atoms
#print test_one.atoms
##print old_new
#test_two.add_data(test_one.angles, "Angles")
#print (test_two.angles) == (test_one.angles)
#test_two.add_data(test_one.bonds, "Bonds")
#print test_two.bonds == test_one.bonds
#test_two.add_data(test_one.dihedrals, "Dihedrals")
#print test_two.dihedrals == test_one.dihedrals
#test_two.add_data(test_one.impropers, "Impropers")
#print test_two.impropers == test_one.impropers
##
#test_three.add_data(test_one.angle_coeffs, "Angle Coeffs")
#print test_three.get_body_data("Angle Coeffs")
#print test_three.angle_coeffs
#test_two.add_body_data(test_three)
#test_two.add_data(test_one.bond_coeffs, "Bond Coeffs")
#print test_two.bond_coeffs == test_one.bond_coeffs
#test_two.add_data(test_one.dihedral_coeffs, "Dihedral Coeffs")
#print test_two.dihedral_coeffs == test_one.dihedral_coeffs
#test_two.add_data(test_one.improper_coeffs, "Improper Coeffs")
#print test_two.improper_coeffs == test_one.improper_coeffs
#test_two.add_data(test_one.pair_coeffs, "Pair Coeffs")
#print test_one.pair_coeffs == test_two.pair_coeffs
#test_two.add_data(test_one.masses, "Masses")
#print test_one.masses == test_two.masses
#test_molecule = Molecule(test_one, 2)
#print len(test_molecule.bonds)
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
#search method tested but not super extensively
#for key, atom in test_molecule.impropers.items():
#find method with method set to "dict" successful
##find method for pair coefficients successful


#need to test reactor class

#need to test density module and space module

#need to finish shape classes and write nano particle class
#need to write two more methods join and add_body_data in body data
#may need to write equivalent methods in lmsdata class
