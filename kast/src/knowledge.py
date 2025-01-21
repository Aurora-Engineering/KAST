# GSC-19360-1, "Knowledge Acquisition and Synthesis Tool"
#
# Copyright © 2024 United States Government as represented by the 
# Administrator of the National Aeronautics and Space Administration.   
# All Rights Reserved.
#
# Licensed under the NASA Open Source Agreement version 1.3
# See "NOSA GSC-19360-1 KAST.pdf"
from warnings import warn
from typing import Callable

class Knowledge():
    def __init__(self, _label: str, _name: str, _value=None):
        """
        Class representing a single datapoint of knowledge.

        Parameters
        ----------
        _label : str
            Is this knowledge low level (sub-symbolic) or high level (symbolic)?
        _name : str
            What does this knowledge represent? 
        _value : variable
            Information representing the knowledge
        """
        self.label = _label
        self.name = _name
        self.value = _value
        self._type = type(self.value)
    
    def update(self,value):
        if type(value) != self._type and self._type != type(None):
            warn(f"\n\tCaution: {self.name} is being updated with new type; changing {self._type} to {type(value)}")
        self._type = type(value)
        self.value = value
    
    def __str__(self):
        return f"({self.name}: {self.value})"
