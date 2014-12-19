# -*- coding: utf-8 -*-

class Reactor(object):
    """contains methods for modifying the objects stored in body_data. Additionally,
    allows the storage of a body_data object that is allowed to interact with other
    body_data objects"""
    def __init__(self, data):
        """initializes the reactor object with a stored body_data object. data
        is the body_data object to store in the reactor."""
        self._data = data
