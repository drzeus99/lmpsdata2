# -*- coding: utf-8 -*-

from body_data import Body_data
from space import Sphere, Cube

class Nanoparticle(Body_data):
    """write later"""
    def __init__(self, data, method, shape, position, size, cutoff_distance, info=[], value=[], rotation=None):
        """write later""" #finished
        #stores shape information of nano particle also used to find the surface
        if shape == 'sphere':
            self.shape = Sphere(position, size)
        elif shape == 'cube':
            self.shape = Cube(position, size, rotation)
        else:
            raise RuntimeError('invalid shape inputed. valid shapes are sphere and cube.')
        #used for producing surface
        self.surface = []
        self.cutoff_distance = cutoff_distance
        self.info = info
        self.value = value
        if method == 'extract':
            Body_data.__init__(self, data.atom_style)
            self.extract(data)
            self._create_surface(self.atoms)
        elif method =='input':
            Body_data.__init__(self, data.atom_style)
            self.add_body_data(data)
            #create surface method is called inside add_body_data
        elif method == 'join':
            Body_data.__init__(self, data[0].atom_style)
            self.join(data)
            self._create_surface(self.atoms)
        else:
            raise RuntimeError('invalid method inputed. valid methods are extract, input, and join.')
        from reactor import Boolean_dict
        self.used_surface = Boolean_dict(self.surface, False)
    
    def _create_surface(self, atoms): #finished
        """Add Later"""
        for key, atom in atoms.items():
            if self.shape.nearest_neighbor(atom, self.cutoff_distance):
                if self.info == [] or self.value == []:
                    self.surface.append(key)
                elif len(self.info) == len(self.value):
                    for i in range(len(self.value)):
                        if atom.__getattribute__(self.info[i]) == self.value[i]:
                            self.surface.append(key)
                            break
                else:
                    raise RuntimeError("the info and value list assigned to nano particle at initialization do not having matching length")
    
    def nearest_neighbor(self, atom, cutoff_distance): #finished
        """Add later"""
        return self.shape.nearest_neighbor(atom, cutoff_distance)
        
    #public methods that need to be implemented            
    def delete_atoms(self, atom_keys): #finished #do you need to check if atoms are on surface
    #can we assume atoms are on surface since we are working with a nano particle?
        """Add later"""
        for key in atom_keys:
            try:
                self.surface.remove(key)
            except ValueError:
                continue
        from reactor import Reactor
        Reactor.delete_atoms(self, atom_keys)
    
    #can add atom to surface and internals yay!
    def add_atom(self, info, method='random_position', pbi = [0, 0, 0]):
        """Add later"""
        from copy import deepcopy
        from reactor import Reactor
        if method == 'random_position':
            position = self.shape.random_position_on_surface(self.cutoff_distance)
            new_info = deepcopy(info)
            new_info.extend(position)
            for i in range(3):
                new_info.append(str(pbi[i]))
            Reactor.add_atom(self, new_info)
            max_key = max(self.atoms)
            temp_atoms = {}
            temp_atoms[max_key] = self.atoms[max_key]
            self._create_surface(temp_atoms)            
#        elif method == 'guess_position': not implemented in this version
#            pass
        elif method == 'known_position':
            Reactor.add_atom(self, info)
            max_key = max(self.atoms)
            temp_atoms = {}
            temp_atoms[max_key] = self.atoms[max_key]
            self._create_surface(temp_atoms)
        else:
            raise RuntimeError("{0} is an invalid method.".format(method))
            
    #reimplementations of Body_data methods
    def delete_body_data(self, keyword): #finished
        """Add later"""
        if keyword == "Atoms":
            self.surface[:] = []
        Body_data.delete_body_data(self, keyword)
    
    def extract(self, data): #change out parameters
        """Add later"""
        atom_keys = self._extract_atoms(data)
        self._extract_coefficients(data)
        self._extract_velocities(data, atom_keys)
        self._extract_connections(data, atom_keys)
    
    def _extract_atoms(self, data): #change out parameters
        """add later"""
        from copy import deepcopy
        atom_keys = []
        for key, atom in data.atoms.items():
            if self.shape.in_shape(atom):
                self.atoms[key] = deepcopy(data.atoms[key])
                atom_keys.append(key)
        return atom_keys
    
    def add_body_data(self, data):
        """Add later"""
        Body_data.add_body_data(self, data)
        self._create_surface(data.atoms)
    
    def add_atoms(self, atoms): #finished
        """Add later"""
        old_new_keys = Body_data.add_atoms(self, atoms)
        temp_atoms = {}
        for old_key, new_key in old_new_keys.items():
            temp_atoms[new_key] = atoms[old_key]
        self._create_surface(temp_atoms)