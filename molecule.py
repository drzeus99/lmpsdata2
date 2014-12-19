# -*- coding: utf-8 -*-

from body_data import Body_data

class Molecule(Body_data):
    """stores the body_data associated with a specific molecule"""
    def __init__(self, data, molecule_id):
        """builds the molecule by creating a new body_data object with the atom_style
        from the passed in data. the new body_data object extracts the information from
        data that correspond to molecule_id. data is a body_data object. molecule_id
        is an int that corresponds to a molecule number stored in data"""
        Body_data.__init__(self, data.atom_style)
        self.extract(data, "molecule", molecule_id)