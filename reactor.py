# -*- coding: utf-8 -*-

class Reactor(object):
    """contains methods for modifying the objects stored in body_data. Additionally,
    allows the storage of a body_data object that is allowed to interact with other
    body_data objects"""
    def __init__(self, data):
        """initializes the reactor object with a stored body_data object. data
        is the body_data object to store in the reactor. particle_bonding_information
        is a list of lists where [i][0] is the atom key in the reactor and [i][1]
        is the atom key in a particle object"""
        self._data = data
        self._particle_bonding_information = []

    @staticmethod
    def change_atom_num(data, old_new_keys): #finished except comment block
        """Add later"""
        from copy import copy
        #use old_new_keys to build new velocity dictionary
        new_velocities = {}
        for old_key, new_key in old_new_keys.items():
            new_velocities[new_key] = copy(data.velocities[old_key])
        #delete old velocity dictionary 
        #[delete is required before set to avoid memory leak due to ref count never reaching 0]
        data.delete_body_data("Velocities")
        #set old velocity dictionary to new_velocity_dictionary
        #copy is required here so that when new_velocities is deleted as this method
        #ends data.velocities will not be pointing to garbage collected objects
        data.__setattr__("velocities", copy(new_velocities))
        #use old_new_keys to modify data.angles, data.bonds, data.dihedrals, data.impropers
        connection_keywords = ["Angles", "Bonds", "Dihedrals", "Impropers"]
        for keyword in connection_keywords:
            connection = data.get_body_data(keyword)
            for item in connection.values():
                for index in range(len(item.atom)):
                    #item.atom[index] is set at the old_key value.
                    # this needs replacing with the new_key
                    #which is old_new_keys[item.atom[index]]
                    item.atom[index] = old_new_keys[item.atom[index]]
                
    @staticmethod
    def delete_atoms(data, keys): #finished except comment block
        """Add later"""
        for key in keys:
            del data.atoms[key]
        connection_keywords = ["Angles", "Bonds", "Dihedrals", "Impropers"]
        for keyword in connection_keywords:
            connection = data.get_body_data(keyword)
            for index, item in connection.items():
                for key in keys:
                    if key in item.atom:
                        del connection[index]
                        break

    @staticmethod
    def add_atom(data, info): #finished except comment block
        """Add later """
        max_key = max(data.atoms)
        data.atoms[max_key + 1] = data.create("Atoms")
        data.atoms[max_key + 1].read(info, 0)

    @staticmethod #has to be a way to simplify this ->second to n insertion can be placed in a seperate method
    def find_connected_atoms(data, atom_keys, connection_rules): #finished except comment block
        """Add later"""
        connected_atoms = []
        if connection_rules == []:
            return connected_atoms
        this_pass = []
        #search for bond ids that contain atom_keys
        connected_bond_ids = data.search("Bonds", "atom", atom_keys, "keys")
        #search for connected_atoms that follow the connection rules
        #this is the first iteration to find connected_atoms
        for bond_id in connected_bond_ids:
            for atom_id in data.bonds[bond_id].atom:
                if atom_id in atom_keys:
                    continue
                else:
                    for rule in connection_rules:
                        if data.atoms[atom_id].__getattribute__(rule[0]) == rule[1]:
                            connected_atoms.append(atom_id)
                            this_pass.append(atom_id)
                        break
        if this_pass == []:
            return connected_atoms
        #search for bond ids that contanin this pass
        connected_bond_ids = data.search("Bonds", "atom", this_pass, "keys")
        previous_pass = this_pass
        #this is the second iteration to find connected atoms
        this_pass = Reactor._find_connections_this_iteration(data, connected_bond_ids, connected_atoms, previous_pass, atom_keys)
        while this_pass != []:
            #search for bond ids that contain this pass
            connected_bond_ids = data.search("Bonds", "atom", this_pass, "keys")
            previous_previous_pass = previous_pass
            previous_pass = this_pass
            #this is the n iteration to find connected atoms
            this_pass = Reactor._find_connections_this_iteration(data, connected_bond_ids, connected_atoms, previous_pass, previous_previous_pass)
        return connected_atoms
        
    @staticmethod
    def _find_connections_this_iteration(data, connected_bond_ids, connected_atoms, previous_pass, previous_previous_pass):
        """Add later"""
        this_pass = []
        for bond_id in connected_bond_ids:
            for atom_id in data.bonds[bond_id].atom:
                if atom_id in previous_previous_pass:
                    break
                elif atom_id in previous_pass:
                    continue
                else:
                    connected_atoms.append(atom_id)
                    this_pass.append(atom_id)
                    break
        return this_pass
    
#    @staticmethod
#    def find_abd_connections(): Will finish in later versions
#        pass

#    @staticmethod
#    def add_abd_connections(): Either use singular or plural method or possibly both
#        pass
    
    @staticmethod
    def modify(data, keyword, index, info, value): #finished except comment block
        """Add later"""
        body_data = data.get_body_data(keyword)
        if info == "all":
            body_data[index].read(value, 0)
        else:
            body_data[index].__setattr__(info, value)
    
    def find_particle_bonding_locations(self, particle, info, value, cutoff_distance, bond_number): #finished except comment block
        """Rewrite this"""
        #checking to make sure bond_number is not 0
        if bond_number == 0:
            print "bond number is 0; so, no possible bonds can form."
            return 
        #find dictionary of atoms in reactor that can possibly form bonds to particle surface
        possible_reactor_bonds = self._data.find("Atoms", info, value, "dict")
        #remove atoms in possible_reactor_bonds that are not nearest neighbors to particle
        for key, item in possible_reactor_bonds.items():
            if not particle.nearest_neighbor(item, cutoff_distance):
                del possible_reactor_bonds[key]
        import space
        #possible bonds is a dictionary where keys are particle surface values
        #and the values are a list of atom keys in the reactor
        possible_bonds = {}
        #find possible_bonds
        for surface_key in particle.surface:
            possible_bonds[surface_key] = []
            for reactor_key in possible_reactor_bonds.keys():
                if space.distance(particle.atoms[surface_key], possible_reactor_bonds[reactor_key]) <= cutoff_distance:
                    possible_bonds[surface_key].append(reactor_key)
        #possible surface keys is a list containing particle surface keys where
        #bonds can form. these keys connect to the possible_bonds dictionary above
        possible_surface_keys = []
        #find possible surface keys
        for surface_key in possible_bonds.keys():
            if len(possible_bonds[surface_key]) != 0:
                possible_surface_keys.append(surface_key)
        #check if possible surface keys is empty
        if possible_surface_keys == []:
            print "no possible bonds can be formed"
            return
        #initialize Boolean_dict representing the state of assigned bond formation
        #to possible reactor bonds 
        assigned_reactor_bonds = Boolean_dict(possible_reactor_bonds.keys(), False)
        #checking if _particle_bonding_information is empty 
        if len(self._particle_bonding_information) != 0:
            self._particle_bonding_information[:] = []
        bonds = 0
        from random import randint
        #iterate until either bonds equals bond_number or possible surface keys is empty
        while bonds != bond_number:
            l = len(possible_surface_keys) - 1
            #randomly choose a surface key from the list of possible surface keys
            index = randint(0, l)
            choosen_surface_key = possible_surface_keys[index]
            #attempt to find a reactor key amongst the possible bonds associated to the choosen surface key
            reactor_key, found = self._find_reactor_bond(possible_bonds[choosen_surface_key], assigned_reactor_bonds)
            if found:
                #append keys to bonding information
                self.bondinginformation.append([reactor_key, choosen_surface_key])
                bonds += 1
            #delete randomly choosen surface key from list of possible surface keys
            del possible_surface_keys[index]
            if possible_surface_keys == []:
                return
                
    def _find_reactor_bond(self, possible_reactor_bonds, assigned_reactor_bonds):#finished except comment block
        """Write this later"""
        from random import randint
        reactor_key = 0
        found = False
        l = len(possible_reactor_bonds) - 1
        #iterate until possible reactor bonds is empty or 
        #the element tested in assigned reactor bonds is set to False
        while possible_reactor_bonds != []:
            index = randint(0, l)
            if assigned_reactor_bonds.test_element(possible_reactor_bonds[index], False):
                #set the tested element to True
                assigned_reactor_bonds.set_element(possible_reactor_bonds[index], True)
                #assign the found key to reactor key
                reactor_key = possible_reactor_bonds[index]
                found = True
                break
            else:
                del possible_reactor_bonds[index]   
                l -= 1
        return reactor_key, found

    def bond_to_ceramic_particle(self, particle, reactor_modifications, reactor_delete_rules):
        """Write this later"""
        print 'modifying the bonded molecules atom information'
        #extract keys from bonding information as you are doing modifications in this step
        reactor_keys = []
        particle_keys = []
        for i in range(len(self.bondinginformation)):
            for j in range(len(reactor_modifications)):
                self.modify(self._data, "Atoms", self.bondinginformation[i][0], reactor_modifications[j][0], reactor_modifications[j][1])
                reactor_keys.append(self.bondinginformation[i][0])
                particle_keys.append(self.bondinginformation[i][1])
                #reactor_modifications[j][0] is info
                #reactor_modifications[j][1] is value
        #find the atom keys in the reactor that need deleting than delete them        
        atom_keys = self.find_connected_atoms(self._data, reactor_keys, reactor_delete_rules)
        self.delete_atoms(self._data, atom_keys)
        #delete the atoms in the particle that the reactor has replaced when bonding
        self.delete_atoms(particle, particle_keys)

class Boolean_dict:#rewrite block comments
    """A class that stores boolean values in a list of lists."""	
    def __init__(self, dictionary, initval): 		
	""" initialise a list of lists (array) with
	rownum correspondinig to the number of lists in the list and 
	colnum corresponding to the number of elements in the list's list.
	initval is the value the list of lists will be initialized with.
	initval should be a boolean value."""
	# initializing _map
	self._map = []
	for i in dictionary.keys():
         self._map[i] = initval
			
    def set_element(self, key, value):
	"""Assigns value to the list of lists (array) element at rownum and colnum."""
	self._map[key] = value
	
    def test_element(self, key, value):
	"""Returns element in the list of lists (array) at rownum and colnum."""
	return self._map[key] == value