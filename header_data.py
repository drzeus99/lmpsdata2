# -*- coding: utf-8 -*-

class Header_data(object):
    """stores, reads and writes data in header lines from LAMMPS data files."""
    def __init__(self):
        """initializes the data stored in header lines and creates a dictionary 
        relating the header keywords to the header data"""
        self.atom_num = int
        self.bond_num = int
        self.angle_num = int
        self.dihedral_num = int
        self.improper_num = int
        self.atom_type_num = int
        self.bond_type_num = int
        self.angle_type_num = int
        self.dihedral_type_num = int
        self.improper_type_num = int
        self.extra_bond_num = int
        self.x_dimension = []
        self.y_dimension = []
        self.z_dimension = []
        self.tilt_dimension = []
        self._header_keyword_map = {}
        self._initialize_header_keyword_map()
        
    def _initialize_header_keyword_map(self): #redo the entire table
        """produces a dictionary relating the header keywords to the header
        data"""
        self._header_keyword_map["atoms"] = "atom_num"
        self._header_keyword_map["bonds"] = "bond_num"
        self._header_keyword_map["angles"] = "angle_num"
        self._header_keyword_map["dihedrals"] = "dihedral_num"
        self._header_keyword_map["impropers"] = "improper_num"
        self._header_keyword_map["atom types"] = "atom_type_num"
        self._header_keyword_map["bond types"] = "bond_type_num"
        self._header_keyword_map["angle types"] = "angle_type_num"
        self._header_keyword_map["dihedral types"] = "dihedral_type_num"
        self._header_keyword_map["improper types"] = "improper_type_num"
        self._header_keyword_map["extra bond per atom"] = "extra_bond_num"
        self._header_keyword_map["xlo xhi"] = "x_dimension"
        self._header_keyword_map["ylo yhi"] = "y_dimension"
        self._header_keyword_map["zlo zhi"] = "z_dimension"
        self._header_keyword_map["xy xz yz"] = "tilt_dimension"
        
    def check_header_keyword(self, input):
        """checks if a header keyword is located in input. input is a list 
        where the header keyword, if stored, will be contained in the last half
        of the list. returns true if a header keyword was found in input and 
        the resulting header keyword as a string. The string is empty if no 
        header keyword is found"""
        #if input is an empty list, no body_keywords can be found, end method
        if input == []:
            return False, ""
        #build list of currently supported body_keywords
        header_keywords = [["atoms"], ["bonds"], ["angles"], ["dihedrals"],\
        ["impropers"], ["atom", "types"], ["bond", "types"], ["angle", "types"],\
        ["dihedral", "types"], ["improper", "types"], ["xlo", "xhi"],\
        ["ylo", "yhi"], ["zlo", "zhi"], ["xy", "xz", "yz"],\
        ["extra", "bond", "per", "atom"]]
        #find if any body_keywords are in input
        for word_list in header_keywords:
            if self._in_header_list(word_list, input):
                #build word_list into a string and return results
                string = " ".join(i for i in word_list)
                return True, string
        #no body_keywords were found in input
        return False, ""        
    
    def _in_header_list(self, list1, list2):
        """list1 is a header keyword and list2 is an input line. Tests if the
        header keyword is in the input line. The header keyword will be at the
        end of the input line."""
        j = len(list2) - 1
        for i in range(len(list1) - 1, -1, -1):
            if list2[j] != list1[i]:
                return False
            j -= 1
        return True
    
    def get_header_data(self, keyword): #redo this entire thing
        """returns the list or value associated with keyword. keyword is a 
        header keyword. the association is stored in _header_keyword_map."""
        return self.__getattribute__(self._header_keyword_map[keyword])
        
    def set_header_data(self, keyword, value):
        """sets the list or value associated with keyword. keyword is a header
        header keyword. the association is stored in _header_keyword_map."""
        self.__setattr__(self._header_keyword_map[keyword], value)
        
    def read(self, input, keyword):
        """converts a list of strings into information stored in header_data.
        the information corresponds to keyword.
        input is a list of strings.
        keyword is a header keyword."""
        #reading floats
        if keyword == 'xlo xhi' or keyword == 'ylo yhi' or keyword == 'zlo zhi'\
        or keyword == 'xy xz yz':
            self._read_float(input, keyword, len(keyword.split()))
        #reading ints    
        elif keyword == 'atoms' or keyword == 'bonds' or keyword == 'angles' or\
        keyword == 'dihedrals' or keyword == 'impropers' or keyword ==\
        'atom types' or keyword == 'bond types' or keyword == 'angle types' or\
        keyword == 'dihedral types' or keyword == 'improper types' or keyword ==\
        'extra bond per atom':
            self._read_int(input, keyword)
        else:
            raise RuntimeError("{0} is not a valid keyword".format(keyword))
        
    def _read_int(self, input, keyword):
        """converts a list of strings to integers. the integers are stored in
        the information corresponding to keyword.
        input is a list of strings.
        keyword is a string."""
        #handling single values
        self.set_header_data(keyword, int(input[0]))

    def _read_float(self, input, keyword, length):
        """converts a list of strings to floats. the floats are stored in
        the information corresponding to keyword.
        input is a list of strings.
        keyword is a string.
        length is the number of words in keyword which is used to control how
        this method operates."""
        #handling lists
        if length != 1:
            data = self.get_header_data(keyword)
            data_len = len(data)
            if data_len == 0:
                for i in range(length):
                    data.append(float(input[i]))
            elif data_len == length:
                for i in range(length):
                    data[i] = float(input[i])
            else:
                raise RuntimeError("the data associated with {0} is not valid anymore"\
                .format(keyword))
        #handling single values        
        else: #even though this case doesn't currently exist it may exist later
            pass
        
    def write(self, keyword):
        """converts the information corresponding to keyword to a string.
        keyword is a header keyword."""
        return self._write_info(keyword, len(keyword.split()))
    
    def _write_info(self, keyword, length): #requires complete rewriting
        """converts the information corresponding to keyword to a space 
        separated string. the string contains the keyword at the end of the string.
        keyword is a header keyword.
        length is the number of words in keyword which is used to control how
        this method operates."""
        data = self.get_header_data(keyword)
        if keyword == 'xlo xhi' or keyword == 'ylo yhi' or keyword == 'zlo zhi'\
        or keyword == 'xy xz yz':
            if len(data) == length:
                return " ".join(str(data[i]) for i in range(len(data))) + ' ' + keyword
            else:
                raise RuntimeError("the data associated with {0} is not valid anymore"\
                .format(keyword))
        else:
            return "{0} {1}".format(data, keyword)
        