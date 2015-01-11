# -*- coding: utf-8 -*-

from angle import Angle
from atom import Atom
from bond import Bond
from coeffs_angle import Coeffs_angle
from coeffs_bond import Coeffs_bond
from coeffs_dihedral import Coeffs_dihedral
from coeffs_improper import Coeffs_improper
from dihedral import Dihedral
from improper import Improper
from mass import Mass
from pair_coeffs import Pair_coeffs
from velocity import Velocity

class Body_data(object):
    """stores the information associated with LAMMPS body data keywords. 
    creates and accesses objects associated with LAMMPS body data keywords."""
    def __init__(self, atom_style):
        """initializes LAMMPS body data information, sets the atom_style used, 
        initializes dictionaries used by the class to create and access dictionaries
        associated with body_data"""
        self.atom_style = atom_style
        self.angles = {}
        self.atoms = {}
        self.bonds = {}
        self.angle_coeffs = {}
        self.bond_coeffs = {}
        self.dihedral_coeffs = {}
        self.improper_coeffs = {}
        self.dihedrals = {}
        self.impropers = {}
        self.masses = {}
        # represents both PairIJ and Pair Coeffs keyword which
        # may cause bugs to occur
        # if bugs occur split PairIJ and Pair Coeffs to seperate lists
        self.pair_coeffs = []
        self.velocities = {}
        self._factory = {}
        self._initialize_factory()
        self._body_keyword_map = {}
        self._initialize_body_keyword_map()
        
    def _initialize_factory(self):
        """create the dictionary used to create objects associated with body
        data. the keys in the dictionary are the body data keywords and the
        values are classes associated with body data."""
        self._factory["Angles"] = Angle
        self._factory["Atoms"] = Atom
        self._factory["Bonds"] = Bond
        self._factory["Angle Coeffs"] = Coeffs_angle
        self._factory["Bond Coeffs"] = Coeffs_bond
        self._factory["Dihedral Coeffs"] = Coeffs_dihedral
        self._factory["Improper Coeffs"] = Coeffs_improper
        self._factory["Dihedrals"] = Dihedral
        self._factory["Impropers"] = Improper
        self._factory["Masses"] = Mass
        self._factory["Pair Coeffs"] = Pair_coeffs
        self._factory["PairIJ"] = Pair_coeffs
        self._factory["Velocities"] = Velocity
        
    def _initialize_body_keyword_map(self):
        """create the dictionary used to access dictionaries associated with
        body data. the keys in the dictionary are the body data keywords and 
        the values are dictionaries associated with body data"""
        self._body_keyword_map["Angles"] = self.angles
        self._body_keyword_map["Atoms"] = self.atoms
        self._body_keyword_map["Bonds"] = self.bonds
        self._body_keyword_map["Angle Coeffs"] = self.angle_coeffs
        self._body_keyword_map["Bond Coeffs"] = self.bond_coeffs
        self._body_keyword_map["Dihedral Coeffs"] = self.dihedral_coeffs
        self._body_keyword_map["Improper Coeffs"] = self.improper_coeffs
        self._body_keyword_map["Dihedrals"] = self.dihedrals
        self._body_keyword_map["Impropers"] = self.impropers
        self._body_keyword_map["Masses"] = self.masses
        self._body_keyword_map["Pair Coeffs"] = self.pair_coeffs
        self._body_keyword_map["PairIJ"] = self.pair_coeffs
        self._body_keyword_map["Velocities"] = self.velocities
        
    def create(self, keyword):
        """create an object associated with a body data keyword using the 
        _factory dictionary to get the correct object type. keyword is a body 
        data keyword."""
        if keyword=="Atoms" or keyword=="Velocities":
            return self._factory[keyword](self.atom_style)
        else:
            return self._factory[keyword]()
    
    def check_body_keyword(self, input):
        """checks if a body data keyword is located in input. input is a list
        of strings. returns whether a body data keyword was found in input and 
        the resulting body data keyword as a string. The string is empty if no 
        body data keyword is found"""
        #if input is an empty list, no body_keywords can be found, end method
        if input == []:
            return False, ""
        #build list of currently supported body_keywords
        body_keywords = [["Angles"], ["Atoms"], ["Bonds"],\
        ["Angle", "Coeffs"], ["Bond", "Coeffs"], ["Dihedral", "Coeffs"],\
        ["Improper", "Coeffs"], ["Dihedrals"], ["Impropers"], ["Masses"],\
        ["Pair", "Coeffs"], ["PairIJ"], ["Velocities"]]
        #find if any body_keywords are in input
        for word_list in body_keywords:
            if self._in_body_list(word_list, input):
                #build word_list into a string and return results
                string = " ".join(i for i in word_list)
                return True, string
        #no body_keywords were found in input
        return False, ""
    
    def _in_body_list(self, list1, list2):
        """check if list2 contains elements from list1. the routine starts 
        checking at list1[0] and list2[0]. The routine continues until list1[i]
        does not equal list2[i] or an index error occurs because list2 is 
        shorter than list1 or all elements of list1 have been checked. If the 
        first two conditions end the algorithm, the algorithm will return false.
        otherwise, the algorithm returns true."""
        for i in range(len(list1)):
            try:
                if list1[i] != list2[i]:
                    return False
            except IndexError:
                return False
        return True
        
    def get_body_data(self, keyword):
        """returns the dicitionary or list associated with keyword. keyword is 
        a body data keyword. the association is stored in _body_keyword_map."""
        return self._body_keyword_map[keyword]
        
    def delete_body_data(self, keyword):
        """deletes the items stored in the dictionary or list associated with
        keyword. keyword is a body data keyword. if the dictionary or list 
        stored in this class has been directly assigned to another dictionary
        or list. this method will clear both dictionaries or lists which have been
        assigned. To avoid this, use copy or deepcopy methods when assigning a
        list or dictionary from this class to another list or dictionary."""
        data = self.get_body_data(keyword)
        #handles body_data which is a list
        if keyword == "Pair Coeffs" or keyword == "PairIJ":
            data[:] = []
        else:#handles body_data which is a dictionary
            data.clear()
                
   # def join(self,): Than do this one
        
    def extract(self, data, atom_info, value):
        """extracts the atoms from data that have the matching value for atom_info.
        than extracts the associated information from angles, bonds, dihedrals,
        impropers, velocities, and masses. copies all coefficient information.
        data is a body_data object, atom_info is a string that corresponds to
        the name of a variable stored in the atom class. the type for value is 
        dependent on atom_info and will either be an int or a float."""
        atom_keys = self._extract_atoms(data, atom_info, value)
        self._extract_coefficients(data)
        self._extract_velocities(data, atom_keys)
        self._extract_connections(data, atom_keys)
        
    def _extract_atoms(self, data, atom_info, value):
        """Add later"""
        from copy import deepcopy
        #deepcopy atoms
        atom_keys = data.find("Atoms", atom_info, value, "keys")
        for key in atom_keys:
            self.atoms[key] = deepcopy(data.atoms[key])
        return atom_keys
    
    def _extract_coefficients(self, data):
        """Add later"""
        coeffs = {}
        coeffs["Angle Coeffs"] = "angle_coeffs"
        coeffs["Bond Coeffs"] = "bond_coeffs"
        coeffs["Dihedral Coeffs"] = "dihedral_coeffs"
        coeffs["Improper Coeffs"] = "improper_coeffs"
        coeffs["Pair Coeffs"] = "pair_coeffs"
        coeffs["Masses"] = "masses"
        #copy coeffs
        from copy import copy
        for keyword, value in coeffs.items():
           self.__setattr__(value, copy(data.get_body_data(keyword)))
           
    def _extract_velocities(self, data, atom_keys):
        from copy import deepcopy
        #deepcopy velocities
        for key in atom_keys:
            try:
                self.velocities[key] = deepcopy(data.velocities[key])
            except KeyError:
                break
    
    def _extract_connections(self, data, atom_keys):
        """Add later"""
        from copy import deepcopy
        #deepcopy uniquely found angles, dihedrals, impropers, bonds
        #this algorithm should be O(N*M) where N is the size of the data dictionary
        #and M is the size of atom_keys
        connection_keywords = ["Angles", "Bonds", "Dihedrals", "Impropers"]
        for keyword in connection_keywords:
            found_keys = data.search(keyword, "atom", atom_keys, "keys")
            for key in found_keys:
                self.get_body_data(keyword)[key] = deepcopy(data.get_body_data(keyword)[key])
        
    def find(self, keyword, info, value, method):
        """finds the data corresponding with keyword that has the matching
        value for info. returns either a list of keys or a new dictionary.
        keyword is a string that is a body_data keyword. info is a string that 
        corresponds to the name of a variable stored in the class that corresponds
        to the given keyword. the type for value is dependent on info and will 
        either be an int, a float or a string. method is a string that is either
        "keys" or "dict" which correspond to the method returning a list of keys 
        or a new dictionary. If keyword is 'PairIJ' or 'Pair Coeffs' this method
        returns a list of Pair_coeffs objects."""
        if keyword == "Pair Coeffs" or keyword == "PairIJ":
            data = self.get_body_data(keyword)
            pair_list = []
            try:
                for item in data:
                    if value in item.__getattribute__(info):
                        pair_list.append(item)
            except TypeError:
                for item in data:
                    if value == item.__getattribute__(info):
                        pair_list.append(item)
            return pair_list
        if method == "keys":
            data = self.get_body_data(keyword)
            key_list = []
            try:
                for key, item in data.items():
                    if value in item.__getattribute__(info):
                        key_list.append(key)
            except TypeError:
                for key, item in data.items():
                    if value == item.__getattribute__(info):
                        key_list.append(key)
            return key_list
        elif method =="dict":
            data = self.get_body_data(keyword)
            new_dict = {}
            try:
                for key, item in data.items():
                    if value in item.__getattribute__(info):
                        from copy import copy
                        new_dict[key] = copy(item)
            except TypeError:
                for key, item in data.items():
                    if value == item.__getattribute__(info):
                        from copy import copy
                        new_dict[key] = copy(item)
            return new_dict
        else:
            raise RuntimeError('the value inputed for method is invalid. valid values are "keys" or "dict".')

    def search(self, keyword, info, values, method):
        """finds the data corresponding with keyword that has the matching 
        values for info. returns either a list of keys or a new dictionary.
        keyword is a string that is a body_data keyword. info is a string that 
        corresponds to the name of a variable stored in the class that corresponds
        to the given keyword. the type for values is dependent on info and will 
        either be a list of ints, a list of floats or a list of strings. 
        method is a string that is either
        "keys" or "dict" which correspond to the method returning a list of keys 
        or a new dictionary. If keyword is 'PairIJ' or 'Pair Coeffs' this method
        returns a list of Pair_coeffs objects."""
        if keyword == "Pair Coeffs" or keyword == "PairIJ":
            data = self.get_body_data(keyword)
            pair_list = []
            try:
                for item in data:
                    for value in values:
                        if value in item.__getattribute__(info):
                            pair_list.append(item)
                            break
            except TypeError:
                for item in data:
                    for value in values:
                        if value == item.__getattribute__(info):
                            pair_list.append(item)
                            break
            return pair_list
        if method == "keys":
            data = self.get_body_data(keyword)
            key_list = []
            try:
                for key, item in data.items():
                    for value in values:
                        if value in item.__getattribute__(info):
                            key_list.append(key)
                            break
            except TypeError:
                for key, item in data.items():
                    for value in values:
                        if value == item.__getattribute__(info):
                            key_list.append(key)
                            break
            return key_list
        elif method =="dict":
            from copy import copy
            data = self.get_body_data(keyword)
            new_dict = {}
            try:
                for key, item in data.items():
                    for value in values:
                        if value in item.__getattribute__(info):
                            new_dict[key] = copy(item)
                            break
            except TypeError:
                for key, item in data.items():
                    for value in values:
                        if value == item.__getattribute__(info):
                            new_dict[key] = copy(item)
                            break
            return new_dict
        else:
            raise RuntimeError('the value inputed for method is invalid. valid values are "keys" or "dict".')

#    def add_body_data(self, data): #start with this one
#        """will implement later"""
#        pass
                                
    def add_atoms(self, atoms):
        """add a dictionary of atoms or a list of list of strings to the body data
        dictionary of atoms. if a list of list of strings is given its converted 
        to a dictionary. returns a dictionary 
        containing the old and new keys. the old keys are are the atom ids of
        the input atoms. the new keys are the atom ids of the atoms added to
        the body data dictionary of atoms. If an incompatibility is detected 
        between the atom_style of atoms and the body data dictionary of atoms, 
        a runtime error is raised."""
        #check to make sure the atoms being added are compatible with the 
        # format of the current atoms contained in this body_data object
        if not(self._compatible_format(atoms)):
            raise RuntimeError("""The atom_style of the atoms being added are 
not compatible with the atoms currently stored in this body_data object""")
        init_key = max(self.atoms) + 1
        old_new_keys = {}
        #if atoms is a list convert atoms to a dictionary
        if isinstance(atoms, list):
            temp_list = atoms #copy atoms pointer to temp_list
            atoms = dict() #convert atoms variable to dictionary
            for row in temp_list: #fill dictionary with atom ids and atoms
                atom = self.create("Atoms")
                atom.read(row, 1)
                atoms[int(row[0])] = atom 
        for key, value in atoms.items():
            #add value to self.atoms as a shallow copy
            self.atoms[init_key] = value
            #store old_new key relationship and update init_key
            old_new_keys[key] = init_key
            init_key += 1
        return old_new_keys
        
    def add_data(self, data, keyword):
        """add a dictionary or list of list of strings or a list to the corresponding 
        item stored in body_data. if a list of list of strings is given its converted
        to a dictionary or list depending on keyword. if an incompatibility is detected between the atom_style of
        velocities and the body data dictionary of velocities, a runtime error 
        is raised. For coefficients runs a method to ensure duplication of data does
        not occur. For other data types, there is no check for duplication."""
        if isinstance(data, list) and keyword != "Pair Coeffs" and\
        keyword != "PairIJ":
            temp_list = data
            data = dict()
            for row in temp_list:
                item = self.create(keyword)
                item.read(row, 1)
                data[int(row[0])] = item
        elif isinstance(data[0], list) and (keyword == "Pair Coeffs" or\
        keyword == "PairIJ"):
            temp_list = data
            data = list()
            for row in temp_list:
                item = self.create(keyword)
                item.read(row, 0)
                data.append(item)
        if keyword == "Velocities":
            if not(self._compatible_format(data)):
                raise RuntimeError("""The atom_style of the velocities being
added are not compatible with the velocities currently stored in this body_data object""")
            self._add_new_data(data, keyword)
        elif keyword == "Angles" or keyword == "Bonds" or keyword == "Dihedrals"\
        or keyword == "Impropers":
            self._add_new_data(data, keyword)
        elif keyword == "Pair Coeffs" or keyword == "PairIJ" or keyword == "Angle Coeffs"\
        or keyword == "Bond Coeffs" or keyword == "Dihedral Coeffs" or keyword \
        == "Improper Coeffs" or keyword == "Masses":
            self._find_new_data(data, keyword)
        else:
            raise ValueError("inputed keyword is not a valid string.")
        
    def _compatible_format(self, keyword, data):
        """checks if the objects stored in data have an atom_style compatible
        with the objects stored in body_data. this method can call the _check_format
        method of the velocity and atom objects."""
        data_keys = data.keys()
        #check if atom_styles match if so return true
        if (data[data_keys[0]].atom_style == self.atom_style):
            return True
        else: #check if atom_styles are compatible
            return data[data_keys[0]]._check_format(self.atom_style)

    def _find_new_data(self, data, keyword):
        """inserts new coefficient data into body_data. insures that duplicate
        data is not inserted."""
        #check if data is empty
        if len(data) == 0:
            return
        #check if get_body_data(keyword) is empty
        if len(self.get_body_data(keyword)) == 0:
            from copy import copy
            data_in_object = self.get_body_data(keyword) 
            data_in_object = copy(data)
        #check if data and get_body_data(keyword) are the same    
        if cmp(data, self.get_body_data(keyword)):
            pass #does nothing since data is the same as get_body_data(keyword)
        else:
            #for dealing with lists, O(n^2) algorithm
            if keyword == "Pair Coeffs" or keyword == "PairIJ":
                for i in data:
                    test = False
                    for j in self.get_body_data(keyword):
                        if not(cmp(i,j)):
                            test = True
                            break
                    if not test:
                        self.get_body_data(keyword).append(i)                    
            #for dealing with dictionaries, O(n^2) algorithm
            elif keyword == "Angle Coeffs" or keyword == "Bond Coeffs" or \
            keyword == "Dihedral Coeffs" or keyword == "Improper Coeffs":
                old_data = self.get_body_data(keyword)
                init_key = max(old_data)
                for val1 in data.values():
                    test = False
                    for val2 in old_data.values():
                        if not(cmp(val1, val2)):
                            test = True
                            break
                    if not test:
                        old_data[init_key] = val1
                        init_key += 1
                        
    def _add_new_data(self, data, keyword):
        """inserts new data into body_data. does not check if duplication occurs"""
        old_data = self.get_body_data(keyword)
        init_key = max(old_data) + 1
        for value in data.values():
            old_data[init_key] = value
            init_key += 1 